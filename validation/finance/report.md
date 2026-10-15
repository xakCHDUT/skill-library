# Finance skill validation report

Date: 2026-10-15. Scope: `model-update` and `sector-overview` only.

## Result

Both skills are ready for review as host-neutral, modified derivatives. Their skill-format validation passed. Author self-checks passed 84 numerical, evidence-boundary, synthetic-label, and upstream-byte assertions. A separate fresh agent then completed all four cases using only the seven specified skill/case/instruction inputs, without the self-check outputs or oracle. Direct grading of its unmodified outputs passed 241 assertions, and a separate semantic read of all four memos passed 20 review criteria. This is selected-case behavioral validation, not an investment-performance backtest or proof of accuracy on live financial data.

No skill was installed. No GitHub changes, external financial API calls, account authentication, subscription purchases, trades, or messages were performed by this subtask.

## Fixed source and licensing

- Repository: https://github.com/anthropics/financial-services
- Fixed source commit: `574ed3624aebd0418c7e96cd101262f30210ab26` (2026-09-21).
- Source paths: `plugins/vertical-plugins/equity-research/skills/model-update/` and `plugins/vertical-plugins/equity-research/skills/sector-overview/`.
- Each upstream skill directory contains only `SKILL.md`; no scripts or hidden runtime dependencies were omitted.
- License: Apache-2.0. The upstream root `LICENSE` is copied without modification into both staged skill directories.
- `upstream-manifest.json` records source commit, paths, byte sizes, and Git blob hashes. The raw upstream `SKILL.md` files, root README, and LICENSE are retained under `upstream/`. All four snapshots match the source Git blob hashes byte for byte.
- Each staged skill has `PROVENANCE.md` identifying Anthropic, the exact source, and the derivative modifications. It explicitly avoids presenting the adaptation as an official Anthropic release.

## Adaptation decisions

### model-update

Retained the update workflow: identify new information, reconcile actuals, revise forecasts, quantify valuation impact, and explain the change in the thesis. Added the following task-relevant constraints:

- Preserve periods, units, accounting basis, and source IDs; distinguish reported actuals, old estimates, new assumptions, and unknowns.
- Keep completed quarters at actuals and reconcile annual totals.
- Separate margin percentage points from growth percentages; handle zero and negative bases without misleading growth rates.
- Use the supplied or sourced annual diluted-share denominator for EPS; do not invent shares.
- Recalculate only valuation methods with sufficient inputs; missing price or consensus remains unavailable.
- Use the host's available spreadsheet and document tools, with recalculation and formula checks when a workbook is actually requested.
- Produce a concise memo by default and do not claim to have updated a workbook when no workbook exists.

### sector-overview

Retained scope, market structure, peer comparison, valuation context, and research implications. Removed fixed page counts and chart quotas. Added these boundaries:

- Require compatible product, geography, period, units, and accounting definitions for comparisons.
- Do not call selected companies' revenue sum the total market or infer market shares without a denominator.
- Exclude unrelated group revenue from a segment comparison; do not compare gross margin as EBITDA margin.
- Avoid value-chain double counting and use the actual elapsed year count for CAGR.
- Keep management claims distinct from verified facts; do not invent valuations, market leadership, or stock rankings from operating data alone.
- Use concise Markdown and available host artifact tools; no Claude-specific integration or paid account is required for bounded supplied-data research.

## Author self-check evidence

The adapter first authored and reviewed the following responses from the staged skills and supplied synthetic cases. These initial responses are explicitly labeled `author_self_check`. A separate program recomputed the arithmetic from raw case inputs after the responses were written. They remain separate from the later independent forward-test outputs.

| Case | What the response demonstrated | Checked result |
|---|---|---|
| Quarterly forecast update | Actual quarters stay fixed; future quarters remain assumptions; annual reconciliation and supported PE scenario | Revenue 1,250 → 1,178.5; EBITDA 250 → 212.245; EPS 1.25 → 0.98; conditional 20× PE value 25.00 → 19.60 |
| Zero baseline and missing inputs | Zero-base growth is undefined; loss-to-profit uses absolute improvement; missing shares/valuation inputs remain missing | Revenue +5; attributable profit +3; EPS and target value unavailable |
| Sector denominator missing | Comparable peers are separated from a mixed group; gross margin stays distinct; sample total is not market size | A/B/D sample revenue 650; A EBITDA margin 20%, B 16%; no invented market share, leader, growth rate, or valuation ranking |
| Matched market denominator added | A new legitimate denominator unlocks only the calculations it supports | 2023–2025 CAGR 10%; A/B/D shares 30.99% / 25.83% / 10.33%; industry leadership and valuation rankings still unsupported |

