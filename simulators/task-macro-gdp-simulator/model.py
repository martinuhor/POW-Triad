"""Pure Acemoglu-style task → TFP/GDP math (no Streamlit dependency)."""

from __future__ import annotations

import numpy as np
import pandas as pd

YEARS = 10
BASE_TFP = 1.0
BASE_GDP = 1.0  # index = 1.0 in year 0


def simulate_paths(
    exposure: float,
    savings_easy: float,
    savings_hard: float,
    easy_share: float,
    adoption_halflife_easy: float,
    adoption_halflife_hard: float,
    capital_drag: float,
) -> pd.DataFrame:
    """
    Discrete-time task automation → TFP → GDP.

    - `exposure`: fraction of labor tasks that are AI-exposed (0–1).
    - Easy vs hard tasks differ in cost savings and adoption speed.
    - GDP growth is TFP growth attenuated by physical capital drag
      (deployment / energy / complementarity friction).
    """
    hard_share = 1.0 - easy_share
    exposed_easy = exposure * easy_share
    exposed_hard = exposure * hard_share

    t = np.arange(0, YEARS + 1, dtype=float)
    adopt_easy = 1.0 - np.power(0.5, t / max(adoption_halflife_easy, 1e-6))
    adopt_hard = 1.0 - np.power(0.5, t / max(adoption_halflife_hard, 1e-6))

    auto_easy = exposed_easy * adopt_easy
    auto_hard = exposed_hard * adopt_hard

    log_tfp = savings_easy * auto_easy + savings_hard * auto_hard
    tfp = BASE_TFP * np.exp(log_tfp)
    gdp = BASE_GDP * np.exp(log_tfp * (1.0 - capital_drag))
    gdp_digital_only = BASE_GDP * tfp

    return pd.DataFrame(
        {
            "year": t.astype(int),
            "adoption_easy": adopt_easy,
            "adoption_hard": adopt_hard,
            "auto_easy_share": auto_easy,
            "auto_hard_share": auto_hard,
            "tfp": tfp,
            "gdp": gdp,
            "gdp_digital_only": gdp_digital_only,
            "tfp_growth_cum_%": 100 * (tfp - 1.0),
            "gdp_growth_cum_%": 100 * (gdp - 1.0),
        }
    )
