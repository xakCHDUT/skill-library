"""Recompute author-case arithmetic and record invariants from supplied inputs.

This checks selected authored artifacts, not model reliability or returns.
"""

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHECKS = []


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def close(actual, expected):
    if expected is None:
        return actual is None
    return isinstance(actual, (int, float)) and math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-8)


def check(name, condition):
    CHECKS.append({"name": name, "passed": bool(condition)})


def inspect(name):
    raw = read(f"cases/{name}.json")
    before = read(f"author-responses/{name}.before.json")
    after = read(f"author-responses/{name}.after.json")
    update = after["updates"][-1]
    sources = {s["id"]: s for s in raw["sources"]}
    check(f"{name}: synthetic company and values stay labeled", raw["synthetic"] and before["synthetic"] and after["synthetic"] and before["company"] == raw["company"] == after["company"])
    check(f"{name}: original thesis and forecasts unchanged", before["baseline"] == after["baseline"] and after["baseline"]["forecasts"][0]["values"] == raw["original_forecast"])
    check(f"{name}: updates append without rewriting previous entries", len(after["updates"]) == len(before["updates"]) + 1 and after["updates"][:-1] == before["updates"])
    check(f"{name}: sources retained without fabricated providers", after["sources"] == raw["sources"] and all(s in after["sources"] for s in before["sources"]))
    check(f"{name}: evidence is available at the historical cutoff", all(e["event_date"] <= e["published_at"] <= update["information_cutoff"] <= update["recorded_at"] and e["published_at"] == sources[e["source_id"]]["published_at"] for e in update["evidence"]))
    check(f"{name}: actual evidence equals supplied raw facts", update["evidence"][0]["fact"] == raw["actual"])
    check(f"{name}: prior conviction kept and no unsupported valuation/action", update["prior_conviction"] == before["baseline"]["conviction"] and update["investment_action"] is None and update["valuation"] is None and before["baseline"]["valuation"] is None)
    check(f"{name}: unknowns remain explicit", update["data_gaps"] == raw["unknowns"] and all(t["expected_date"] is None for t in update["next_tests"]))
    for row in update["comparisons"]:
        metric = row["metric"]
        actual = raw["actual"][metric]
        prior = raw["prior_year"][metric]
        forecast = raw["original_forecast"].get(metric)
        expected = {
            "actual": actual, "prior_year_actual": prior, "original_forecast": forecast,
            "yoy_absolute": actual - prior,
            "yoy_percent": (actual / prior - 1) * 100 if prior > 0 else None,
            "forecast_difference_absolute": actual - forecast if forecast is not None else None,
            "forecast_difference_percent": (actual / forecast - 1) * 100 if forecast is not None and forecast > 0 else None,
        }
        check(f"{name}: {metric} raw values and all comparisons recomputed", all(close(row[key], value) for key, value in expected.items()))
        check(f"{name}: {metric} period, units and sources traceable", row["unit"] == raw["unit"] and row["actual_source_id"] in sources and row["prior_source_id"] in sources and (row["forecast_source_id"] in sources if forecast is not None else row["forecast_source_id"] is None) and (row["period"] == "2026-03-31 vs 2025-03-31" if metric == "inventory" else row["period"] == "2026 Q1 vs 2025 Q1"))
    evidence = {e["id"]: e for e in update["evidence"]}
    pillar_ids = {p["id"] for p in before["baseline"]["pillars"]}
    check(f"{name}: every original pillar reviewed against relevant evidence", {r["pillar_id"] for r in update["scorecard"]} == pillar_ids and all(all(r["pillar_id"] in evidence[e]["pillar_ids"] for e in r["evidence_ids"]) for r in update["scorecard"]))
    return raw, update