Qualitative review confirmed the memos label every exercise synthetic; refer only to supplied source IDs; identify assumptions and missing evidence; and do not fabricate URLs, data-provider access, actual investment ratings, or workbook completion. The sector responses do not manufacture an industry landscape beyond the narrow supplied evidence.

## Independent forward-test and scoring

The independent output author received only the two staged `SKILL.md` files, four original case JSON files, and `cases/README.md`. The adapter reviewed the returned four JSON files and four memos without modifying, normalizing, or filling their conclusions. The independent verifier reads the original fields directly, recomputes arithmetic from the raw case inputs, and records a failure for an absent field or incompatible type. Missing conclusions are never defaulted to a passing value.

| Independent case | Direct assertions passed | Failed | Memo review |
|---|---:|---:|---|
| Quarterly forecast update | 108 | 0 | 5 of 5 criteria passed |
| Zero baseline and missing inputs | 32 | 0 | 5 of 5 criteria passed |
| Sector denominator missing | 46 | 0 | 5 of 5 criteria passed |
| Matched market denominator added | 55 | 0 | 5 of 5 criteria passed |
| Total | 241 | 0 | 20 of 20 criteria passed |

The fresh responses preserved the actual/assumption distinction, correctly reconciled quarters to years and EPS, and left price, consensus, DCF and rating conclusions unavailable when unsupported. They also handled the zero/negative-base edge case, excluded unrelated group revenue, separated gross and EBITDA margins, differentiated sample shares from market shares, used two intervals for CAGR, and declined to infer the market leader or a stock ranking from incomplete evidence. The memos agree with their structured values and make no false workbook-completion claim. No material issue requiring a further skill edit was found in these four cases.

`independent-verification.json` includes SHA-256 hashes of all eight unmodified response files and each direct assertion. `qualitative-review.json` records the adapter's separate semantic review with concrete evidence from each memo; those 20 manual criteria are not presented as automated semantic grading. Output generation and evaluation were performed by different agents, while the evaluator was also the skill adapter.

## Reproduction and artifacts

- Cases and replay prompt: `cases/` and `cases/README.md`.
- Actual author responses: `self-check-results/` (four Chinese memos plus structured JSON).
- Deterministic check: `python verify_results.py` (Python standard library only, no network).
- Full assertion results: `verification.json` (84 passed, 0 failed).
- Unmodified independent responses: `independent-results/` (four Chinese memos plus four JSON files).
- Independent direct grading: `python verify_independent.py` (Python standard library only, no network).
- Independent assertion results and raw-output hashes: `independent-verification.json` (241 passed, 0 failed).
- Separate semantic memo review: `qualitative-review.json` (20 criteria passed, 0 failed).
- The host-provided skill creator's `quick_validate.py` was run separately for each staged skill; both returned `Skill is valid!`.

The first format-validation attempt used a Python runtime without PyYAML and stopped before validation. Re-running with an already available environment containing PyYAML passed; no new dependencies were installed. The deterministic verification program itself requires no third-party packages.

The two verifier scripts deliberately use the respective original output schemas. They do not coerce a missing result into a valid conclusion. To repeat forward testing with another fresh agent, supply only the inputs listed in `cases/README.md`; if its JSON layout differs, map the grader to its explicit fields without rewriting the response or inferring absent answers.

## Practical limits

The exercises check selected arithmetic and data-boundary behavior on small synthetic inputs. They do not validate every sector, reporting standard, spreadsheet formula engine, real data connection, or investment result. The skills use existing host tools rather than bundling their own data or model runtime. Live research still requires verifiable current disclosures or supplied documents.

Only the two selected skills were adapted. Known defects in unrelated upstream DCF, comps, or plugin connector files were not copied into these self-contained directories and were not repaired by this task.
