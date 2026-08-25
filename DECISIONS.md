# Decisions Log

One line per decision, in the order you make them. This is your proof, later,
that you made deliberate engineering trade-offs instead of just following a
tutorial. Recruiters and interviewers respond well to this file specifically.

Format: `YYYY-MM-DD — decision — why`

---

2025-08-17 — Chose DataCo Smart Supply Chain dataset over a synthetic dataset — real-world data has genuine messiness (nulls, inconsistent formats) that's more defensible in an interview than data I generated myself.

2025-08-17 — Excluded actual delivery date from model features — using it would leak the answer into the prediction (we only know it after the shipment is already late or not).

2025-08-21 — Downloaded DataCo Smart Supply Chain dataset from Kaggle, placed in data/ (git-ignored) — this is the primary dataset for delay analysis; not committed to Git per data-hosting best practice.

2025-08-24 — First look at dataset: confirmed it loads with latin-1 encoding, 180,519 rows and 53 columns. Noticed a 'Late_delivery_risk' column — likely target variable for Week 3's model. Logging encoding fix now so tomorrow's cleaning notebook starts from a known-working read.
