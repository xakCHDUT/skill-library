# Thesis tracker validation

Date: 2026-10-15. Scope: the adapted `thesis-tracker` skill only.

## Result and scope

Skill-format validation passed. Two fully synthetic cases were actually materialized into before/after JSON tracking records and Chinese review memos. A separate arithmetic and record-integrity checker recomputed the entered answers from the raw cases: **47 named author self-checks passed, zero failed**. This is author-produced selected-case validation, not independent behavioral evaluation, a live market test, or an investment-return backtest.

No global skill installation, account mutation, trades, subscription access, or external messages were performed in this subtask. Only text artifacts are included.

## Source and adaptations

The source is Anthropic's `financial-services` repository at fixed commit `574ed3624aebd0418c7e96cd101262f30210ab26`, path `plugins/vertical-plugins/equity-research/skills/thesis-tracker/SKILL.md`. The source directory contains one file. The root license is Apache-2.0; the pinned tree has no root NOTICE file. Both source files in `upstream/` match the Git blob hashes recorded by GitHub, and the staged skill's license matches byte for byte. `source-manifest.json` records SHA-256 hashes as well.

The adaptation preserves the five-part original workflow: define/load a thesis, log new data, update a pillar scorecard, track catalysts, and deliver a review. It adds a compact optional structured-record guide and addresses the errors most relevant to recurring research:

- Preserve the original statement, forecasts, thresholds, and prior conviction; append new evidence and dated corrections rather than rewriting the history.
- Retain event dates, publication dates, record dates, source locators, and the information cutoff.
- Show both supporting and disconfirming evidence and explain why a decisive failed pillar can outweigh a profit beat.
- Separate reported profit, recurring profit, cash conversion, forecast differences, rate changes, market price context, thesis confidence, financial-statement scores, and valuation.
- Preserve missing values as unknown; make conditional research recommendations only to the extent requested and supported.

## Actual author exercises

All company names, publications, accounting values, and share-price observations below are fictional. They contain no personal portfolio information or course materials.

| Case | Actual generated result | Meaningful checks |
|---|---|---|
| Cash versus profit | Revenue +25% YoY, profit +50%, cash flow −75%; cash conversion 1.2 → 0.2. Inventory grows 62.5%, above the original 10% limit. Thesis weakened; medium conviction becomes low. | Preserve baseline; separate stock and flow periods; original forecasts remain visible; profit beat +15.38% coexists with cash-flow forecast miss −76.92%; no invented inventory forecast or unsupported fraud allegation. |
| Positive earnings, refuted thesis | Reported profit +50% YoY and +20% versus forecast, but recurring revenue is flat, core profit falls 10%, and customer retention falls from 95% to 84%, below the original 92% invalidation threshold. Thesis refuted; high conviction becomes low. | Reconcile core profit 18 plus after-tax disposal gain 12 to reported profit 30; one-off share 40%; retention decline −11 percentage points; zero-base gain does not produce a bogus growth percentage; synthetic price gain +18% is separate market context, not pillar evidence. |

The raw inputs are in `cases/`. Each `.before.json` stores the baseline and each `.after.json` preserves it and appends a dated entry. The `.md` memos explain the controlling evidence and missing data. `build_author_cases.py` reproduces these author-written fixtures; it is not a model runner. Numerical answers are explicitly entered in that builder, then independently recomputed as arithmetic by `check_cases.py`. This does **not** make the author assessment an independent agent evaluation.

Run from this directory with Python 3:

```text
python build_author_cases.py
python check_cases.py
```

`results.json` records the 47 named checks. These cover original-record preservation, append behavior, historical date/source consistency, raw-input equality, every entered metric comparison, zero-base handling, rate units, profit bridges, the original threshold treatment, source-byte integrity, and the two selected qualitative classifications. The qualitative classifications are author expectations, not proof of general judgment quality.

## Limits

No live issuer disclosure, market-data retrieval, investment-return simulation, real portfolio decision, broker execution, or multi-company workflow was tested. The examples exercise one update per company; they do not establish long-run file versioning, all accounting edge cases, model consistency across repeated runs, or performance on previously unseen financial cases. Future independent behavioral results, if performed, should be recorded separately from these author artifacts.

## Independent forward exercise

A fresh-context agent that did not write the adaptation received the skill, its record reference and one new synthetic historical task, with no author answers or expected result. Its actual [memo](independent/response.md), [record](independent/record.json) and [task](independent/task.md) are retained. The parent curator inspected the complete output against the raw task:

- Original 2026-05-10 forecasts and the two operating conditions remain visible and unchanged.
- The 2026-09-01 correction is excluded from the 2026-08-20 replay; the later writing date is stored separately.
- Profit after one-off contributions is 33−40=−7, so the positive-core-profit pillar fails. Cash flow −12 is 45 below net profit 33, independently failing the second pillar.
- Negative prior-year profit is handled as a 38 absolute improvement and a loss-to-profit transition, not a misleading percentage. Margin differences use percentage points.
- An unverified 30% share-price statement is not used as operating evidence or a fabricated current quote. Missing valuation and position information remain unknown.
- New Q3 observation conditions are dated as new and do not rewrite the Q2 thesis. The conclusion does not predict permanent business failure or execute a trade.

All eight comparison rows were then recomputed from raw-task constants by [check_arithmetic.py](independent/check_arithmetic.py): **8/8 passed**, recorded in [numerical-checks.json](independent/numerical-checks.json). These are eight numeric rows, not eight independent model trials. The qualitative review is a separate manual assessment. Captured relative paths refer to the isolated original run; public inputs are linked above. One unseen example does not establish repeated-run reliability or investment performance.
