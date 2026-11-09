#!/usr/bin/env python3
"""Run mini PRM rejection sampling demo (default: fully offline mock backends)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow running as `python main.py` from this directory
sys.path.insert(0, str(Path(__file__).resolve().parent))

from analysis.plot_metrics import plot_prm_vs_orm
from config import get_config
from models.generator import build_generator
from models.prm_scorer import build_orm, build_prm
from pipeline.rejection_sampler import StepLevelRejectionSampler
from pipeline.verifier import stats_as_dict, summarize


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Mini PRM vs ORM rejection sampler")
    p.add_argument("--generator-backend", default="mock", choices=["mock", "hf", "vllm"])
    p.add_argument("--prm-backend", default="mock", choices=["mock", "hf"])
    p.add_argument("--model-name", default="gpt2")
    p.add_argument("--n-candidates", type=int, default=8)
    p.add_argument("--max-steps", type=int, default=4)
    p.add_argument("--prm-threshold", type=float, default=0.55)
    p.add_argument("--orm-threshold", type=float, default=0.60)
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    cfg = get_config(
        generator_backend=args.generator_backend,
        prm_backend=args.prm_backend,
        model_name=args.model_name,
        n_candidates=args.n_candidates,
        max_steps=args.max_steps,
        prm_step_threshold=args.prm_threshold,
        orm_threshold=args.orm_threshold,
        seed=args.seed,
    )
    cfg.output_dir.mkdir(parents=True, exist_ok=True)

    with open(cfg.seed_prompts_path) as f:
        prompts = json.load(f)

    sampler = StepLevelRejectionSampler(
        generator=build_generator(cfg),
        prm=build_prm(cfg),
        orm=build_orm(cfg),
        n_candidates=cfg.n_candidates,
        max_steps=cfg.max_steps,
        prm_step_threshold=cfg.prm_step_threshold,
        orm_threshold=cfg.orm_threshold,
    )
    results = sampler.run(prompts)
    stats = stats_as_dict(summarize(results))

    metrics_path = cfg.output_dir / "metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(stats, f, indent=2)

    # Persist a compact selection log
    selections = []
    for r in results:
        selections.append(
            {
                "id": r.prompt_id,
                "gold": r.gold,
                "prm_answer": None
                if r.prm_selected is None
                else r.prm_selected.trajectory.final_answer,
                "orm_answer": None
                if r.orm_selected is None
                else r.orm_selected.trajectory.final_answer,
                "n_prm_accepted": sum(1 for c in r.candidates if c.accepted_prm),
                "n_orm_accepted": sum(1 for c in r.candidates if c.accepted_orm),
            }
        )
    with open(cfg.output_dir / "selections.json", "w") as f:
        json.dump(selections, f, indent=2)

    plot_path = plot_prm_vs_orm(stats, cfg.output_dir / cfg.plot_filename)

    print("=== Mini PRM Rejection Sampler ===")
    print(json.dumps(stats, indent=2))
    print(f"Wrote {metrics_path}")
    print(f"Wrote {plot_path}")


if __name__ == "__main__":
    main()
