# Provenance

- Upstream: https://github.com/kepano/obsidian-skills
- Revision: `3ccff5338ea700537839b21900aa5358a0402c98` (2026-09-15).
- Upstream license: MIT, Copyright (c) 2026 Steph Ango (@kepano); retained in `LICENSE`.
- Adaptation date: 2026-10-15. Added Codex workflow guidance and synthetic validation fixtures; upstream reference material remains unchanged.
- Added a local HTML adapter with `useAsync: false`, exclusive output creation, a lockfile, and regression tests. Defuddle package 0.19.5 is MIT (Steph Ango, 2025); linkedom 0.18.12 is ISC. Dependencies are installed from npm, not vendored.
- Implementation entry points reviewed at https://github.com/kepano/defuddle/tree/556d74e8c8fd68c49912d4b11a4ae9ec04d7b2b5 .
- Original files were verified against these Git blob hashes before adaptation:

  - `LICENSE`: `33d692ee84f4464f575f2d1e927f19cf1c8ccc57`
  - `skills/defuddle/SKILL.md`: `c1c9b1ba572cb725cb616ccd2d36f1737c65f18e`

New adapter, fixtures, and validation code in this adaptation are provided under the MIT terms in LICENSE. Test fixtures are synthetic and contain no private notes or real-company data.
