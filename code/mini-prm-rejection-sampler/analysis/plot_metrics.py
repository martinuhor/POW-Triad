"""Plot PRM vs ORM filter metrics."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt


def plot_prm_vs_orm(stats: Dict, out_path: Path) -> Path:
    labels = ["Accept rate", "Exact match", "Diversity proxy"]
    prm_vals = [
        stats["prm_accept_rate"],
        stats["prm_exact_match"],
        stats["diversity_proxy_prm"],
    ]
    orm_vals = [
        stats["orm_accept_rate"],
        stats["orm_exact_match"],
        stats["diversity_proxy_orm"],
    ]

    x = range(len(labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar([i - width / 2 for i in x], prm_vals, width, label="PRM (step-level)")
    ax.bar([i + width / 2 for i in x], orm_vals, width, label="ORM (outcome)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Rate")
    ax.set_title("Step-level PRM rejection vs ORM outcome filtering")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path
