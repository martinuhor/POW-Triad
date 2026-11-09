# refusal-vector-steering

Educational **mechanistic interpretability** demo: extract a difference-in-means **refusal vector** from a small open-weights model and orthogonally ablate it in the residual stream (TransformerLens).

## Framing (read this)

This repo is for **defensive safety research** — understanding how refusal is linearly represented in open weights, and what that implies for **post-exfiltration** risk if model weights leak. It is **not** an attack playbook. Prompt sets are stylized; swap in institutionally approved eval suites before any real study.

## Layout

```
refusal-vector-steering/
├── README.md
├── requirements.txt
├── notebooks/refusal_ablation_demo.ipynb
├── src/activation_harvest.py
├── src/vector_compute.py
├── src/weight_steering.py
└── eval/benchmark_refusal.py
```

## Offline check (no GPU / no weights)

```bash
cd code/refusal-vector-steering
python -m venv .venv && source .venv/bin/activate
pip install numpy
python eval/benchmark_refusal.py --mock
```

## Full TransformerLens path

```bash
pip install -r requirements.txt
python eval/benchmark_refusal.py --model gpt2-small --layer 6 --device cpu
# Or a 1–3B chat model supported by TransformerLens, e.g.:
# python eval/benchmark_refusal.py --model Qwen/Qwen2.5-1.5B-Instruct --layer 14 --device cuda
```

Open `notebooks/refusal_ablation_demo.ipynb` and set `MODEL_NAME` / `LAYER` at the top.
