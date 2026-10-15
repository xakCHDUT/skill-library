# Source and modifications

Original author: OpenAI. Source: [openai/skills](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/jupyter-notebook).

Pinned commit: `49f948faa9258a0c61caceaf225e179651397431`.
Personal upstream fork: https://github.com/xakCHDUT/openai-skills
License: Apache-2.0; original `LICENSE.txt` retained. This derivative is not an official OpenAI release.

Modified on 2026-10-15:

- `scripts/new_notebook.py`: use the caller's working directory for default output; emit UTF-8 so Unicode paths do not turn a completed write into a failing command; exclusively create files unless `--force` is explicit.
- Both notebook templates: add stable, unique cell IDs required by their declared notebook format.
- `SKILL.md`: clarify Windows invocation, optional uv, explicit output locations and isolated validation; avoid rewriting CODEX_HOME in examples.
- Add provenance, source hashes and reproducible synthetic regression tests.

Original Windows reproduction: a Chinese/emoji output path with `PYTHONIOENCODING=gbk` produced a file then exited with UnicodeEncodeError. Original templates also emitted MissingIDFieldWarning under strict nbformat validation. The default path issue was identified by source inspection. The exclusive-create change closes a check/write race; no concurrent-race stress test is claimed.

All 12 original files were checked against GitHub Git blob hashes at the pinned commit; see `upstream-manifest.json`. Seventeen post-fix CLI, schema and actual notebook execution checks passed. These tests exercise the bundled examples; they do not establish correctness for arbitrary future notebooks.
