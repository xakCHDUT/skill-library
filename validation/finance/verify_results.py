#!/usr/bin/env python3
"""Check synthetic finance outputs; no network, account, or third-party library.

This verifies numerical and evidence-boundary assertions in structured outputs.
It does not establish model quality, independent agent performance, or investment
returns. The supplied self-check results were written by the skill adapter.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", default="self-check-results")
    parser.add_argument("--output", default="verification.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    results = root / args.results
    checks = []

    def check(name, passed):
        checks.append({"assertion": name, "passed": bool(passed)})

    def near(name, observed, expected):
        check(name, isinstance(observed, (int, float)) and
              math.isclose(observed, expected, rel_tol=1e-10, abs_tol=1e-10))

    case = read_json(root / "cases/model-update.json")
    result = read_json(results / "model-update.json")
    prior = case["old_forecast"]
    assumed = case["explicit_assumptions"]
    actual = case["new_actuals"]["Q2"]
    computed = {"Q1": prior["Q1"], "Q2": actual}
    for quarter in ("Q3", "Q4"):
        revenue = prior[quarter]["revenue"] * (1 + assumed[quarter + "_revenue_change_from_old"])
        computed[quarter] = {
            "revenue": revenue,
            "ebitda": revenue * assumed[quarter + "_ebitda_margin"],
            "net_income_attributable": assumed[quarter + "_net_income_attributable"],
        }
    for quarter, values in computed.items():
        for metric in ("revenue", "ebitda", "net_income_attributable"):
            near(f"model: {quarter} {metric}", result["new_forecast"][quarter][metric], values[metric])
        expected_class = "reported_actual" if quarter in ("Q1", "Q2") else "derived_from_explicit_assumptions"
        check(f"model: {quarter} actual/assumption boundary", result["new_forecast"][quarter]["classification"] == expected_class)
        check(f"model: {quarter} only supplied source IDs", set(result["new_forecast"][quarter]["sources"]).issubset(case["sources"]))

    for metric in ("revenue", "ebitda", "net_income_attributable"):
        old = sum(prior[q][metric] for q in prior)
        new = sum(computed[q][metric] for q in computed)
        near(f"model: old annual {metric}", result["annual"]["old"][metric], old)
        near(f"model: new annual {metric}", result["annual"]["new"][metric], new)
        near(f"model: annual {metric} change %", result["annual"]["change_pct"][metric], (new / old - 1) * 100)
    shares = assumed["fy_weighted_average_diluted_shares_old_and_new"]
    for period in ("old", "new"):
        eps = result["annual"][period]["net_income_attributable"] / shares
        near(f"model: {period} EPS with correct units", result["annual"][period]["eps"], eps)
        near(f"model: {period} conditional PE value", result["valuation"][period + "_implied_value_per_share"], eps * assumed["unchanged_pe_scenario_multiple"])
    new_margin = result["annual"]["new"]["ebitda"] / result["annual"]["new"]["revenue"]
    old_margin = result["annual"]["old"]["ebitda"] / result["annual"]["old"]["revenue"]
    near("model: annual EBITDA margin %", result["annual"]["new_ebitda_margin_pct"], new_margin * 100)
    near("model: annual margin change in pp", result["annual"]["margin_change_pp"], (new_margin - old_margin) * 100)
    near("model: Q2 margin change in pp", result["quarter_actual_comparison"]["ebitda_margin_change_pp"], (actual["ebitda"] / actual["revenue"] - prior["Q2"]["ebitda"] / prior["Q2"]["revenue"]) * 100)
    for field in ("current_price", "upside_pct", "dcf_value", "consensus_comparison", "investment_rating"):
        check("model: unavailable " + field, result["valuation"][field] is None)
    check("model: missing FY2027 not invented", result["fy2027_forecast"] is None)
    check("model: no false workbook update claim", result["workbook_updated"] is False)

    edge_case = read_json(root / "cases/model-update-edge.json")
    edge = read_json(results / "model-update-edge.json")
    for metric, output in (("revenue", "revenue_delta"), ("net_income_attributable", "net_income_delta")):
        near("edge: " + output, edge[output], edge_case["reported_quarter_actual"][metric] - edge_case["old_quarter_estimate"][metric])
    for field in ("revenue_change_pct", "net_income_change_pct", "eps", "price_target", "upside_pct", "consensus_comparison", "full_year_forecast"):
        check("edge: unsupported " + field, edge[field] is None)

    sector_case = read_json(root / "cases/sector-overview.json")
    sector = read_json(results / "sector-overview.json")
    companies = {x["id"]: x for x in sector_case["companies"]}
    eligible = [x["id"] for x in sector_case["companies"] if x["revenue_scope"].startswith("in_scope")]
    sample = sum(companies[x]["revenue"] for x in eligible)
    check("sector: compatible revenue universe", sector["eligible_revenue_peers"] == eligible)
    check("sector: unrelated group excluded", sector["excluded_group_revenue_peer"] == "C")
    near("sector: sample total is not a market estimate", sector["sample_revenue_total"], sample)
    for field in ("market_size", "market_shares", "industry_leader", "concentration_ratio", "valuation_ranking", "growth_rate"):
        check("sector: unavailable " + field, sector[field] is None)
    for company in ("A", "B"):
        near("sector: EBITDA margin " + company, sector["ebitda_margin_pct"][company], companies[company]["ebitda"] / companies[company]["revenue"] * 100)
    check("sector: gross margin not reclassified as EBITDA", sector["ebitda_margin_pct"]["D"] is None and sector["D_gross_margin_pct"] == 30)
    check("sector: unsupported delivery claim not verified", sector["A_fast_delivery_claim_verified"] is False)

    known_case = read_json(root / "cases/sector-overview-denominator.json")
    known = read_json(results / "sector-overview-denominator.json")
    market = known_case["additional_source"]
    total = market["FY2025_total_market_revenue"]
    near("known denominator: two-year CAGR", known["cagr_2023_2025_pct"], (math.sqrt(total / market["FY2023_total_market_revenue"]) - 1) * 100)
    check("known denominator: year intervals", known["year_intervals"] == 2)
    for company in eligible:
        near("known denominator: market share " + company, known["market_share_pct"][company], companies[company]["revenue"] / total * 100)
    near("known denominator: sample coverage", known["sample_coverage_pct"], sample / total * 100)
    near("known denominator: unassigned revenue", known["unassigned_market_revenue"], total - sample)
    check("known denominator: missing segment stays missing", known["market_share_pct"]["C"] is None)
    for field in ("industry_leader", "concentration_ratio", "valuation_ranking"):
        check("known denominator: still unsupported " + field, known[field] is None)

    for name, item in (("model", result), ("edge", edge), ("sector", sector), ("known", known)):
        check(name + ": synthetic label preserved", item["synthetic"] is True)

    manifest = read_json(root / "upstream-manifest.json")
    for entry in manifest["files"]:
        data = (root / "upstream" / entry["path"]).read_bytes()
        blob_hash = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
        check("upstream exact bytes: " + entry["path"], blob_hash == entry["git_blob_sha"])

    report = {
        "evaluation_role": "author_self_check_with_deterministic_arithmetic_and_boundary_checks",
        "independent_agent_evaluation": False,
        "external_financial_data_used": False,
        "investment_performance_backtest": False,
        "assertion_count": len(checks),
        "passed": sum(x["passed"] for x in checks),
        "failed": sum(not x["passed"] for x in checks),
        "checks": checks,
    }
    (root / args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "checks"}, ensure_ascii=True))
    return 0 if not report["failed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
