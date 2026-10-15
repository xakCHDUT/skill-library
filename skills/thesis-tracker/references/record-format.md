# Dated record format

Use this structure when creating a new persistent tracker. Existing user formats can retain their own field names. It is a storage guide, not a requirement to expose every field in a short memo.

```json
{
  "company": "Company name and supplied ticker, if any",
  "synthetic": false,
  "baseline": {
    "created_at": "YYYY-MM-DD",
    "information_cutoff": "YYYY-MM-DD",
    "thesis": "Original falsifiable statement",
    "conviction": "Original conviction and reason",
    "pillars": [
      {
        "id": "P1",
        "claim": "Operating claim",
        "expectation": "Metric, period, unit, and threshold",
        "source_ids": ["S1"]
      }
    ],
    "forecasts": [],
    "risks": [],
    "valuation": null
  },
  "updates": [
    {
      "id": "U1",
      "recorded_at": "YYYY-MM-DD",
      "information_cutoff": "YYYY-MM-DD",
      "evidence": [
        {
          "id": "E1",
          "event_date": "YYYY-MM-DD",
          "published_at": "YYYY-MM-DD",
          "source_id": "S2",
          "locator": "Page, table, or supplied input field",
          "type": "reported_actual",
          "period": "Relevant reporting period",
          "fact": "Verifiable fact",
          "pillar_ids": ["P1"]
        }
      ],
      "comparisons": [],
      "scorecard": [],
      "prior_conviction": "Original or most recent conviction",
      "current_conviction": "New conviction and reason",
      "conclusion": "What changed and why",
      "data_gaps": [],
      "next_tests": []
    }
  ],
  "sources": []
}
```

Keep each source's identifier, title, date, locator or supplied file, and origin. Comparisons should carry the actual, baseline or original forecast, absolute difference, relative difference where meaningful, unit, and source identifiers. Rate changes use `percentage_points`; an unavailable result uses `null` plus a reason rather than an invented zero.

An update does not mutate `baseline` or earlier `updates`. Append a correction entry referring to the affected entry when a source is corrected. To replace the operating thesis after it fails, create a dated new thesis version linked to the old version; do not backfill the new claim into the old baseline.
