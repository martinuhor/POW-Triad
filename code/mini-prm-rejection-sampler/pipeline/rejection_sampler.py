"""Step-level PRM rejection sampling vs ORM outcome filtering."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from models.generator import BaseGenerator, Trajectory
from models.prm_scorer import BaseORM, BasePRM


@dataclass
class ScoredTrajectory:
    trajectory: Trajectory
    step_scores: List[float]
    min_step_score: float
    mean_step_score: float
    orm_score: float
    accepted_prm: bool
    accepted_orm: bool


@dataclass
class FilterResult:
    prompt_id: str
    prompt: str
    gold: Optional[str]
    candidates: List[ScoredTrajectory] = field(default_factory=list)
    prm_selected: Optional[ScoredTrajectory] = None
    orm_selected: Optional[ScoredTrajectory] = None


class StepLevelRejectionSampler:
    """
    Compare two synthetic-data filters on the same candidate pool:

    1. **PRM (step-level rejection)**: reject any trajectory whose *minimum*
       per-step process score falls below `prm_step_threshold`. Among survivors,
       pick the highest mean step score (optional ORM tie-break).
    2. **ORM (outcome filtering)**: ignore intermediate steps; keep trajectories
       whose final outcome score ≥ `orm_threshold`, pick the max ORM score.

    This is the core demo that step-level process filtering retains higher-quality
    reasoning traces than outcome-only filtering — reducing early model collapse
    when generating synthetic trajectories.
    """

    def __init__(
        self,
        generator: BaseGenerator,
        prm: BasePRM,
        orm: BaseORM,
        n_candidates: int = 8,
        max_steps: int = 4,
        prm_step_threshold: float = 0.55,
        orm_threshold: float = 0.60,
    ):
        self.generator = generator
        self.prm = prm
        self.orm = orm
        self.n_candidates = n_candidates
        self.max_steps = max_steps
        self.prm_step_threshold = prm_step_threshold
        self.orm_threshold = orm_threshold

    def _generate(self, prompt_id: str, prompt: str, gold: Optional[str]) -> List[Trajectory]:
        # MockGenerator accepts gold; other backends ignore via signature variance
        gen = self.generator
        if hasattr(gen, "sample_trajectories"):
            try:
                return gen.sample_trajectories(  # type: ignore[call-arg]
                    prompt_id, prompt, self.n_candidates, self.max_steps, gold=gold
                )
            except TypeError:
                return gen.sample_trajectories(
                    prompt_id, prompt, self.n_candidates, self.max_steps
                )
        raise RuntimeError("Generator missing sample_trajectories")

    def filter_prompt(
        self, prompt_id: str, prompt: str, gold: Optional[str] = None
    ) -> FilterResult:
        trajs = self._generate(prompt_id, prompt, gold)
        scored: List[ScoredTrajectory] = []
        for traj in trajs:
            step_scores = self.prm.score_trajectory_steps(traj)
            orm_score = self.orm.score_outcome(traj, gold=gold)
            min_s = min(step_scores) if step_scores else 0.0
            mean_s = sum(step_scores) / len(step_scores) if step_scores else 0.0
            scored.append(
                ScoredTrajectory(
                    trajectory=traj,
                    step_scores=step_scores,
                    min_step_score=min_s,
                    mean_step_score=mean_s,
                    orm_score=orm_score,
                    accepted_prm=min_s >= self.prm_step_threshold,
                    accepted_orm=orm_score >= self.orm_threshold,
                )
            )

        prm_pool = [s for s in scored if s.accepted_prm]
        orm_pool = [s for s in scored if s.accepted_orm]

        prm_selected = (
            max(prm_pool, key=lambda s: (s.mean_step_score, s.orm_score))
            if prm_pool
            else None
        )
        orm_selected = (
            max(orm_pool, key=lambda s: s.orm_score) if orm_pool else None
        )

        return FilterResult(
            prompt_id=prompt_id,
            prompt=prompt,
            gold=gold,
            candidates=scored,
            prm_selected=prm_selected,
            orm_selected=orm_selected,
        )

    def run(self, items: List[Dict]) -> List[FilterResult]:
        results = []
        for item in items:
            results.append(
                self.filter_prompt(
                    prompt_id=item["id"],
                    prompt=item["prompt"],
                    gold=item.get("gold"),
                )
            )
        return results
