# Provenance and validation

Upstream: [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)  
Commit: `a1043ef544e3a100c28e70a736b6cf32554d0677`  
Source path: `skills/scientific-slides`  
License: MIT, copyright K-Dense Inc.; see `LICENSE.md`. The repository-root license was checked at this same commit.  
Local adaptation: 1, validated 2026-10-15.

This package retains the upstream resources. The entrypoint now routes scientific content planning to the host's presentation tools, makes paid image generation and sibling skills optional, and keeps exact quantitative results in native objects or unchanged source figures. Runtime metadata was moved into the Codex-supported metadata field. The validator now rejects absent parsers, zero-slide PPTX files, and unsupported extensions, and prints UTF-8 diagnostics on Windows.

See the library's `validation/ppt/report.md`, `results.json`, `unicode-cli.json`, and `source-manifest.json` for evidence and per-file hashes. The original snapshot was retained separately during review. This is a local adaptation, not an upstream release or endorsement.

Validated route: Chinese, three-slide native PPTX with a chart and embedded editable workbook, rendered using LibreOffice. PowerPoint application editing, accessibility, paid image generation, Beamer, and the scientific correctness of real research claims were not verified.
