# Decisions Log

One line per decision, in the order you make them. This is your proof, later,
that you made deliberate engineering trade-offs instead of just following a
tutorial. Recruiters and interviewers respond well to this file specifically.

Format: `YYYY-MM-DD — decision — why`

---

2025-08-17 — Chose DataCo Smart Supply Chain dataset over a synthetic dataset — real-world data has genuine messiness (nulls, inconsistent formats) that's more defensible in an interview than data I generated myself.

2025-08-17 — Excluded actual delivery date from model features — using it would leak the answer into the prediction (we only know it after the shipment is already late or not).

