---
name: model-update
description: Update an existing company forecast or financial model after earnings, guidance changes, or revised assumptions. Reconcile actuals, explain estimate revisions, and calculate supported valuation changes. Use for quarterly model updates and earnings forecast revisions; a standalone annual-report diagnosis or a new valuation model is outside this skill's scope.
---

# Model Update

Turn new evidence into a traceable change to the existing forecast. Keep reported results, prior estimates, and new assumptions distinct.

## Establish the update

Identify the company, reporting period, information cutoff, old model version, and trigger: earnings, guidance, macro assumptions, or a company event. Record currency, scale, accounting basis, and share units. A supplied synthetic case stays explicitly labeled synthetic in the output.

Use supplied filings and model inputs first. Retrieve missing facts from company disclosures or available data tools when the task calls for them. A paid financial-data service is optional. Do not invent consensus, market prices, multiples, source links, or missing model lines. Separate an unknown from a reported zero. For a historical replay, respect the information cutoff.

## Reconcile reported results

Compare the new actuals with the corresponding old estimates for revenue, margins, earnings, and the company's key metrics. Reconcile relevant segment totals, cash, debt, capital spending, working capital, and share changes.

- Label each number as reported actual, prior estimate, explicit assumption, derived calculation, or unavailable; attach its source and period.
- Show absolute and percentage changes where meaningful. If the old value is zero or the sign changes, explain the change rather than presenting a misleading percentage.
- Express margin changes in percentage points; do not confuse them with percentage growth.
- Keep accounting definitions consistent. Identify nonrecurring items and reconcile adjusted versus reported results rather than silently mixing them.

## Revise the forecast

Keep completed periods at reported actuals. Update future periods from disclosed guidance or stated assumptions, explaining the reason for each change. Do not treat guidance or an analyst assumption as a reported result. Avoid automatically annualizing a noisy quarter.

Show an old/new bridge for the current and next financial year only to the extent supported by the available model. Reconcile the full year to its component periods and segments. Show the drivers of the revision, not just the resulting totals.

Compute EPS using earnings attributable to the relevant shareholders and the appropriate weighted average diluted share count. Do not average quarterly share counts without checking duration and dilution, or sum rounded quarterly EPS when annual inputs are available. State whether the denominator is constant, modeled, or missing.

## Explain valuation impact

Recalculate only valuation methods supported by the existing model and supplied or sourced assumptions. Show the prior value, revised value, and the driver: earnings, multiple, discount rate, net debt, or share count.

A supplied P/E scenario can be updated from consistent EPS and its stated multiple. A DCF needs the cash-flow model and discount assumptions; EV-based methods need the equity bridge and diluted shares. Do not substitute one for the other. If current price, consensus, or a required input is absent, mark that comparison unavailable and explain what is missing.

Preserve a prior recommendation only if it was supplied and remains supported. Otherwise describe research implications without inventing a rating. An implied value is conditional on the assumptions and is not a guaranteed outcome.

## Deliver and validate

Default to a concise memo: what changed, actual-versus-estimate table, forecast revision bridge, supported valuation changes, and material data gaps. Scale detail to the user's request. Keep a dated revision history when maintaining an existing model.

If the user requests a workbook, use the host's available spreadsheet tools. Preserve the original file, retain formulas for derived cells, record sources for inputs, recalculate with a supported engine, and verify reconciliation and formula errors before delivery. Do not claim a workbook was updated when only a memo was produced. Word or other formats are optional when requested; no specific Claude, Office, or data-provider integration is required.

End the analysis with a short interpretation: whether the new evidence changes the main thesis or only its timing, what would contradict that interpretation, and which missing evidence could materially change it. Execute no trades or external communications as part of this skill.
