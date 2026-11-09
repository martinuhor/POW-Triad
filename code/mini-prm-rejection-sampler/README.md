# mini-prm-rejection-sampler

Lightweight Python demo: **step-level Process Reward Model (PRM) rejection sampling** vs **outcome-only (ORM) filtering** on synthetic reasoning trajectories.

## Why this exists

When labs generate synthetic reasoning data, outcome-only filters let through trajectories that *guess right* with broken intermediate steps — a fast path to **model collapse**. Step-level PRM rejection drops those traces early.

## Layout

```
mini-prm-rejection-sampler/
├── README.md
├── requirements.txt
├── config.py
├── data/seed_prompts.json
├── models/generator.py      # mock | HF | vLLM adapters
├── models/prm_scorer.py     # mock | HF PRM + ORM
├── pipeline/rejection_sampler.py
├── pipeline/verifier.py
├── analysis/plot_metrics.py
└── main.py
```

## Quick start (offline mock — no GPU)

```bash
cd code/mini-prm-rejection-sampler
python -m venv .venv && source .venv/bin/activate
pip install numpy matplotlib   # torch/transformers optional for mock path
python main.py
```

Outputs land in `outputs/metrics.json`, `outputs/selections.json`, and `outputs/prm_vs_orm_metrics.png`.

## Swap in real models

```bash
pip install -r requirements.txt
python main.py --generator-backend hf --prm-backend hf --model-name gpt2
# On CUDA + vLLM:
# pip install vllm
# python main.py --generator-backend vllm --model-name <your-model>
```

## Core API

`StepLevelRejectionSampler` draws `n` candidates per prompt, scores each step with a PRM, rejects if `min(step_scores) < threshold`, and compares against ORM outcome filtering on the same pool.
