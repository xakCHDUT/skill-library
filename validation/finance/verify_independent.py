#!/usr/bin/env python3
"""Grade the independent outputs directly; absent or mistyped fields fail.

No normalization, default conclusions, rewritten output, network, or third-party
dependencies. Numerical oracles are computed from the original case inputs.
Qualitative memo review is recorded separately in qualitative-review.json.
"""
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MISSING = object()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    checks = []
    documents = {}
    case_name = ""

    def observed(document, path):
        value = document
        for part in path.split("."):
            if not isinstance(value, dict) or part not in value:
                return MISSING
            value = value[part]
        return value

    def record(path, passed, note=""):
        checks.append({"case": case_name, "field": path, "passed": bool(passed), "note": note})

    def equal(document, path, expected):
        value = observed(document, path)
        record(path, value is not MISSING and type(value) is type(expected) and value == expected,
               "Required field missing" if value is MISSING else "Direct comparison; no default value")

    def near(document, path, expected):
        value = observed(document, path)
        passed = type(value) in (int, float) and math.isfinite(value) and math.isclose(value, expected, rel_tol=1e-10, abs_tol=1e-10)
        record(path, passed, "Required field missing" if value is MISSING else "Arithmetic recomputed from supplied inputs")

    def load_case(filename):
        data = read_json(ROOT / "cases" / filename)
        response_path = ROOT / "independent-results" / filename
        response = read_json(response_path)
        documents[filename] = hashlib.sha256(response_path.read_bytes()).hexdigest()
        memo = response_path.with_suffix(".md")
        documents[memo.name] = hashlib.sha256(memo.read_bytes()).hexdigest()
        return data, response

    case_name = "model-update-quarterly"
    case, result = load_case("model-update.json")
    equal(result, "case_id", case["case_id"])
    equal(result, "synthetic", True)
    equal(result, "information_cutoff", case["information_cutoff"])
    prior, actual, assumptions = case["old_forecast"], case["new_actuals"]["Q2"], case["explicit_assumptions"]
    for metric in ("revenue", "ebitda", "net_income_attributable"):
        old, new = prior["Q2"][metric], actual[metric]
        prefix = "q2_actual_vs_estimate." + metric + "."
        for key, number in (("old_estimate", old), ("reported_actual", new), ("change", new-old), ("change_pct", (new/old-1)*100)):
            near(result, prefix+key, number)
    for metric, label in (("ebitda", "ebitda_margin"), ("net_income_attributable", "net_income_margin")):
        old_margin = prior["Q2"][metric] / prior["Q2"]["revenue"] * 100
        new_margin = actual[metric] / actual["revenue"] * 100
        for key, number in (("old_pct", old_margin), ("actual_pct", new_margin), ("change_pp", new_margin-old_margin)):
            near(result, "q2_actual_vs_estimate."+label+"."+key, number)
    computed = {"Q1": prior["Q1"], "Q2": actual}
    for quarter in ("Q3", "Q4"):
        revenue = prior[quarter]["revenue"] * (1+assumptions[quarter+"_revenue_change_from_old"])
        computed[quarter] = {"revenue": revenue, "ebitda": revenue*assumptions[quarter+"_ebitda_margin"], "net_income_attributable": assumptions[quarter+"_net_income_attributable"]}
    for quarter, values in computed.items():
        for metric in ("revenue", "ebitda", "net_income_attributable"):
            near(result, "quarterly_new."+quarter+"."+metric, values[metric])
            near(result, "revision_bridge."+quarter+"."+metric+"_change", values[metric]-prior[quarter][metric])
        equal(result, "quarterly_new."+quarter+".classification", "reported_actual" if quarter in ("Q1", "Q2") else "forecast_from_explicit_assumptions")
    annual = {}
    for period, quarters in (("old", prior), ("new", computed)):
        annual[period] = {metric: sum(quarters[q][metric] for q in quarters) for metric in ("revenue", "ebitda", "net_income_attributable")}
        annual[period]["weighted_average_diluted_shares"] = assumptions["fy_weighted_average_diluted_shares_old_and_new"]
        annual[period]["eps"] = annual[period]["net_income_attributable"] / annual[period]["weighted_average_diluted_shares"]
        annual[period]["ebitda_margin_pct"] = annual[period]["ebitda"] / annual[period]["revenue"] * 100
        annual[period]["net_income_margin_pct"] = annual[period]["net_income_attributable"] / annual[period]["revenue"] * 100
        for metric, number in annual[period].items():
            near(result, "fy2026."+period+"."+metric, number)
    for metric in ("revenue", "ebitda", "net_income_attributable", "eps"):
        old, new = annual["old"][metric], annual["new"][metric]
        near(result, "fy2026.change."+metric, new-old)
        near(result, "fy2026.change."+metric+"_pct", (new/old-1)*100)
    for metric in ("ebitda", "net_income"):
        near(result, "fy2026.change."+metric+"_margin_pp", annual["new"][metric+"_margin_pct"]-annual["old"][metric+"_margin_pct"])
    equal(result, "fy2026.shares_classification", "constant_explicit_assumption")
    equal(result, "guidance.classification", "company_forecast_not_actual")
    near(result, "guidance.revenue_min", 1150)
    near(result, "guidance.revenue_max", 1250)
    equal(result, "guidance.revised_revenue_within_range", 1150 <= annual["new"]["revenue"] <= 1250)
    near(result, "guidance.above_lower_bound", annual["new"]["revenue"]-1150)
    near(result, "guidance.below_upper_bound", 1250-annual["new"]["revenue"])
    multiple = assumptions["unchanged_pe_scenario_multiple"]
    old_value, new_value = annual["old"]["eps"]*multiple, annual["new"]["eps"]*multiple
    equal(result, "pe_valuation.classification", "conditional_scenario")
    for key, number in (("multiple_explicit_assumption", multiple), ("prior_value", old_value), ("revised_value", new_value), ("change", new_value-old_value), ("change_pct", (new_value/old_value-1)*100)):
        near(result, "pe_valuation."+key, number)
    equal(result, "pe_valuation.upside_to_current_price", None)
    for key in ("current_share_price", "consensus_eps", "fy2027_forecast", "dcf_value", "ev_based_value", "investment_rating", "segment_reconciliation", "capital_expenditure", "working_capital", "nonrecurring_items"):
        equal(result, "unavailable."+key, None)
    balance = case["reported_balance_sheet"]
    for key, number in (("cash_reported", balance["cash"]), ("debt_reported", balance["debt"]), ("net_cash_derived", balance["cash"]-balance["debt"]), ("net_debt_derived", balance["debt"]-balance["cash"])):
        near(result, "balance_sheet."+key, number)
    equal(result, "balance_sheet.statement_date", None)
    equal(result, "balance_sheet.prior_balance_changes", None)
    equal(result, "workbook_updated", False)
    for key, source in (("prior_estimates", "OLD"), ("reported_actuals", "ACT"), ("explicit_assumptions", "ASSUMPTIONS"), ("revenue_guidance", "GUIDANCE")):
        equal(result, "sources."+key, source)

    case_name = "model-update-zero-and-missing"
    case, result = load_case("model-update-edge.json")
    equal(result, "case_id", case["case_id"])
    equal(result, "synthetic", True)
    equal(result, "source", "EDGE")
    equal(result, "information_cutoff", case["information_cutoff"])
    for metric in ("revenue", "net_income_attributable"):
        old, new = case["old_quarter_estimate"][metric], case["reported_quarter_actual"][metric]
        for key, number in (("old_estimate", old), ("reported_actual", new), ("absolute_change", new-old)):
            near(result, metric+"."+key, number)
        equal(result, metric+".change_pct", None)
        equal(result, metric+".yoy_growth_pct", None)
    equal(result, "revenue.change_pct_status", "undefined_zero_denominator")
    equal(result, "net_income_attributable.change_pct_status", "not_meaningful_due_to_sign_change")
    equal(result, "net_income_attributable.interpretation", "loss_to_profit")
    near(result, "net_income_margin.actual_pct", case["reported_quarter_actual"]["net_income_attributable"] / case["reported_quarter_actual"]["revenue"] * 100)
    for path in ("net_income_margin.old_pct", "net_income_margin.change_pp", "weighted_average_diluted_shares", "old_eps", "actual_eps", "target_multiple", "target_price", "current_share_price", "upside_pct", "consensus", "future_quarters", "full_year_forecast", "investment_rating"):
        equal(result, path, None)
    equal(result, "workbook_updated", False)

    case_name = "sector-overview-denominator-missing"
    case, result = load_case("sector-overview.json")
    equal(result, "case_id", case["case_id"])
    equal(result, "synthetic", True)
    companies = {item["id"]: item for item in case["companies"]}
    eligible = [item["id"] for item in case["companies"] if item["revenue_scope"].startswith("in_scope")]
    sample = sum(companies[x]["revenue"] for x in eligible)
    equal(result, "comparable_sample.members", eligible)
    near(result, "comparable_sample.revenue_sum", sample)
    near(result, "comparable_sample.share_denominator", sample)
    equal(result, "comparable_sample.share_type", "sample_share_not_market_share")
    equal(result, "comparable_sample.is_total_market_size", False)
    for name in eligible:
        near(result, "companies."+name+".in_scope_revenue", companies[name]["revenue"])
        near(result, "companies."+name+".derived_sample_share_pct", companies[name]["revenue"]/sample*100)
        equal(result, "companies."+name+".market_share_pct", None)
    for name in ("A", "B"):
        near(result, "companies."+name+".reported_ebitda", companies[name]["ebitda"])
        near(result, "companies."+name+".derived_ebitda_margin_pct", companies[name]["ebitda"]/companies[name]["revenue"]*100)
    near(result, "comparable_sample.a_minus_b_ebitda_margin_pp", (60/300-40/250)*100)
    near(result, "companies.C.group_revenue", companies["C"]["revenue"])
    near(result, "companies.C.group_ebitda", companies["C"]["ebitda"])
    near(result, "companies.C.derived_group_ebitda_margin_pct", companies["C"]["ebitda"]/companies["C"]["revenue"]*100)
    equal(result, "companies.C.included_in_comparable_sample", False)
    for path in ("companies.C.in_scope_revenue", "companies.C.in_scope_ebitda", "companies.C.market_share_pct", "companies.D.ebitda", "companies.D.ebitda_margin_pct"):
        equal(result, path, None)
    near(result, "companies.D.reported_gross_margin_pct", companies["D"]["gross_margin"]*100)
    near(result, "companies.D.derived_gross_profit", companies["D"]["gross_margin"]*companies["D"]["revenue"])
    equal(result, "companies.A.delivery_claim_verified", False)
    equal(result, "companies.B.customer_retention", None)
    for name in companies:
        equal(result, "companies."+name+".source", name)
    for path in ("total_market_size", "market_leader", "concentration_ratio", "growth_pct", "cagr_pct", "valuation_ranking", "stock_return_ranking"):
        equal(result, path, None)
    equal(result, "market_leader_proven", False)

    case_name = "sector-overview-known-denominator"
    case, result = load_case("sector-overview-denominator.json")
    equal(result, "case_id", case["case_id"])
    equal(result, "synthetic", True)
    market = case["additional_source"]
    old, new = market["FY2023_total_market_revenue"], market["FY2025_total_market_revenue"]
    equal(result, "market.source", "MARKET")
    equal(result, "market.classification", "synthetic_historical_census")
    for key, number in (("FY2023_revenue", old), ("FY2025_revenue", new), ("absolute_growth", new-old), ("cumulative_growth_pct", (new/old-1)*100), ("annual_intervals", 2), ("cagr", math.sqrt(new/old)-1), ("cagr_pct", (math.sqrt(new/old)-1)*100)):
        near(result, "market."+key, number)
    equal(result, "market.FY2024_revenue", None)
    equal(result, "market.forward_growth_pct", None)
    equal(result, "market.is_tam", False)
    equal(result, "scope.distributor_resale_double_counting", False)
    equal(result, "scope.accounting_definition_matches_A_B_D", True)
    for name in eligible:
        prefix = "fy2025_market_shares."+name+"."
        equal(result, prefix+"numerator_source", name)
        for key, number in (("revenue", companies[name]["revenue"]), ("denominator", new), ("share", companies[name]["revenue"]/new), ("share_pct", companies[name]["revenue"]/new*100)):
            near(result, prefix+key, number)
    for name in ("A", "B"):
        near(result, "fy2025_market_shares."+name+".ebitda_margin_pct", companies[name]["ebitda"]/companies[name]["revenue"]*100)
    near(result, "fy2025_market_shares.D.gross_margin_pct", companies["D"]["gross_margin"]*100)
    for path in ("fy2025_market_shares.D.ebitda", "fy2025_market_shares.D.ebitda_margin_pct", "fy2025_market_shares.C.in_scope_revenue", "fy2025_market_shares.C.share", "fy2025_market_shares.C.share_pct"):
        equal(result, path, None)
    equal(result, "identified_supplier_coverage.suppliers", eligible)
    near(result, "identified_supplier_coverage.revenue_sum", sample)
    near(result, "identified_supplier_coverage.share", sample/new)
    near(result, "identified_supplier_coverage.share_pct", sample/new*100)
    equal(result, "identified_supplier_coverage.is_cr3", False)
    near(result, "unallocated_market.revenue", new-sample)
    near(result, "unallocated_market.share", (new-sample)/new)
    near(result, "unallocated_market.share_pct", (new-sample)/new*100)
    equal(result, "unallocated_market.could_include_supplier_larger_than_A", new-sample > companies["A"]["revenue"])
    equal(result, "largest_observed_comparable_supplier", max(eligible, key=lambda x: companies[x]["revenue"]))
    for path in ("market_leader", "concentration_ratio", "valuation_ranking", "stock_return_ranking"):
        equal(result, path, None)
    equal(result, "market_leader_proven", False)
    equal(result, "valuation_ranking_proven", False)

    per_case = {}
    for item in checks:
        summary = per_case.setdefault(item["case"], {"passed": 0, "failed": 0})
        summary["passed" if item["passed"] else "failed"] += 1
    report = {"output_author": "independent_forward_test_agent", "grader_role": "skill_adapter_after_receiving_raw_outputs", "raw_outputs_modified": False, "normalization_used": False, "missing_fields_default_to_pass": False, "independent_agent_evaluation": True, "external_financial_data_used": False, "investment_performance_backtest": False, "input_output_sha256": documents, "assertion_count": len(checks), "passed": sum(x["passed"] for x in checks), "failed": sum(not x["passed"] for x in checks), "per_case": per_case, "checks": checks}
    (ROOT/"independent-verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("assertion_count", "passed", "failed", "per_case")}, ensure_ascii=True))
    return 0 if not report["failed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
