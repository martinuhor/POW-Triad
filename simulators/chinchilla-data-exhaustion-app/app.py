"""
Chinchilla Data Exhaustion Simulator
------------------------------------
Maps Hoffmann et al. Chinchilla-optimal compute (C ≈ 6ND) against
Villalobos et al. human-data exhaustion bounds (D_max), with optional
synthetic-token mix and an effective-data quality penalty.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from model import (
    A,
    ALPHA,
    B,
    BETA,
    DEFAULT_D_HUMAN,
    E,
    FLOPS_PER_TOKEN_PARAM,
    chinchilla_optimal_nd,
    effective_tokens,
    loss,
    loss_penalty_vs_chinchilla,
    tokens_under_budget,
)

st.set_page_config(
    page_title="Chinchilla Data Exhaustion",
    page_icon="📉",
    layout="wide",
)

st.title("Chinchilla Data Exhaustion App")
st.markdown(
    """
Interactive map of **Hoffmann et al.** optimal compute allocation
($C \\approx 6ND$) against **Villalobos et al.** human-data exhaustion
($D_{\\max}$), including synthetic-token mix and loss-efficiency walls.
"""
)

with st.sidebar:
    st.header("Compute & Scale")
    log_c = st.slider(
        "Compute budget C (log10 FLOPs)",
        min_value=23.0,
        max_value=28.0,
        value=25.0,
        step=0.1,
        help="Training FLOPs. Frontier cluster scale is roughly 10²⁵–10²⁷.",
    )
    c = 10.0**log_c

    log_n = st.slider(
        "Parameter count N (log10)",
        min_value=9.0,
        max_value=13.0,
        value=11.0,
        step=0.05,
        help="Model size in parameters (10¹¹ ≈ 100B).",
    )
    n = 10.0**log_n

    st.header("Data Caps")
    log_d_human = st.slider(
        "Human token cap D_human (log10)",
        min_value=12.0,
        max_value=15.0,
        value=14.0,
        step=0.05,
        help="Villalobos-style high-quality human text ceiling (~10¹⁴).",
    )
    d_human = 10.0**log_d_human

    synth_ratio = st.slider(
        "Synthetic token mix ratio",
        min_value=0.0,
        max_value=5.0,
        value=1.0,
        step=0.1,
        help="D_synthetic / D_human. 0 = pure human data.",
    )
    d_synthetic = synth_ratio * d_human

    quality = st.slider(
        "Synthetic quality δ",
        min_value=0.0,
        max_value=1.0,
        value=0.6,
        step=0.05,
        help="Effective-token multiplier for synthetic data (PRM/compiler filtering raises δ).",
    )

n_star, d_star = chinchilla_optimal_nd(c)
d_eff = effective_tokens(d_human, d_synthetic, quality)
d_from_budget = tokens_under_budget(c, n)

# Feasible tokens: cannot exceed effective supply; cannot exceed compute budget at chosen N
d_used = min(d_from_budget, d_eff)
# If data-capped below Chinchilla D*, excess compute buys parameters (over-training wall)
data_capped = d_eff < d_star

l_actual = float(loss(n, d_used))
l_chin = float(loss(n_star, d_star))
penalty = loss_penalty_vs_chinchilla(l_actual, l_chin)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Compute C", f"{c:.2e} FLOPs")
col2.metric("Chinchilla N*, D*", f"{n_star:.2e}")
col3.metric("D_eff (human+δ·synth)", f"{d_eff:.2e}")
col4.metric("Loss penalty vs Chin.", f"{100 * penalty:.1f}%")

if data_capped:
    st.warning(
        f"Data-capped regime: $D_{{\\mathrm{{eff}}}}$ ({d_eff:.2e}) < Chinchilla $D^*$ "
        f"({d_star:.2e}). Further compute buys **parameter over-training**, not matched tokens."
    )
else:
    st.success(
        "Still inside the Chinchilla 1:1 scaling corridor for this compute budget "
        "(effective tokens can match $D^*$)."
    )

# --- Chart 1: loss vs compute with / without data cap ---
log_c_grid = np.linspace(23.0, 28.0, 120)
c_grid = 10.0**log_c_grid
n_stars = np.sqrt(c_grid / FLOPS_PER_TOKEN_PARAM)
d_stars = n_stars.copy()

# Unconstrained Chinchilla loss
l_unconstrained = loss(n_stars, d_stars)

# Data-capped: D fixed at D_eff; N = C / (6 D_eff)
d_cap = np.full_like(c_grid, d_eff)
n_capped = c_grid / (FLOPS_PER_TOKEN_PARAM * d_cap)
l_capped = loss(n_capped, d_cap)

# Inflection: where D* hits D_eff
inflection_c = FLOPS_PER_TOKEN_PARAM * d_eff * d_eff
inflection_log_c = float(np.log10(inflection_c))

fig_loss = go.Figure()
fig_loss.add_trace(
    go.Scatter(
        x=log_c_grid,
        y=l_unconstrained,
        name="Unconstrained Chinchilla (1:1)",
        line=dict(width=3),
    )
)
fig_loss.add_trace(
    go.Scatter(
        x=log_c_grid,
        y=l_capped,
        name="Data-capped over-training wall",
        line=dict(width=3, dash="dash"),
    )
)
fig_loss.add_vline(
    x=inflection_log_c,
    line_dash="dot",
    annotation_text="Inflection: D* = D_eff",
)
fig_loss.add_vline(
    x=log_c,
    line_dash="solid",
    line_color="crimson",
    annotation_text="Your C",
)
fig_loss.update_layout(
    title="Loss efficiency: Chinchilla vs data-capped wall",
    xaxis_title="log₁₀ Compute (FLOPs)",
    yaxis_title="Predicted loss L(N, D)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    height=480,
)
st.plotly_chart(fig_loss, use_container_width=True)

# --- Chart 2: N–D plane ---
log_n_grid = np.linspace(9.0, 13.0, 80)
n_grid = 10.0**log_n_grid
d_iso = c / (FLOPS_PER_TOKEN_PARAM * n_grid)

fig_nd = go.Figure()
fig_nd.add_trace(
    go.Scatter(
        x=np.log10(n_grid),
        y=np.log10(d_iso),
        name=f"IsoFLOP C={c:.1e}",
        line=dict(width=2),
    )
)
fig_nd.add_hline(
    y=np.log10(d_human),
    line_dash="dash",
    annotation_text="D_human",
)
fig_nd.add_hline(
    y=np.log10(d_eff),
    line_dash="dot",
    annotation_text="D_eff",
)
fig_nd.add_trace(
    go.Scatter(
        x=[np.log10(n_star)],
        y=[np.log10(d_star)],
        mode="markers+text",
        text=["Chin. opt"],
        textposition="top center",
        name="Chinchilla optimum",
        marker=dict(size=14, symbol="star"),
    )
)
fig_nd.add_trace(
    go.Scatter(
        x=[np.log10(n)],
        y=[np.log10(d_used)],
        mode="markers+text",
        text=["Your (N, D_used)"],
        textposition="bottom center",
        name="Selected point",
        marker=dict(size=12, color="crimson"),
    )
)
fig_nd.update_layout(
    title="Parameter–token plane under fixed compute",
    xaxis_title="log₁₀ N (parameters)",
    yaxis_title="log₁₀ D (tokens)",
    height=480,
)
st.plotly_chart(fig_nd, use_container_width=True)

# --- Table: sweep synthetic quality ---
st.subheader("Synthetic quality sweep at fixed C and D_human")
deltas = np.linspace(0.0, 1.0, 11)
rows = []
for delta in deltas:
    de = effective_tokens(d_human, d_synthetic, float(delta))
    du = min(d_from_budget, de)
    la = float(loss(n, du))
    rows.append(
        {
            "δ": round(float(delta), 2),
            "D_eff": de,
            "D_used": du,
            "L(N, D_used)": la,
            "penalty_vs_chin_%": 100 * loss_penalty_vs_chinchilla(la, l_chin),
            "data_capped": de < d_star,
        }
    )
st.dataframe(pd.DataFrame(rows), use_container_width=True)

with st.expander("Math reference"):
    st.latex(r"L(N,D)=E+\frac{A}{N^{\alpha}}+\frac{B}{D^{\beta}}")
    st.latex(r"C \approx 6ND \quad\Rightarrow\quad N^{*}=D^{*}=\sqrt{C/6}")
    st.latex(r"D_{\mathrm{eff}}=D_{\mathrm{human}}+\delta\,D_{\mathrm{synthetic}}")
    st.markdown(
        f"Constants: $A={A}$, $B={B}$, $E={E}$, $\\alpha={ALPHA}$, $\\beta={BETA}$. "
        f"Default human cap stylized at ${DEFAULT_D_HUMAN:.0e}$ tokens (Villalobos-scale)."
    )