def main():
    a, au = inspect("cash-versus-profit")
    ad = au["derived"]
    actual_ratio = a["actual"]["operating_cash_flow"] / a["actual"]["net_profit"]
    prior_ratio = a["prior_year"]["operating_cash_flow"] / a["prior_year"]["net_profit"]
    check("cash case: cash conversion ratios and percentage-point decline", close(ad["cash_conversion_current"], actual_ratio) and close(ad["cash_conversion_prior"], prior_ratio) and close(ad["cash_conversion_change_percentage_points"], (actual_ratio - prior_ratio) * 100))
    inventory_limit = a["prior_year"]["inventory"] * (1 + a["thresholds"]["inventory_yoy_max_percent"] / 100)
    check("cash case: inventory threshold remains an original limit, not an invented forecast", close(ad["inventory_threshold_amount"], inventory_limit) and close(ad["inventory_excess_above_threshold"], a["actual"]["inventory"] - inventory_limit) and "inventory" not in a["original_forecast"])
    check("cash case: mixed evidence weakens the overall view", [r["status"] for r in au["scorecard"]] == ["supported", "weakened", "weakened"] and au["thesis_status"] == "weakened" and au["current_conviction"] == "low")

    b, bu = inspect("positive-earnings-refuted-thesis")
    bd = bu["derived"]
    check("refutation case: one-off and core profit reconcile", bd["reported_profit_bridge"] == {k: b["actual"][k] for k in ["core_net_profit", "after_tax_disposal_gain", "net_profit"]} and bd["reported_profit_bridge"]["core_net_profit"] + bd["reported_profit_bridge"]["after_tax_disposal_gain"] == bd["reported_profit_bridge"]["net_profit"] and close(bd["disposal_share_of_reported_net_profit_percent"], b["actual"]["after_tax_disposal_gain"] / b["actual"]["net_profit"] * 100))
    check("refutation case: zero-baseline gain is absolute rather than infinite growth", next(r for r in bu["comparisons"] if r["metric"] == "after_tax_disposal_gain")["yoy_percent"] is None and next(r for r in bu["comparisons"] if r["metric"] == "after_tax_disposal_gain")["yoy_percent_reason"])
    check("refutation case: retention changes are percentage points", close(bd["gross_customer_retention_change_percentage_points"], b["actual"]["gross_customer_retention_percent"] - b["prior_year"]["gross_customer_retention_percent"]) and close(bd["retention_gap_to_threshold_percentage_points"], b["actual"]["gross_customer_retention_percent"] - b["thresholds"]["gross_customer_retention_min_percent"]))
    check("refutation case: price context is sourced but proves no operating pillar", close(bd["market_price_change_percent"], (b["market_context"]["end_price"] / b["market_context"]["start_price"] - 1) * 100) and bu["evidence"][1]["fact"] == b["market_context"] and bu["evidence"][1]["pillar_ids"] == [] and all("B-E2" not in r["evidence_ids"] for r in bu["scorecard"]))
    check("refutation case: invalidation outweighs near-term profit beat", b["actual"]["net_profit"] > b["original_forecast"]["net_profit"] and b["actual"]["gross_customer_retention_percent"] < b["thresholds"]["gross_customer_retention_min_percent"] and [r["status"] for r in bu["scorecard"]] == ["weakened", "refuted", "weakened"] and bu["thesis_status"] == "refuted" and bu["current_conviction"] == "low")

    for rel, expected in {
        "upstream/SKILL.md": "f9a3ce9187bdc3410d3f4f3713ce70a6f6b8f221",
        "upstream/LICENSE": "d645695673349e3947e8e5ae42332d0ac3164cd7",
    }.items():
        data = (ROOT / rel).read_bytes()
        git_blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        check(f"source: {rel} matches fixed upstream Git blob", git_blob == expected)
    check("license: staged license matches source byte for byte", (ROOT.parent.parent / "skills/thesis-tracker/LICENSE").read_bytes() == (ROOT / "upstream/LICENSE").read_bytes())
    result = {"date": "2026-10-15", "scope": "author_self_check", "cases": 2,
              "passed": sum(c["passed"] for c in CHECKS), "failed": sum(not c["passed"] for c in CHECKS),
              "checks": CHECKS,
              "not_tested": ["independent agent behavior", "live company or market data", "investment returns", "broker execution", "full portfolio workflow"]}
    (ROOT / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{result['passed']} passed, {result['failed']} failed; author self-check only.")
    for item in CHECKS:
        if not item["passed"]:
            print("FAIL:", item["name"])
    raise SystemExit(1 if result["failed"] else 0)


if __name__ == "__main__":
    main()
