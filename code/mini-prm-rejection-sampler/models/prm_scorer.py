"""Process Reward Model (PRM) and Outcome Reward Model (ORM) scorers."""

from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from typing import List

from config import Config
from models.generator import Step, Trajectory


class BasePRM(ABC):
    @abstractmethod
    def score_step(self, prompt: str, prior_steps: List[Step], step: Step) -> float:
        """Return P(step is correct | context) in [0, 1]."""
        raise NotImplementedError

    def score_trajectory_steps(self, traj: Trajectory) -> List[float]:
        scores = []
        prior: List[Step] = []
        for step in traj.steps:
            scores.append(self.score_step(traj.prompt, prior, step))
            prior.append(step)
        return scores


class BaseORM(ABC):
    @abstractmethod
    def score_outcome(self, traj: Trajectory, gold: str | None = None) -> float:
        """Return P(final answer / trajectory is correct) in [0, 1]."""
        raise NotImplementedError


class MockPRM(BasePRM):
    """
    Heuristic PRM: rewards steps that look like careful reasoning;
    penalizes guess / contradiction / wrong-operation language.
    """

    POS = ("identify", "equation", "simplify", "check", "parse", "solve", "apply the correct")
    NEG = ("guess", "skip", "contradict", "misread", "wrong operation", "inconsistent", "propagat")

    def score_step(self, prompt: str, prior_steps: List[Step], step: Step) -> float:
        t = step.text.lower()
        score = 0.5
        if any(p in t for p in self.POS):
            score += 0.25
        if any(n in t for n in self.NEG):
            score -= 0.35
        # Slight position prior: later cleanup steps a bit higher if not negative
        score += 0.02 * step.index
        return float(min(1.0, max(0.0, score)))


class MockORM(BaseORM):
    """Outcome scorer: exact gold match if provided, else hash-stable pseudo-score."""

    def score_outcome(self, traj: Trajectory, gold: str | None = None) -> float:
        if gold is not None:
            ans = traj.final_answer.strip().lower()
            g = gold.strip().lower()
            if ans == g:
                return 0.95
            if g in ans:
                return 0.75
            return 0.2
        h = hashlib.md5(traj.full_text.encode()).hexdigest()
        return (int(h[:8], 16) % 100) / 100.0


class HFPRM(BasePRM):
    """
    Placeholder HF adapter: treat a causal LM as a pointwise PRM via
    next-token yes/no logprob ratio. Swap in a real PRM checkpoint for production.
    """

    def __init__(self, model_name: str):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.eval()

    def score_step(self, prompt: str, prior_steps: List[Step], step: Step) -> float:
        ctx = prompt + "\n" + "\n".join(s.text for s in prior_steps) + "\n" + step.text
        query = ctx + "\nIs this step correct? Answer yes or no:"
        inputs = self.tokenizer(query, return_tensors="pt")
        with self.torch.no_grad():
            logits = self.model(**inputs).logits[0, -1]
        yes_id = self.tokenizer.encode(" yes", add_special_tokens=False)[0]
        no_id = self.tokenizer.encode(" no", add_special_tokens=False)[0]
        probs = self.torch.softmax(logits, dim=-1)
        p_yes = float(probs[yes_id])
        p_no = float(probs[no_id])
        denom = p_yes + p_no + 1e-8
        return p_yes / denom


def build_prm(cfg: Config) -> BasePRM:
    if cfg.prm_backend.lower() == "mock":
        return MockPRM()
    if cfg.prm_backend.lower() == "hf":
        return HFPRM(cfg.model_name)
    raise ValueError(f"Unknown prm_backend: {cfg.prm_backend}")


def build_orm(cfg: Config) -> BaseORM:
    # ORM demo always uses mock outcome head; swap freely for a trained ORM
    return MockORM()
