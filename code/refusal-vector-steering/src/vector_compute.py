"""Difference-in-means refusal vector and orthogonal projection helpers."""

from __future__ import annotations

import numpy as np


def difference_in_means(
    harmful_mean: np.ndarray, harmless_mean: np.ndarray, normalize: bool = True
) -> np.ndarray:
    """
    r̂ = μ_harmful − μ_harmless  (optionally unit-normalized).

    This is the classic directional activation-steering / ablation direction
    used in refusal studies (e.g., Arditi et al.–style difference-in-means).
    """
    vec = np.asarray(harmful_mean, dtype=np.float64) - np.asarray(
        harmless_mean, dtype=np.float64
    )
    if normalize:
        n = np.linalg.norm(vec) + 1e-12
        vec = vec / n
    return vec


def project_orthogonal(x: np.ndarray, direction: np.ndarray) -> np.ndarray:
    """Remove the component of x along `direction`: x − (x·r̂) r̂."""
    x = np.asarray(x, dtype=np.float64)
    r = np.asarray(direction, dtype=np.float64)
    r = r / (np.linalg.norm(r) + 1e-12)
    return x - np.dot(x, r) * r


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    return float(np.dot(a, b) / ((np.linalg.norm(a) + 1e-12) * (np.linalg.norm(b) + 1e-12)))


def ablation_effect_norm(before: np.ndarray, after: np.ndarray) -> float:
    """Relative L2 change after ablating the refusal direction."""
    before = np.asarray(before, dtype=np.float64)
    after = np.asarray(after, dtype=np.float64)
    return float(np.linalg.norm(before - after) / (np.linalg.norm(before) + 1e-12))
