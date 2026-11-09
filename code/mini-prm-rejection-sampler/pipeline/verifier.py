"""Post-filter verification: compare selected answers against gold labels."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from pipeline.rejection_sampler import FilterResult, ScoredTrajectory


@dataclass
class VerifyStats:
    n_prompts: int
    prm_accept_rate: float
    orm_accept_rate: float
    prm_exact_match: float
    orm_exact_match: float
    prm_mean_min_step: float
    orm_mean_outcome: float
    collapse_proxy_prm: float
    collapse_proxy_orm: float


def _exact(selected: Optional[ScoredTrajectory], gold: Optional[str]) -> bool:
    if selected is None or gold is None:
        return False
    return selected.trajectory.final_answer.strip().lower() == gold.strip().lower()


def _unique_answer_ratio(result: FilterResult, mode: str) -> float:
    """Proxy for diversity / anti-collapse: unique finals among accepted set."""
    if mode == "prm":
        pool = [c for c in result.candidates if c.accepted_prm]
    else:
        pool = [c for c in result.candidates if c.accepted_orm]
    if not pool:
        return 0.0
    uniq = {c.trajectory.final_answer.strip().lower() for c in pool}
    return len(uniq) / len(pool)


def summarize(results: List[FilterResult]) -> VerifyStats:
    n = len(results)
    if n == 0:
        return VerifyStats(0, 0, 0, 0, 0, 0, 0, 0, 0)

    prm_acc = sum(1 for r in results if r.prm_selected is not None) / n
    orm_acc = sum(1 for r in results if r.orm_selected is not None) / n
    prm_em = sum(1 for r in results if _exact(r.prm_selected, r.gold)) / n
    orm_em = sum(1 for r in results if _exact(r.orm_selected, r.gold)) / n

    prm_mins = [
        c.min_step_score
        for r in results
        for c in r.candidates
        if c.accepted_prm
    ]
    orm_outs = [
        c.orm_score for r in results for c in r.candidates if c.accepted_orm
    ]

    # Higher unique-answer ratio among accepted = less collapse
    collapse_prm = sum(_unique_answer_ratio(r, "prm") for r in results) / n
    collapse_orm = sum(_unique_answer_ratio(r, "orm") for r in results) / n

    return VerifyStats(
        n_prompts=n,
        prm_accept_rate=prm_acc,
        orm_accept_rate=orm_acc,
        prm_exact_match=prm_em,
        orm_exact_match=orm_em,
        prm_mean_min_step=(sum(prm_mins) / len(prm_mins)) if prm_mins else 0.0,
        orm_mean_outcome=(sum(orm_outs) / len(orm_outs)) if orm_outs else 0.0,
        collapse_proxy_prm=collapse_prm,
        collapse_proxy_orm=collapse_orm,
    )


def stats_as_dict(stats: VerifyStats) -> dict:
    return {
        "n_prompts": stats.n_prompts,
        "prm_accept_rate": stats.prm_accept_rate,
        "orm_accept_rate": stats.orm_accept_rate,
        "prm_exact_match": stats.prm_exact_match,
        "orm_exact_match": stats.orm_exact_match,
        "prm_mean_min_step": stats.prm_mean_min_step,
        "orm_mean_outcome": stats.orm_mean_outcome,
        "diversity_proxy_prm": stats.collapse_proxy_prm,
        "diversity_proxy_orm": stats.collapse_proxy_orm,
    }
