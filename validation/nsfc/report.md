# NSFC application-audit curation validation

Date: 2026-10-15. Upstream: `jiankang1991/nsfc-benzi-audit`, pinned at `9a6010b94a165473f3c4ad71a522b7957381ed5e`, source path `nsfc-benzi-audit`. License: MIT. Upstream repository and skill-package license bytes match.

## What changed

The adapted package has 15 text files: the 14-file upstream skill plus `PROVENANCE.md`. The entrypoint now describes existing-draft diagnosis in Chinese, resolves references relative to the skill, uses available Codex document/web tools, and saves requested reports in the selected output directory. UI wording was updated. The bundled rules reference clearly attributes its 2026-09-12 source check to upstream and requires a fresh applicable official source before any actual compliance finding. The ten subject references and report template are retained. No account, paid API or companion skill is needed for a text-only audit.

## Executed checks

| Check | Actual outcome | What it establishes |
| --- | --- | --- |
| Fixed-source verification | All 17 selected upstream files match the GitHub tree's Git blob IDs; SHA-256 also recorded in `source-manifest.json` | The 14 skill files, two upstream scripts and root LICENSE are the pinned versions |
| Codex skill quick validation | Passed | Entry naming and frontmatter validity, not diagnosis quality |
| Upstream structural validator unit tests | 8 run, 8 passed | Positive and negative fixtures for names, resources, Markdown links/anchors, JSON, license and manifest mutation |
| Adapted package structural validation | No errors; 15 skill files plus one temporary root license checked | Package resources/structure are readable and internally consistent |
| Synthetic evidence replay | Four calculations completed | 86+32=118 contradicts one narrative count of 100; same-year split does not test another year; 6+6+6=18 matches the second draft; two questions can be covered by three tasks |
| Semantic author self-review | Two actual audit artifacts written and inspected | The listed selected decisions below; this is not independent validation |

The first upstream-unit-test attempt failed because the host-provided temporary directory rejected file creation. A workspace-local disposable directory was then used; all eight tests passed without changing the upstream scripts. The published runner uses disposable copies below `work/nsfc-validation-run` and does not modify application inputs. Upstream scripts in `upstream-structure/` are unchanged, with their MIT LICENSE retained alongside them.

Run `python -B validation/nsfc/check_nsfc.py` from the library root. This runner checks structure and replays fixture arithmetic; it does **not** grade prose, infer innovation, or emulate a scientific reviewer. Actual captured output is in `results.json`.

## Author self-review evidence

The two application fixtures are newly written synthetic materials, not real applications. The adapting agent wrote both fixtures and reviews, so these results are author self-checks. No expected-word regex or generated-heading match was used to claim diagnostic success.

| Decision | Review evidence and judgment |
| --- | --- |
| Scientific question versus evidence design | `self-review-01.md` N1 distinguishes correlation/prediction from the promised queue-state causal mechanism and permits narrowing the claim instead of inventing experiments |
| Generalization boundary | N2 separately identifies a 2024-only split as unable to support cross-year claims |
| Data contradiction | N3 reports 100 versus 118 with the reproducible 86+32 sum; it does not decide which original data count is true |
| Innovation evidence | N4 requires a concrete comparative contribution, but does not fabricate citations or infer absence of novelty from an unperformed search |
| Missing attachments | N5 marks agreement status pending rather than inferring lack of authorization from unprovided attachments |
| Missing annual guide | Both reports mark 2027 category/form requirements unverified; neither applies preserved 2026 rules as established 2027 requirements |
| False-positive regression | `self-review-02.md` withdraws unsupported equal-count, first-author SCI and automatic-budget-failure findings; it does not add unwarranted mechanisms or tasks |
| Revision versus execution | The second report marks the validation-plan defect resolved in text while retaining that actual effectiveness has not been tested |
| Evidence integrity | Neither report invents policy, literature, data, funding probability or official reviewer status |

The source snapshots, fixtures and actual outputs are reproducible materials for further evaluation. Upstream historical behavioral runs were read as context; they were not re-run or counted as this curator's results. Any separate forward evaluation must be recorded separately with its own inputs, evaluator and actual artifacts.

## Limits

This selected-case pass does not certify general scientific accuracy, suitability for every NSFC discipline, grant success, target-year eligibility, or current formal compliance. It did not use a real application, perform external novelty searching, validate current annual rules, inspect real attachments, or exercise PDF/DOCX extraction/OCR and document rendering. The skill's dated reference links are navigation aids and must be rechecked for an actual rule-sensitive audit. Text-only use is the validated route.

## Independent forward exercise

A fresh-context agent that did not adapt this skill received only the skill, relevant references and one new synthetic revision-review task. It was not shown the author's answers or intended conclusions. The actual [task](independent/task.md) and [response](independent/response.md) are retained. The parent curator reviewed the response against every supplied excerpt:

- R01 is explicitly withdrawn: two questions can map to three mutually supporting tasks. The response does not demand equal counts or unnecessary deletion.
- R02 remains a must-fix: one city's two districts cannot establish the claimed cross-city or national scope. Remedies are conditional on real data availability, with narrowing the claim as an alternative.
- Absolute novelty wording is separated from an unperformed novelty search; the response neither invents literature nor concludes the whole application lacks evidence.
- The mechanism-versus-association question is marked for verification against the complete draft, not treated as a confirmed defect from an excerpt alone.
- Unknown application year, category and formal guide stay unverified. Missing attachments or unshown accuracy results are not fabricated defects.

This is one independently executed text-only case with qualitative parent review, separate from the author's two exercises, eight upstream unit tests and four calculations. Captured relative execution paths refer to the original isolated run; the public input is linked above. No official reviewer decision or grant outcome was tested.
