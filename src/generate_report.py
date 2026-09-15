"""
Generates a weekly written report from pre-computed shipment delay statistics.
The AI only summarizes numbers calculated here in Python — it never calculates
anything itself, avoiding hallucinated statistics.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import date

load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")

# --- Pre-computed stats (from your notebooks — hardcoded here for this example run) ---
stats = {
    "overall_late_rate": 0.547,
    "first_class_late_rate": 1.00,
    "second_class_late_rate": 0.80,
    "standard_class_late_rate": 0.40,
    "same_day_late_rate": 0.00,
    "model_pr_auc": 0.843,
    "top_feature": "Days for shipment (scheduled)",
}

prompt = f"""You are a data analyst writing a short weekly ops report.
Using ONLY the numbers below, write a 3-4 paragraph plain-English summary
for a logistics manager. Do not invent, estimate, or calculate any numbers
beyond what is given. Be direct and specific.

Stats:
- Overall late-delivery rate: {stats['overall_late_rate']:.1%}
- First Class late rate: {stats['first_class_late_rate']:.1%}
- Second Class late rate: {stats['second_class_late_rate']:.1%}
- Standard Class late rate: {stats['standard_class_late_rate']:.1%}
- Same Day late rate: {stats['same_day_late_rate']:.1%}
- Prediction model PR-AUC: {stats['model_pr_auc']}
- Strongest predictive feature: {stats['top_feature']}
"""

response = model.generate_content(prompt)
report_text = response.text

output_path = f"reports/weekly_report_{date.today().isoformat()}.md"
with open(output_path, "w") as f:
    f.write(f"# Weekly Delay Report — {date.today().isoformat()}\n\n")
    f.write(report_text)

print(f"Report saved to {output_path}")