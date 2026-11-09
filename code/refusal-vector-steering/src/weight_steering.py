"""
Activation steering / orthogonal ablation hooks for TransformerLens models.

Educational safety-research tooling: quantifies how strongly refusal is
linearly represented, and how fragile that representation is under ablation —
a concrete input to open-weights exfiltration risk assessments.
"""

from __future__ import annotations

from typing import Callable, Optional

import numpy as np


def make_orthogonal_ablation_hook(
    direction: np.ndarray, layer: int
) -> tuple[str, Callable]:
    """
    Return (hook_name, hook_fn) that projects the residual stream orthogonal
    to the refusal direction at `blocks.{layer}.hook_resid_post`.
    """
    import torch

    r = torch.tensor(direction, dtype=torch.float32)
    r = r / (torch.linalg.norm(r) + 1e-12)
    hook_name = f"blocks.{layer}.hook_resid_post"

    def hook_fn(resid, hook):
        # resid: [batch, pos, d_model]
        # Ablate along r for all positions (demo); production code may limit to last token.
        dots = torch.einsum("bpd,d->bp", resid.float(), r.to(resid.device))
        resid = resid - dots[..., None] * r.to(resid.device)
        return resid

    return hook_name, hook_fn


def make_addition_steer_hook(
    direction: np.ndarray, layer: int, scale: float = 1.0
) -> tuple[str, Callable]:
    """Add ±scale * r̂ into the residual stream (steering, not ablation)."""
    import torch

    r = torch.tensor(direction, dtype=torch.float32)
    r = r / (torch.linalg.norm(r) + 1e-12)
    hook_name = f"blocks.{layer}.hook_resid_post"

    def hook_fn(resid, hook):
        return resid + scale * r.to(resid.device)

    return hook_name, hook_fn


def generate_with_hook(
    model,
    prompt: str,
    hook_name: Optional[str] = None,
    hook_fn: Optional[Callable] = None,
    max_new_tokens: int = 64,
) -> str:
    """Greedy-ish generate with an optional resid hook installed."""
    tokens = model.to_tokens(prompt, prepend_bos=True)
    if hook_name is not None and hook_fn is not None:
        with model.hooks(fwd_hooks=[(hook_name, hook_fn)]):
            out = model.generate(tokens, max_new_tokens=max_new_tokens, do_sample=False)
    else:
        out = model.generate(tokens, max_new_tokens=max_new_tokens, do_sample=False)
    return model.to_string(out[0])


def mock_ablate_vector(x: np.ndarray, direction: np.ndarray) -> np.ndarray:
    """Pure-numpy ablation for offline unit checks."""
    from src.vector_compute import project_orthogonal

    return project_orthogonal(x, direction)
