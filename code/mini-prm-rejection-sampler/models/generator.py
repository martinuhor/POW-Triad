"""Trajectory generator adapters: mock (offline), HF transformers, optional vLLM."""

from __future__ import annotations

import hashlib
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from config import Config


@dataclass
class Step:
    text: str
    index: int


@dataclass
class Trajectory:
    prompt_id: str
    prompt: str
    steps: List[Step]
    final_answer: str

    @property
    def full_text(self) -> str:
        body = "\n".join(s.text for s in self.steps)
        return f"{self.prompt}\n{body}\nFinal: {self.final_answer}"


class BaseGenerator(ABC):
    @abstractmethod
    def sample_trajectories(
        self, prompt_id: str, prompt: str, n: int, max_steps: int
    ) -> List[Trajectory]:
        raise NotImplementedError


class MockGenerator(BaseGenerator):
    """
    Deterministic-ish offline generator for demo / CI.
    Mixes correct and incorrect reasoning paths so PRM vs ORM differ.
    """

    CORRECT_TEMPLATES = [
        [
            "Identify the quantities in the problem.",
            "Apply the correct arithmetic / logical rule.",
            "Simplify carefully without dropping terms.",
            "Box the final result.",
        ],
        [
            "Parse the question into knowns and unknowns.",
            "Write the governing equation.",
            "Solve step by step.",
            "Check the result against the prompt.",
        ],
    ]
    BAD_TEMPLATES = [
        [
            "Guess a round number without calculating.",
            "Skip an intermediate carry / constraint.",
            "Contradict an earlier step.",
            "Commit to an inconsistent final answer.",
        ],
        [
            "Misread a key quantity from the prompt.",
            "Apply the wrong operation.",
            "Propagate the error silently.",
            "Output a plausible but wrong answer.",
        ],
    ]

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

    def _answer_for(self, prompt: str, correct: bool, gold: str | None) -> str:
        if correct and gold is not None:
            return gold
        # Wrong but stable for a given prompt
        h = int(hashlib.md5(prompt.encode()).hexdigest()[:8], 16)
        return str((h % 97) + 1)

    def sample_trajectories(
        self, prompt_id: str, prompt: str, n: int, max_steps: int, gold: str | None = None
    ) -> List[Trajectory]:
        out: List[Trajectory] = []
        for i in range(n):
            # ~40% correct trajectories in the candidate pool
            correct = self.rng.random() < 0.4
            templates = self.CORRECT_TEMPLATES if correct else self.BAD_TEMPLATES
            template = self.rng.choice(templates)
            steps = [
                Step(text=f"Step {j+1}: {template[j % len(template)]}", index=j)
                for j in range(max_steps)
            ]
            ans = self._answer_for(prompt, correct, gold)
            out.append(
                Trajectory(
                    prompt_id=prompt_id,
                    prompt=prompt,
                    steps=steps,
                    final_answer=ans,
                )
            )
        return out


class HFGenerator(BaseGenerator):
    """Hugging Face transformers generate() adapter (optional heavy path)."""

    def __init__(self, model_name: str, temperature: float = 0.8):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.temperature = temperature
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.eval()
        self.torch = torch
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def sample_trajectories(
        self, prompt_id: str, prompt: str, n: int, max_steps: int
    ) -> List[Trajectory]:
        # Single-shot generations; split into pseudo-steps by newline
        inputs = self.tokenizer(prompt, return_tensors="pt")
        trajs: List[Trajectory] = []
        with self.torch.no_grad():
            for _ in range(n):
                out = self.model.generate(
                    **inputs,
                    max_new_tokens=128,
                    do_sample=True,
                    temperature=self.temperature,
                    pad_token_id=self.tokenizer.eos_token_id,
                )
                text = self.tokenizer.decode(out[0], skip_special_tokens=True)
                lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
                if not lines:
                    lines = [text]
                # Pad / trim to max_steps
                while len(lines) < max_steps:
                    lines.append("(continue)")
                lines = lines[:max_steps]
                steps = [Step(text=ln, index=i) for i, ln in enumerate(lines)]
                trajs.append(
                    Trajectory(
                        prompt_id=prompt_id,
                        prompt=prompt,
                        steps=steps,
                        final_answer=lines[-1][:64],
                    )
                )
        return trajs


class VLLMGenerator(BaseGenerator):
    """vLLM adapter — only imported when backend=vllm."""

    def __init__(self, model_name: str, temperature: float = 0.8):
        try:
            from vllm import LLM, SamplingParams
        except ImportError as e:
            raise ImportError(
                "vLLM not installed. `pip install vllm` on a CUDA host, "
                "or set generator_backend='mock'."
            ) from e
        self.llm = LLM(model=model_name)
        self.params = SamplingParams(temperature=temperature, max_tokens=128)

    def sample_trajectories(
        self, prompt_id: str, prompt: str, n: int, max_steps: int
    ) -> List[Trajectory]:
        prompts = [prompt] * n
        outputs = self.llm.generate(prompts, self.params)
        trajs: List[Trajectory] = []
        for out in outputs:
            text = out.outputs[0].text
            lines = [ln.strip() for ln in text.split("\n") if ln.strip()] or [text]
            while len(lines) < max_steps:
                lines.append("(continue)")
            lines = lines[:max_steps]
            steps = [Step(text=ln, index=i) for i, ln in enumerate(lines)]
            trajs.append(
                Trajectory(
                    prompt_id=prompt_id,
                    prompt=prompt,
                    steps=steps,
                    final_answer=lines[-1][:64],
                )
            )
        return trajs


def build_generator(cfg: Config) -> BaseGenerator:
    backend = cfg.generator_backend.lower()
    if backend == "mock":
        return MockGenerator(seed=cfg.seed)
    if backend == "hf":
        return HFGenerator(cfg.model_name, temperature=cfg.temperature)
    if backend == "vllm":
        return VLLMGenerator(cfg.model_name, temperature=cfg.temperature)
    raise ValueError(f"Unknown generator_backend: {cfg.generator_backend}")
