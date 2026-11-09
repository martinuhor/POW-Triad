# Task Macro GDP Simulator

Interactive Streamlit app implementing a **Daron Acemoglu–style task-based** macroeconomic framework.

## Features

- Sliders for **task exposure %**, **cost savings** (easy vs hard), and **hard-vs-easy proportions**
- Adoption half-lives for easy / hard tasks
- Physical capital / deployment drag vs pure digital R&D path
- Predicted **10-year TFP and GDP** index curves

## Run locally

```bash
cd simulators/task-macro-gdp-simulator
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Upload `app.py` + `requirements.txt` to a Hugging Face Space (Streamlit SDK).
