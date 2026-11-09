# Proof-of-Work Triad

Live demo: https://pow-triad.pages.dev 

Public portfolio of **three artifact types** for AGI strategy / safety / policy roles:

```
                       THE PROOF-OF-WORK TRIAD
                                   │
      ┌────────────────────────────┼────────────────────────────┐
      ▼                            ▼                            ▼
[ ARTIFACT 1: CODE ]        [ ARTIFACT 2: SIMULATORS ]   [ ARTIFACT 3: STRATEGY ]
• Python PRM Verifier       • Interactive Scaling App    • Executive Policy Memos
• Refusal Vector Ablator    • Task GDP Impact Calculator  • Slide Decks (PDF/Gamma)
```

## Digital dissertation (web)

The public-facing monograph with **embedded client-side simulators** lives in [`site/`](site/). It is designed for **GitHub → Cloudflare Pages**.

```bash
cd site && npm install && npm run dev
```

Deploy notes: [`site/README.md`](site/README.md).

## Repository map

| Artifact | Path | Status |
|---|---|---|
| Dissertation website | [`site/`](site/) | Vite + React; CF Pages ready |
| Repo A — mini PRM rejection sampler | [`code/mini-prm-rejection-sampler/`](code/mini-prm-rejection-sampler/) | Runnable offline (mock) |
| Repo B — refusal vector steering | [`code/refusal-vector-steering/`](code/refusal-vector-steering/) | Mock eval + TL notebook |
| Simulator A — Chinchilla / data wall | [`simulators/chinchilla-data-exhaustion-app/`](simulators/chinchilla-data-exhaustion-app/) | Streamlit |
| Simulator B — Acemoglu task GDP | [`simulators/task-macro-gdp-simulator/`](simulators/task-macro-gdp-simulator/) | Streamlit |
| Memo A — Hardware wall vs data wall | [`memos/hardware-wall-vs-data-wall.md`](memos/hardware-wall-vs-data-wall.md) | Draft |
| Memo B — Weight theft / SCIF controls | [`memos/weight-theft-risks.md`](memos/weight-theft-risks.md) | Draft |
| Build-in-public templates | [`posts/`](posts/) | X + LinkedIn |

## How to run

### Simulator A — Chinchilla data exhaustion

```bash
cd simulators/chinchilla-data-exhaustion-app
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Simulator B — Task macro GDP

```bash
cd simulators/task-macro-gdp-simulator
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Code A — PRM vs ORM sampler (offline)

```bash
cd code/mini-prm-rejection-sampler
pip install numpy matplotlib
python main.py
```

### Code B — Refusal vector (offline mock)

```bash
cd code/refusal-vector-steering
pip install numpy
python eval/benchmark_refusal.py --mock
```

Full TransformerLens path and notebook instructions live in each package README. Heavy deps (`torch`, `vllm`, `transformer-lens`) are optional—swap backends when you have GPU/weights.






## Note on Repo B framing

`refusal-vector-steering` is **defensive / educational** mechanistic interpretability for understanding post-exfiltration safety fragility. It is not an attack guide.





