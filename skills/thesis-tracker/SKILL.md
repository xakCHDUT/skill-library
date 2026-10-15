---
name: thesis-tracker
description: Maintain a dated investment-thesis record for a company or watchlist, compare new disclosures with original expectations, and identify supporting evidence, disconfirming evidence, and review triggers. Use for updating an existing investment view or checking whether its reasoning still holds; a standalone annual-report score, fresh valuation, or price-only analysis is outside this skill's scope.
---

# Thesis Tracker

Modified from Anthropic's thesis-tracker on 2026-10-15; see [PROVENANCE.md](PROVENANCE.md). Preserve what was believed at the time, then show exactly what new evidence changes.

## Define or load the original thesis

Use the existing record and supplied disclosures first. Record the company, thesis date, information cutoff, watchlist or user-supplied position, one- or two-sentence thesis, key pillars, risks, and catalysts. Each pillar needs a falsifiable expectation, a relevant period, and the evidence or assumption behind it. Use the number of pillars that the case supports.

Preserve the original thesis, forecasts, thresholds, conviction, and source references. Date new forecasts or changed thresholds as revisions; keep the earlier values visible. A data correction needs a dated correction entry explaining its source and effect, rather than a silent rewrite of past reasoning. If no original record exists, create an explicitly retrospective baseline and mark unknown expectations unknown.

Keep optional target prices and valuation assumptions separate from the operating thesis. Carry them forward only if supplied or supported by a valuation model. A financial-statement quality score, thesis conviction, and whether a security is attractive at today's price answer different questions; do not convert between them mechanically.

## Append the new evidence

For each material disclosure or development, retain:

- Event or reporting date, publication date, and the date added to the tracker; for historical replay, exclude information published after the cutoff.
- Source identifier or verifiable link and locator; period, units, and accounting definition for quantitative inputs. Distinguish reported facts, company guidance, original analyst expectations, and new assumptions.
- The affected pillar, the new fact, its comparison with the **original** expectation, and whether it supports, weakens, refutes, or leaves the pillar unresolved.
- Both favorable and unfavorable evidence, including the strongest counterargument to the current view. An absent disclosure is a data gap rather than a zero or proof of failure.

Recompute year-on-year growth and forecast differences from comparable inputs. For a positive baseline, percentage difference is `(actual / baseline - 1) × 100`; show the absolute difference too. Use percentage points for rate changes. For zero or negative baselines, state the absolute change and explain the sign transition instead of a misleading growth rate. Keep cash flows, profit, balance-sheet stocks, and recurring/nonrecurring measures distinct. A one-off profit beat can coexist with a failed operating thesis.

Use available disclosure or research tools to obtain missing facts when the task requires them; no paid data service is mandatory. Record a missing current price, consensus figure, or metric as unavailable. Price movement can be separately dated market context; it does not establish that an operating pillar is true. Keep synthetic exercises explicitly labeled synthetic.

## Update the scorecard and review conclusion

| Pillar | Original expectation and date | New evidence and source | Current status | Next test |
|---|---|---|---|---|
| | | | Supported / Weakened / Refuted / Unresolved | |

Explain which pillar controls the overall conclusion instead of averaging a count of positive and negative facts. Update conviction with its reason; retain the previous conviction. A decisive invalidation trigger can outweigh higher near-term reported earnings. Distinguish a delayed catalyst from a structural contradiction.

Lead the memo with one precise sentence stating the core change, then the supporting arithmetic and material evidence gaps. For example, use a diagnosis such as “Profit improved while cash conversion deteriorated” only when both sides are evidenced. Do not turn a memorable label into an unsupported allegation.

Default to a research conclusion: thesis intact, weakened, refuted, or unresolved; what evidence would change that conclusion; and the next review. If the user requests a portfolio action, present it as a conditional research recommendation with the supplied position, price, and constraints. Tracking an opinion does not authorize trades, messages, or portfolio changes.

## Maintain the catalyst calendar and record

Track the event, expected date or unknown timing, the metric or evidence to inspect, and the original confirmation/invalidation threshold. Choose a review cadence appropriate to disclosures, commonly quarterly, without scheduling future automation unless requested.

Deliver a concise Markdown memo by default, or use available document tools when Word is requested. For ongoing tracking, save the original baseline plus dated update entries and current scorecard in structured form. Read [references/record-format.md](references/record-format.md) for a compact JSON structure; adapt it to an existing user format rather than replacing that format unnecessarily. Verify that old entries are preserved, all comparisons cite their inputs, and the final conclusion reflects the strongest contrary evidence.
