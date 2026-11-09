"""
Task Macro GDP Simulator
------------------------
Interactive implementation of a Daron Acemoglu–style task-based
macroeconomic framework: task exposure, cost savings on easy vs hard
tasks, and predicted 10-year TFP / GDP paths.
"""

from __future__ import annotations

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from model import simulate_paths

st.set_page_config(
    page_title="Task Macro GDP Simulator",
    page_icon="📈",
    layout="wide",
)

st.title("Task Macro GDP Simulator")
st.markdown(
    """
Acemoglu-style **task-based** macro simulator. Adjust AI task exposure and
cost savings on easy vs hard tasks to see **10-year TFP and GDP** index paths,
including a physical-capital / deployment drag vs a pure digital R&D path.
"""
)

with st.sidebar:
    st.header("Task structure")
    exposure = st.slider(
        "Task exposure %",
        min_value=0.0,
        max_value=100.0,
        value=40.0,
        step=1.0,
        help="Share of economy-wide tasks that are AI-exposed.",
    ) / 100.0

    easy_share = st.slider(
        "Easy-task share of exposed tasks %",
        min_value=0.0,
        max_value=100.0,
        value=60.0,
        step=1.0,
        help="Hard-task share is the complement.",
    ) / 100.0

    st.header("Cost savings per automated task")
    savings_easy = st.slider(
        "Cost savings — easy tasks",
        min_value=0.0,
        max_value=0.5,
        value=0.25,
        step=0.01,
        help="Log-TFP contribution weight when an easy task is automated.",
    )
    savings_hard = st.slider(
        "Cost savings — hard tasks",
        min_value=0.0,
        max_value=0.5,
        value=0.10,
        step=0.01,
        help="Typically lower: hard tasks need complementary capital / HTI redesign.",
    )

    st.header("Adoption & frictions")
    half_easy = st.slider("Easy adoption half-life (years)", 0.5, 8.0, 2.0, 0.5)
    half_hard = st.slider("Hard adoption half-life (years)", 0.5, 12.0, 6.0, 0.5)
    capital_drag = st.slider(
        "Physical capital / deployment drag",
        min_value=0.0,
        max_value=0.9,
        value=0.45,
        step=0.05,
        help="Fraction of TFP gains that do not pass through to measured GDP "
        "(energy, buildings, regulation, complementarity).",
    )

df = simulate_paths(
    exposure=exposure,
    savings_easy=savings_easy,
    savings_hard=savings_hard,
    easy_share=easy_share,
    adoption_halflife_easy=half_easy,
    adoption_halflife_hard=half_hard,
    capital_drag=capital_drag,
)

y10 = df.iloc[-1]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Year-10 TFP index", f"{y10['tfp']:.3f}", f"+{y10['tfp_growth_cum_%']:.1f}%")
c2.metric("Year-10 GDP index", f"{y10['gdp']:.3f}", f"+{y10['gdp_growth_cum_%']:.1f}%")
c3.metric("Digital-only GDP (no drag)", f"{y10['gdp_digital_only']:.3f}")
c4.metric(
    "GDP lag vs digital-only",
    f"{100 * (y10['gdp_digital_only'] - y10['gdp']):.1f} pp",
)

fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=("TFP index (10 years)", "GDP index: with drag vs digital-only"),
)
fig.add_trace(
    go.Scatter(x=df["year"], y=df["tfp"], name="TFP", line=dict(width=3)),
    row=1,
    col=1,
)
fig.add_trace(
    go.Scatter(x=df["year"], y=df["gdp"], name="GDP (w/ drag)", line=dict(width=3)),
    row=1,
    col=2,
)
fig.add_trace(
    go.Scatter(
        x=df["year"],
        y=df["gdp_digital_only"],
        name="GDP digital-only",
        line=dict(width=2, dash="dash"),
    ),
    row=1,
    col=2,
)
fig.update_xaxes(title_text="Year", row=1, col=1)
fig.update_xaxes(title_text="Year", row=1, col=2)
fig.update_yaxes(title_text="Index (Y0=1)", row=1, col=1)
fig.update_yaxes(title_text="Index (Y0=1)", row=1, col=2)
fig.update_layout(height=480, legend=dict(orientation="h", y=1.12))
st.plotly_chart(fig, use_container_width=True)

st.subheader("Adoption & automated task mass")
fig2 = go.Figure()
fig2.add_trace(
    go.Scatter(x=df["year"], y=df["adoption_easy"], name="Easy adoption CDF", line=dict(width=2))
)
fig2.add_trace(
    go.Scatter(x=df["year"], y=df["adoption_hard"], name="Hard adoption CDF", line=dict(width=2))
)
fig2.add_trace(
    go.Scatter(
        x=df["year"],
        y=df["auto_easy_share"] + df["auto_hard_share"],
        name="Total automated task share",
        line=dict(width=3, dash="dot"),
    )
)
fig2.update_layout(
    xaxis_title="Year",
    yaxis_title="Share",
    height=400,
    legend=dict(orientation="h", y=1.12),
)
st.plotly_chart(fig2, use_container_width=True)

st.dataframe(df.round(4), use_container_width=True)

with st.expander("Model notes"):
    st.markdown(
        r"""
**Task exposure** $\tau$ splits into easy / hard shares.
Adoption follows a half-life CDF: $a_t = 1 - 1/2^{t/h}$.
Log TFP accumulates as $\log A_t = s_e\,\tau_e a^e_t + s_h\,\tau_h a^h_t$.
GDP passes a fraction $(1-\kappa)$ of that TFP path, where $\kappa$ is physical
capital / deployment drag — the core Acemoglu / Erdil macro-skeptic channel
versus pure digital R&D acceleration.
"""
    )
