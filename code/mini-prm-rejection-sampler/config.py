"""Pipeline configuration for mini PRM rejection sampling."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent


@dataclass
class Config:
    seed_prompts_path: Path = ROOT / "data" / "seed_prompts.json"
    output_dir: Path = ROOT / "outputs"

    # Sampling
    n_candidates: int = 8
    max_steps: int = 4
    temperature: float = 0.8
    seed: int = 42

    # PRM step-level thresholds
    prm_step_threshold: float = 0.55
    # ORM outcome threshold (final-answer / trajectory score)
    orm_threshold: float = 0.60

    # Backend: "mock" runs fully offline; "hf" uses transformers; "vllm" if installed
    generator_backend: str = "mock"
    prm_backend: str = "mock"
    model_name: str = "gpt2"  # swap for a real chat / math model when ready

    # Analysis
    plot_filename: str = "prm_vs_orm_metrics.png"

    extra: dict = field(default_factory=dict)


def get_config(**overrides) -> Config:
    cfg = Config()
    for k, v in overrides.items():
        if hasattr(cfg, k):
            setattr(cfg, k, v)
        else:
            cfg.extra[k] = v
    return cfg
