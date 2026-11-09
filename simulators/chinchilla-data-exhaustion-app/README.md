# Chinchilla Data Exhaustion App

Interactive Streamlit simulator mapping **Hoffmann et al.** Chinchilla-optimal compute ($C \approx 6ND$) against **Villalobos et al.** human-data exhaustion bounds ($D_{\max}$), with synthetic-token mix and loss-penalty charts.

## What it shows

- Unconstrained 1:1 Chinchilla scaling loss curve
- Inflection where $D^* = D_{\mathrm{eff}}$ (data-capped over-training wall)
- Sliders for compute $C$, parameters $N$, human token cap, synthetic mix ratio, and quality $\delta$
- IsoFLOP $N$–$D$ plane with your selected operating point

## Run locally

```bash
cd simulators/chinchilla-data-exhaustion-app
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (Hugging Face Spaces)

Create a Space with SDK **Streamlit**, upload `app.py` + `requirements.txt`, and set the entrypoint to `app.py`.

## Math

$$
L(N,D)=E+\frac{A}{N^{\alpha}}+\frac{B}{D^{\beta}},\quad
C\approx 6ND,\quad
D_{\mathrm{eff}}=D_{\mathrm{human}}+\delta D_{\mathrm{synthetic}}
$$

Hoffmann constants baked in: $A=406.4$, $B=410.7$, $E=1.69$, $\alpha=0.34$, $\beta=0.28$.
