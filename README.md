# Inbound Logistics Delay Root-Cause & Agentic Reporting System

> Status: 🚧 Week 1 — data cleaning in progress

## Problem
*(Fill in from docs/design.md Section 1 once written.)*

## Live dashboard
*(Link goes here once published in Week 2.)*

## Approach
1. Cleaned and joined DataCo shipment data with weather (Open-Meteo) and US holiday data
2. Identified top delay drivers through exploratory analysis
3. Built a time-split delay-risk classifier (logistic regression → XGBoost), evaluated on PR-AUC
4. Built an AI agent that turns the week's computed stats into a written report — it summarizes numbers, it does not calculate them

## Key findings
*(Fill in with real numbers once Week 2-3 are done. This is the section
recruiters actually read — be specific: "Late shipments cluster on X carrier
with a Y% higher rate than average" beats "found some interesting patterns.")*

## Repo structure
```
data/       # not committed — see "Getting the data" below
notebooks/  # exploratory analysis, model development
src/        # reusable cleaning/modeling/reporting scripts
docs/       # design.md, decisions log
reports/    # example AI-generated weekly reports
```

## Getting the data
1. Download the DataCo Smart Supply Chain dataset from Kaggle: *(link)*
2. Place the CSV in `data/`
3. Run `notebooks/01_cleaning.ipynb` to reproduce the cleaned dataset

## Setup
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then add your API key
```

## Design decisions
See `docs/design.md` for the full design doc and `DECISIONS.md` for a
running log of trade-offs made along the way.

## Resume bullet
*(Write this last, once you have real measured numbers. Draft placeholder:
"Built a shipment delay root-cause and risk-prediction system with an AI
agent that auto-generates weekly ops reports, identifying top delay drivers
and achieving [X] PR-AUC on a held-out test set.")*
