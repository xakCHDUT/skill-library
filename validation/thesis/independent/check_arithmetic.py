"""Recompute the eight comparison rows captured in this single forward exercise.

Raw inputs are transcribed from task.md, not extracted from the model answer.
This checks arithmetic, not general investment judgment or model reliability.
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
record = json.loads((HERE / "record.json").read_text(encoding="utf-8"))
rows = {row["id"]: row for row in record["updates"][0]["comparisons"]}
revenue, prior_revenue, forecast_revenue = 330, 300, 300
profit, prior_profit, forecast_profit, nonrecurring = 33, -5, 25, 40
cash_flow, margin, prior_margin, forecast_margin = -12, 19, 21, 20
expected = {
    "C1": (revenue, prior_revenue, revenue - prior_revenue, (revenue / prior_revenue - 1) * 100),
    "C2": (revenue, forecast_revenue, revenue - forecast_revenue, (revenue / forecast_revenue - 1) * 100),
    "C3": (profit, prior_profit, profit - prior_profit, None),
    "C4": (profit, forecast_profit, profit - forecast_profit, (profit / forecast_profit - 1) * 100),
    "C5": (profit - nonrecurring, 0, profit - nonrecurring, None),
    "C6": (cash_flow, profit, cash_flow - profit, None),
    "C7": (margin, prior_margin, margin - prior_margin, None),
    "C8": (margin, forecast_margin, margin - forecast_margin, None),
}
checks = []
for row_id, values in expected.items():
    row = rows[row_id]
    actual = tuple(row.get(k) for k in ("actual", "baseline", "absolute_difference", "relative_difference_percent"))
    passed = all(a is None if b is None else isinstance(a, (int, float)) and math.isclose(a, b, abs_tol=1e-9)
                 for a, b in zip(actual, values))
    if row_id in ("C7", "C8"):
        passed = passed and row.get("difference_unit") == "percentage_points"
    checks.append({"row": row_id, "passed": passed, "recomputed": list(values), "captured": list(actual)})

result = {"scope": "eight numeric comparison rows in one independent synthetic task", "passed": sum(c["passed"] for c in checks), "failed": sum(not c["passed"] for c in checks), "checks": checks}
(HERE / "numerical-checks.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in result.items() if k != "checks"}, ensure_ascii=False))
raise SystemExit(1 if result["failed"] else 0)
