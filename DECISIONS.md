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

2025-09-01 — Checked delay rate by month. Found a narrow range (~54.1% to ~55.5%) across all 12 months — note the chart's y-axis auto-scaled to this tight range, which visually exaggerates the swings. There's a mild uptick toward year-end (Aug-Dec) that could hint at holiday-season pressure, but the effect is weak and not strong enough to treat as a confirmed driver. Shipping mode remains the clearest, strongest root cause found so far.

2025-09-11 — Exported a clean, focused dashboard_data.csv (12 columns) from the full 53-column raw dataset, rather than connecting the dashboard directly to raw data — includes calculated fields (is_late, order_month, actual_delay_days) so Power BI doesn't need to recompute business logic that's already validated in the notebook.

2025-09-11 — Built first Power BI dashboard visuals: overall late-delivery rate card (55%) and late-rate-by-shipping-mode bar chart. Cross-checked against notebook calculations — numbers match exactly, confirming the dashboard is reading the same validated logic (is_late) correctly rather than recalculating it independently.

2025-09-16 — Found Order State has 1,089 unique values, causing one-hot encoding to explode from 9 to 1,330 columns. Dropped Order State from features, keeping Order Region (23) and Order Country (164) for geographic signal — a trade-off between granularity and having enough examples per category for the model to learn from.

2025-09-16 — Trained baseline Logistic Regression model on 241 leak-free features (241 one-hot encoded columns after dropping high-cardinality Order State). Time-based 80/20 split. Result: PR-AUC 0.842 (vs ~0.55 naive baseline) — strong predictive signal. Classification report shows high precision (0.87) but moderate recall (0.57) for the 'late' class, meaning the model is conservative — when it flags a shipment as risky it's usually right, but it misses some late shipments. Next: try XGBoost to see if it improves recall without sacrificing precision.

2025-09-16 — Trained XGBoost (100 estimators, max_depth 5) on same features/split as Logistic Regression baseline. Result: PR-AUC 0.843 vs Logistic Regression's 0.842 — essentially no improvement. Classification report nearly identical. Conclusion: the added complexity of XGBoost isn't justified here — the underlying delay pattern appears fairly linear/simple, consistent with Week 1's finding that a single strong driver (Shipping Mode's unrealistic scheduling) dominates. Choosing to keep both results and report this honestly rather than force a narrative that the more complex model "won."

2025-09-16 — Generated XGBoost feature importance chart. Days for shipment (scheduled) overwhelmingly dominates all other features combined (~15-20x larger importance than the next highest). This independently confirms Week 1's manual finding that the shipping promise itself — not geography, product category, or season — is the primary driver of lateness. Also explains why XGBoost barely outperformed Logistic Regression: with one dominant, near-linear feature, the added model complexity wasn't needed.

2025-09-15 — Built generate_report.py script that turns pre-computed weekly stats into an AI-written report. Switched from Anthropic API to Google Gemini API (gemini-3.6-flash) since Gemini offers a free tier and Anthropic required paid credit — a deliberate choice to avoid a paid dependency for a portfolio project. The prompt explicitly instructs the model to only summarize provided numbers, never calculate or invent statistics. First report generated successfully and saved to reports/.

2025-09-18 — Built and deployed a live, public interactive dashboard using Streamlit and Streamlit Community Cloud, going beyond the original plan (Power BI was free-tier-limited to local viewing only). Fixed a .gitignore bug along the way: data/ (with trailing slash) excludes the whole folder as a unit, preventing Git from checking exception rules inside it — changed to data/* to allow dashboard_data.csv through while still excluding the raw Kaggle dataset.

2025-09-18 — Added a live prediction form to the Streamlit dashboard, letting users input shipment details (shipping mode, region, country, category, scheduled days, month) and get a real-time late/on-time prediction from the trained XGBoost model. Saved the trained model and feature list via joblib so the app can load them without retraining. Tested with First Class + realistic 4-day schedule (vs the unrealistic 1-day default) — correctly predicted on-time, confirming the model learned the true promise-vs-reality relationship rather than a naive "First Class = always late" shortcut.
