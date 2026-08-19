# Design Doc — Inbound Logistics Delay Root-Cause & Agentic Reporting System

> Fill this in yourself, in your own words. Each section has a prompt —
> delete the prompt once you've written your answer. This doc is what you'll
> paraphrase in an interview when someone asks "walk me through your project."

## 1. Problem statement
(2-3 sentences. Prompt: What specific business pain does this solve? Who
feels that pain? Why does it matter in dollars/time, not just "it's cool"?)

## 2. Who will use it
(Prompt: Name a specific persona — e.g. "an inbound planning manager who
currently spends 3 hours every Monday building a delay report by hand."
Specific personas answer well in interviews; vague ones don't.)

## 3. Scope
**In scope:**
-

**NOT in scope:**
- (Prompt: what are you deliberately NOT doing, and why? e.g. "Not
  predicting exact delay duration, only late/not-late — because duration
  prediction needs more granular data than this dataset has.")

## 4. Data sources
- DataCo Smart Supply Chain dataset (Kaggle) — [link]
- Open-Meteo API — weather data joined on shipment date/region
- `holidays` Python library — US holiday calendar joined on shipment date

(Prompt: for each source, note what it gives you and what's missing/messy
about it. You will thank yourself in Week 1.)

## 5. System diagram (text is fine, no need for fancy tools)
raw data (Kaggle CSV + weather API + holidays)
      |
   cleaning (fix dates, nulls, duplicates, define "late")
      |
   joined dataset
      |
   -----------------------------
   |             |             |
EDA/charts   delay-risk    dashboard
             model         (Tableau/PowerBI)
   |             |
   root-cause   feature
   findings     importance
        \         /
      weekly stats summary
             |
      LLM report generator
             |
      saved report (reports/)

## 6. Success metrics
(Prompt: be specific and measurable. Draft:
- Model: PR-AUC on time-split test set, beats a naive baseline by X%
- Root cause: top 3-5 delay drivers identified with supporting evidence
- Report automation: estimated hours saved per week vs. manual reporting
- Dashboard: publishable link, loads in under X seconds)

## 7. Risks
- **Data leakage**: features that wouldn't be known at ship-time (e.g.
  actual delivery date) must not be used to predict lateness.
- **Class imbalance**: most shipments are probably on-time, so accuracy
  is a misleading metric — use PR-AUC/recall instead.
- **AI hallucination**: the LLM must only summarize numbers you already
  computed — it must never be asked to calculate or invent a statistic.
- (Add any you find as you go — that's what DECISIONS.md is for.)
