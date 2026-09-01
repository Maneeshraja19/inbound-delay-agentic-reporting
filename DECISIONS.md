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

2025-08-25 — Converted order date and shipping date columns from text to real datetime type using pd.to_datetime(). Calculated actual_delay_days as (shipping date - order date). Result: min 0 days, max 6 days, mean 3.47 days, no negative values — confirms no shipped-before-ordered data errors. This will be compared against the 'Days for shipment (scheduled)' column to define what counts as "late."

2025-08-29 — Confirmed zero duplicate rows in the dataset. Defined is_late as actual_delay_days > Days for shipment (scheduled). Result: 98,743 late (55%) vs 81,776 on-time (45%) — reasonably balanced, reducing class imbalance risk for Week 3 modeling. Cross-checked against the dataset's own Late_delivery_risk column: ~95% agreement (171,845/180,519 rows), validating this definition. The ~5% disagreement will be investigated later but isn't blocking.

2025-08-31 — Investigated why First Class shows 100% late rate and Same Day shows 0%. Found the root cause: scheduled promise times are unrealistic for First Class (1 day promised vs 2 days actual) and Second Class (2 promised vs ~4 actual), while Standard Class's promise roughly matches reality (4 vs ~4). Same Day always shows 0 for both scheduled and actual, likely a data granularity artifact rather than genuinely perfect performance. This reframes the finding: for First/Second Class, the delivery promise itself appears to be the problem, not operational execution — a genuine root-cause insight, not just a chart artifact.
2025-09-01 — Checked delay rate by Order Region. Found a narrow spread (~51% to ~59% across all regions), unlike the sharp pattern seen in shipping mode. Conclusion: region is a comparatively weak driver of delay in this dataset — no single region stands out as a major outlier. Shipping mode remains the stronger lever so far.