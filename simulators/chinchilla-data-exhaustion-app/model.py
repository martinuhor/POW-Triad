"""Pure Chinchilla / data-exhaustion math (no Streamlit dependency)."""

from __future__ import annotations

import numpy as np

# Hoffmann et al. (2022) IsoFLOP / Chinchilla loss fit
A = 406.4
B = 410.7
E = 1.69
ALPHA = 0.34
BETA = 0.28

# FLOPs ≈ 6 N D for dense transformers
FLOPS_PER_TOKEN_PARAM = 6.0

# Villalobos et al. stylized human-token ceiling (tokens)
DEFAULT_D_HUMAN = 1e14


def loss(n: np.ndarray | float, d: np.ndarray | float) -> np.ndarray | float:
    """L(N, D) = E + A / N^α + B / D^β"""
    return E + A / np.power(n, ALPHA) + B / np.power(d, BETA)


def chinchilla_optimal_nd(c: float) -> tuple[float, float]:
    """Compute-optimal N*, D* under C = 6ND for Hoffmann loss exponents."""
    coeff = (ALPHA * A) / (BETA * B)
    n = coeff ** (1 / (ALPHA + BETA)) * (c / FLOPS_PER_TOKEN_PARAM) ** (
        BETA / (ALPHA + BETA)
    )
    d = c / (FLOPS_PER_TOKEN_PARAM * n)
    return float(n), float(d)


def effective_tokens(d_human: float, d_synthetic: float, quality: float) -> float:
    """Effective data after synthetic quality penalty: D_eff = D_h + δ · D_s."""
    return d_human + quality * d_synthetic


def tokens_under_budget(c: float, n: float) -> float:
    """D = C / (6N)."""
    return c / (FLOPS_PER_TOKEN_PARAM * n)


def loss_penalty_vs_chinchilla(l_actual: float, l_chin: float) -> float:
    """Relative loss inefficiency vs unconstrained Chinchilla optimum."""
    if l_chin <= 0:
        return 0.0
    return (l_actual - l_chin) / l_chin
