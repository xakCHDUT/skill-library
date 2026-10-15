# Provenance and validation

Upstream: [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)  
Commit: `a1043ef544e3a100c28e70a736b6cf32554d0677`  
Source path: `skills/statistical-analysis`  
License: MIT, copyright K-Dense Inc.; see LICENSE.md.  
Local fork revision: 1, validated 2026-10-15.

Changes: Preserve full precision of Pingouin CI95 before presentation rounding; adapt compatibility metadata for Codex. Statistical algorithms are unchanged.

The original snapshot and upstream blob hashes were retained separately during review. Full source attribution is retained. This is a reviewed fork, not an upstream release or a claim of endorsement.

Validation evidence is in `validation/validation.json`; the environment snapshot is `validation/requirements-tested.txt`. It records a Windows Python 3.12 environment, not a universal cross-platform lockfile. Install only task-required dependencies in an isolated environment. Run the bundled additional regressions with `python -m pytest validation` from this skill directory.

- Optional PyMC/ArviZ Bayesian workflow was not installed or sampled in this validation.
- Diagnostic plots do not establish independence, causal validity or model adequacy.
