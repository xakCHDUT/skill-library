"""Materialize two author-written synthetic cases and tracker responses.

This is reproducible fixture assembly, not an independent model evaluation.
Numerical answers are entered explicitly; check_cases.py recomputes them from
the raw inputs. All companies, releases, events, and values are fictional.
"""

from copy import deepcopy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def save(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source(sid, title, publication, locator):
    return {"id": sid, "title": title, "published_at": publication,
            "locator": locator, "origin": "synthetic_supplied_case"}


def comparison(metric, actual, prior, forecast, yoy_abs, yoy_pct, surprise_abs, surprise_pct):
    return {"metric": metric, "unit": "CNY million", "actual": actual,
            "prior_year_actual": prior, "original_forecast": forecast,
            "yoy_absolute": yoy_abs, "yoy_percent": yoy_pct,
            "forecast_difference_absolute": surprise_abs,
            "forecast_difference_percent": surprise_pct}


def write_case(name, raw, baseline, sources, update, memo):
    before = {"company": raw["company"], "synthetic": True,
              "baseline": baseline, "updates": [], "sources": sources[:2]}
    after = deepcopy(before)
    after["sources"] = sources
    after["updates"].append(update)
    save(f"cases/{name}.json", raw)
    save(f"author-responses/{name}.before.json", before)
    save(f"author-responses/{name}.after.json", after)
    (ROOT / "author-responses" / f"{name}.md").write_text(memo, encoding="utf-8")


def cash_case():
    sources = [
        source("A-PRIOR", "Fictional 2025 Q1 disclosure", "2025-04-25", "prior_year fields"),
        source("A-THESIS", "Fictional original research note", "2026-02-15", "original_forecast and baseline"),
        source("A-NEW", "Fictional 2026 Q1 disclosure", "2026-04-27", "actual fields"),
    ]
    raw = {
        "company": "合成案例甲：岭山设备（虚构，无证券代码）", "synthetic": True,
        "request": "用原始观点更新季度跟踪记录，保留原文和预测，说明哪些新证据支持或削弱观点，并计算同比及预期差。不要另建估值。",
        "unit": "CNY million", "flow_period": "2026 Q1", "stock_date": "2026-03-31",
        "prior_flow_period": "2025 Q1", "prior_stock_date": "2025-03-31",
        "accounting_basis": "consolidated; net_profit and operating_cash_flow share the same entity scope",
        "prior_year": {"revenue": 100, "net_profit": 10, "operating_cash_flow": 12, "inventory": 40},
        "original_forecast": {"revenue": 120, "net_profit": 13, "operating_cash_flow": 13},
        "actual": {"revenue": 125, "net_profit": 15, "operating_cash_flow": 3, "inventory": 65},
        "thresholds": {"revenue_yoy_min_percent": 15, "cash_conversion_min_ratio": 1,
                       "inventory_yoy_max_percent": 10},
        "new_data_publication": "2026-04-27", "recorded_at": "2026-04-28",
        "information_cutoff": "2026-04-28", "sources": sources,
        "unknowns": ["inventory composition and aging", "receivable aging", "seasonality and next-quarter collections", "market price", "valuation"],
    }
    baseline = {
        "created_at": "2026-02-15", "information_cutoff": "2026-02-15", "position": "watchlist",
        "thesis": "收入增长可转化为现金，备货保持克制，支持盈利增长具有持续性。",
        "conviction": "medium",
        "pillars": [
            {"id": "P1", "claim": "收入延续增长", "expectation": "2026 Q1 revenue YoY >= 15%", "source_ids": ["A-THESIS", "A-PRIOR"]},
            {"id": "P2", "claim": "利润转化为现金", "expectation": "2026 Q1 operating cash flow / net profit >= 1.0", "source_ids": ["A-THESIS", "A-PRIOR"]},
            {"id": "P3", "claim": "库存占用克制", "expectation": "2026-03-31 inventory YoY <= 10%", "source_ids": ["A-THESIS", "A-PRIOR"]},
        ],
        "forecasts": [{"period": "2026 Q1", "unit": "CNY million", "values": raw["original_forecast"], "source_id": "A-THESIS"}],
        "risks": ["利润不能回款", "库存积压或增长超过需求"], "valuation": None,
    }
    comps = [comparison("revenue", 125, 100, 120, 25, 25, 5, 4.1666666667),
             comparison("net_profit", 15, 10, 13, 5, 50, 2, 15.3846153846),
             comparison("operating_cash_flow", 3, 12, 13, -9, -75, -10, -76.9230769231),
             comparison("inventory", 65, 40, None, 25, 62.5, None, None)]
    for row in comps:
        row.update({"actual_source_id": "A-NEW", "prior_source_id": "A-PRIOR",
                    "forecast_source_id": "A-THESIS" if row["original_forecast"] is not None else None,
                    "period": "2026-03-31 vs 2025-03-31" if row["metric"] == "inventory" else "2026 Q1 vs 2025 Q1"})
    update = {
        "id": "A-U1", "recorded_at": "2026-04-28", "information_cutoff": "2026-04-28",
        "evidence": [{"id": "A-E1", "event_date": "2026-03-31", "published_at": "2026-04-27", "source_id": "A-NEW",
                      "locator": "actual revenue, net_profit, operating_cash_flow, inventory", "type": "reported_actual",
                      "period": "2026 Q1 flows; inventory at 2026-03-31", "fact": raw["actual"], "pillar_ids": ["P1", "P2", "P3"]}],
        "comparisons": comps,
        "derived": {"cash_conversion_current": 0.2, "cash_conversion_prior": 1.2,
                    "cash_conversion_change_percentage_points": -100,
                    "inventory_threshold_amount": 44, "inventory_excess_above_threshold": 21},
        "scorecard": [
            {"pillar_id": "P1", "status": "supported", "evidence_ids": ["A-E1"], "reason": "收入同比25%，超过原15%门槛。"},
            {"pillar_id": "P2", "status": "weakened", "evidence_ids": ["A-E1"], "reason": "现金转化率0.2，未达原1.0门槛；季节性解释未知。"},
            {"pillar_id": "P3", "status": "weakened", "evidence_ids": ["A-E1"], "reason": "库存同比62.5%，超过原10%上限；性质和库龄未知。"},
        ],
        "prior_conviction": "medium", "current_conviction": "low", "thesis_status": "weakened",
        "conclusion": "利润长得快，现金跟不上：原先的现金型增长判断明显受损，库存去化与回款成为下一次验证重点。",
        "strongest_supporting_evidence": "收入同比25%、净利润同比50%，分别比原预测高4.17%、15.38%。",
        "strongest_disconfirming_evidence": "经营现金流同比下降75%，现金转化率0.2，库存同比增加62.5%。",
        "data_gaps": raw["unknowns"], "valuation": None, "investment_action": None,
        "next_tests": [{"event": "下一次财务披露及库存/回款解释", "expected_date": None,
                        "test": "核对季节性、库龄、订单与回款；季度现金转化原门槛1.0仍保留，任何新门槛需另记日期及依据。"}],
    }
    memo = """# 合成案例甲：季度观点更新

**利润长得快，现金跟不上：原先的现金型增长判断明显受损。** 公司、披露、数值均为虚构；信息截止 2026-04-28。这是技能作者自检产物。

2026-02-15 原始观点为收入增长能够转化为现金、备货克制，信心为中。原文、三项门槛与 Q1 预测均保留在记录的 baseline 中，没有用新数据改写旧预期。

| 指标（百万元） | 2025 Q1 / 期末 | 2026 Q1 原预测 | 2026 Q1 / 期末实际 | 同比 | 较原预测 |
|---|---:|---:|---:|---:|---:|
| 收入 | 100 | 120 | 125 | +25.00% | +4.17% |
| 净利润 | 10 | 13 | 15 | +50.00% | +15.38% |
| 经营现金流 | 12 | 13 | 3 | −75.00% | −76.92% |
| 库存 | 40 | 未预测 | 65 | +62.50% | 不适用 |

收入支柱获得支持。现金转化率从 1.2 降至 0.2，即 120% 降至 20%，下降 100 个百分点；未达到原 1.0 门槛。库存 65 高于原同比增长不超过 10% 对应的 44 上限，超出 21。库存是 3 月 31 日时点值；其他指标是 Q1 期间值。资料口径为合并报表。

因此整体观点削弱，信心由中降为低。利润高于预期是正面证据，但不足以抵消现金和库存对原逻辑的冲击。单季不足以断言库存积压、财务造假或必然经营失败；还缺库龄、订单、回款和季节性解释。下一次披露日期未知，届时检查这些问题，保留原门槛。未提供价格与估值，不据此给出买卖动作或年报质量分。

来源：A-PRIOR（2025-04-25，prior_year）、A-THESIS（2026-02-15，原观点与预测）、A-NEW（2026-04-27，actual）；均为 supplied synthetic case。\n"""
    write_case("cash-versus-profit", raw, baseline, sources, update, memo)


def refuted_case():
    sources = [
        source("B-PRIOR", "Fictional 2025 Q1 disclosure", "2025-04-26", "prior_year fields"),
        source("B-THESIS", "Fictional original research note", "2026-02-20", "original_forecast and baseline"),
        source("B-NEW", "Fictional 2026 Q1 disclosure and customer update", "2026-04-28", "actual fields"),
        source("B-MARKET", "Fictional market context", "2026-04-29", "market_context fields"),
    ]
    raw = {
        "company": "合成案例乙：晴川订阅（虚构，无证券代码）", "synthetic": True,
        "request": "更新原先关于订阅增长与客户黏性的观点。新一期净利润超预期且股价上涨，检查原逻辑是否仍然成立，保留旧观点和门槛。",
        "unit": "CNY million", "flow_period": "2026 Q1", "prior_flow_period": "2025 Q1",
        "accounting_basis": "consolidated; core_net_profit + after-tax_disposal_gain = net_profit",
        "prior_year": {"revenue": 200, "net_profit": 20, "recurring_revenue": 180,
                       "core_net_profit": 20, "after_tax_disposal_gain": 0, "gross_customer_retention_percent": 95},
        "original_forecast": {"revenue": 220, "net_profit": 25, "recurring_revenue": 198, "core_net_profit": 25},
        "actual": {"revenue": 210, "net_profit": 30, "recurring_revenue": 180,
                   "core_net_profit": 18, "after_tax_disposal_gain": 12, "gross_customer_retention_percent": 84},
        "thresholds": {"recurring_revenue_yoy_min_percent": 10, "gross_customer_retention_min_percent": 92,
                       "core_net_profit_yoy_min_percent": 10},
        "qualitative_actual": "截至2026-03-31，上一年贡献15%订阅收入的一家客户未续约；新客户收入恰好抵消其流失额。",
        "market_context": {"start_date": "2026-02-19", "start_price": 40, "end_date": "2026-04-29", "end_price": 47.2,
                           "unit": "synthetic CNY per share", "source_id": "B-MARKET"},
        "new_data_publication": "2026-04-28", "recorded_at": "2026-04-29", "information_cutoff": "2026-04-29",
        "sources": sources, "unknowns": ["reasons for nonrenewal and replacement customer quality", "next-quarter customer retention", "valuation model"],
    }
    baseline = {
        "created_at": "2026-02-20", "information_cutoff": "2026-02-20", "position": "watchlist",
        "thesis": "高客户黏性支持订阅收入及核心利润持续增长；增长依靠持续经营业务。",
        "conviction": "high",
        "pillars": [
            {"id": "P1", "claim": "订阅持续增长", "expectation": "2026 Q1 recurring revenue YoY >= 10%", "source_ids": ["B-THESIS", "B-PRIOR"]},
            {"id": "P2", "claim": "客户黏性稳固", "expectation": "2026 Q1 gross customer retention >= 92%; below 92% invalidates the strong-retention pillar", "source_ids": ["B-THESIS", "B-PRIOR"]},
            {"id": "P3", "claim": "核心盈利增长", "expectation": "2026 Q1 core net profit YoY >= 10%", "source_ids": ["B-THESIS", "B-PRIOR"]},
        ],
        "forecasts": [{"period": "2026 Q1", "unit": "CNY million", "values": raw["original_forecast"], "source_id": "B-THESIS"}],
        "risks": ["关键客户流失", "报告利润被一次性收入抬高"], "valuation": None,
    }
    comps = [comparison("revenue", 210, 200, 220, 10, 5, -10, -4.5454545455),
             comparison("net_profit", 30, 20, 25, 10, 50, 5, 20),
             comparison("recurring_revenue", 180, 180, 198, 0, 0, -18, -9.0909090909),
             comparison("core_net_profit", 18, 20, 25, -2, -10, -7, -28),
             comparison("after_tax_disposal_gain", 12, 0, None, 12, None, None, None)]
    comps[-1]["yoy_percent_reason"] = "Prior-year zero; percent growth is undefined."
    for row in comps:
        row.update({"actual_source_id": "B-NEW", "prior_source_id": "B-PRIOR",
                    "forecast_source_id": "B-THESIS" if row["original_forecast"] is not None else None,
                    "period": "2026 Q1 vs 2025 Q1"})
    update = {
        "id": "B-U1", "recorded_at": "2026-04-29", "information_cutoff": "2026-04-29",
        "evidence": [
            {"id": "B-E1", "event_date": "2026-03-31", "published_at": "2026-04-28", "source_id": "B-NEW",
             "locator": "actual and qualitative_actual", "type": "reported_actual", "period": "2026 Q1",
             "fact": raw["actual"], "additional_fact": raw["qualitative_actual"], "pillar_ids": ["P1", "P2", "P3"]},
            {"id": "B-E2", "event_date": "2026-04-29", "published_at": "2026-04-29", "source_id": "B-MARKET",
             "locator": "market_context", "type": "market_context", "period": "2026-02-19 to 2026-04-29",
             "fact": raw["market_context"], "pillar_ids": []},
        ],
        "comparisons": comps,
        "derived": {"gross_customer_retention_change_percentage_points": -11,
                    "retention_gap_to_threshold_percentage_points": -8,
                    "disposal_share_of_reported_net_profit_percent": 40,
                    "reported_profit_bridge": {"core_net_profit": 18, "after_tax_disposal_gain": 12, "net_profit": 30},
                    "market_price_change_percent": 18},
        "scorecard": [
            {"pillar_id": "P1", "status": "weakened", "evidence_ids": ["B-E1"], "reason": "订阅收入零增长，低于原10%增长门槛与198预测。"},
            {"pillar_id": "P2", "status": "refuted", "evidence_ids": ["B-E1"], "reason": "客户留存率84%低于92%失效门槛，且关键客户未续约。"},
            {"pillar_id": "P3", "status": "weakened", "evidence_ids": ["B-E1"], "reason": "核心净利润同比下降10%；一次性处置收益贡献报告净利润40%。"},
        ],
        "prior_conviction": "high", "current_conviction": "low", "thesis_status": "refuted",
        "conclusion": "净利润超预期，但一次性收益撑起增长；客户流失已击穿原先的高黏性增长逻辑。",
        "strongest_supporting_evidence": "报告净利润同比增长50%、比原预测高20%；新客户收入抵消了流失客户收入。",
        "strongest_disconfirming_evidence": "留存率84%触发原92%失效条件，订阅收入零增长、核心净利润下降10%。",
        "data_gaps": raw["unknowns"], "valuation": None, "investment_action": None,
        "next_tests": [{"event": "下一次客户及财务披露", "expected_date": None,
                        "test": "核对流失原因、替代客户质量及持续核心利润；若建立新观点，应另建有日期的版本，不能降低旧门槛后宣布旧观点成立。"}],
    }
    memo = """# 合成案例乙：反证优先的观点更新

**净利润超预期，但一次性收益撑起增长；客户流失已击穿原先的高黏性增长逻辑。** 公司、披露、股价和数值均为虚构；信息截止 2026-04-29。这是技能作者自检产物。

2026-02-20 原始判断为客户黏性支撑订阅与核心盈利持续增长，信心为高。原预期包括订阅收入增长至少10%、客户留存率至少92%、核心净利润增长至少10%；原记录明确留存率低于92%使高黏性支柱失效。保留这些原始门槛，不事后降低标准。

| 指标（百万元） | 上年同期 | 原预测 | 本期实际 | 同比 | 较原预测 |
|---|---:|---:|---:|---:|---:|
| 收入 | 200 | 220 | 210 | +5.00% | −4.55% |
| 报告净利润 | 20 | 25 | 30 | +50.00% | +20.00% |
| 订阅收入 | 180 | 198 | 180 | 0.00% | −9.09% |
| 核心净利润 | 20 | 25 | 18 | −10.00% | −28.00% |
| 税后处置收益 | 0 | 未预测 | 12 | 增加12；零基数不算增长率 | 不适用 |

核心净利润18加税后处置收益12等于报告净利润30，一次性部分占40%。留存率由95%降至84%，下降11个百分点，低于原92%门槛8个百分点。一家上年贡献15%订阅收入的客户未续约；新客户恰好抵消收入损失，是积极证据，但尚不能证明客户稳定性恢复。

当前原始观点被反证，信心由高降为低。支柱判断由留存率触发条件及核心盈利决定，不以正面消息条数投票。合成股价从40涨到47.2（+18%）仅作为市场背景，不是客户黏性证据，也不是估值便宜的证据。未提供估值模型，不给出目标价、交易动作或财报质量分。

下一次披露日期未知，重点核对流失原因、替代客户质量与持续核心盈利。若需要提出新的投资逻辑，应创建有日期的新版本并链接旧观点，不能覆盖这次判断。来源 B-PRIOR、B-THESIS、B-NEW、B-MARKET 均为 supplied synthetic case，其日期与字段位置见 JSON。\n"""
    write_case("positive-earnings-refuted-thesis", raw, baseline, sources, update, memo)


if __name__ == "__main__":
    cash_case()
    refuted_case()
    print("Wrote 2 synthetic input cases and 6 author-response artifacts.")
