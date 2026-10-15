#!/usr/bin/env python3
"""Run structural tests and replay the synthetic evidence arithmetic; MIT.

This does not judge the semantic quality of an AI audit. See report.md.
Run from the repository root with: python -B validation/nsfc/check_nsfc.py
"""
import csv
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
LIBRARY = HERE.parents[1]
SKILL = LIBRARY / "skills" / "nsfc-benzi-audit"
SCRATCH = (Path.cwd() / "work" / "nsfc-validation-run").resolve()
# Every disposable copy created and removed by this runner stays under cwd/work.
assert SCRATCH.is_relative_to(Path.cwd().resolve())
SCRATCH.mkdir(parents=True, exist_ok=True)
tempfile.tempdir = str(SCRATCH)
sys.path.insert(0, str(HERE / "upstream-structure"))
from validate_repo import validate


def read_rows(relative):
    with (HERE / "cases" / relative).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main():
    spec = importlib.util.spec_from_file_location(
        "upstream_tests", HERE / "upstream-structure" / "test_validate_repo.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream).run(
        unittest.defaultTestLoader.loadTestsFromModule(module))
    if not result.wasSuccessful():
        print(stream.getvalue(), file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="nsfc-package-", dir=SCRATCH) as tmp:
        root = Path(tmp).resolve()
        assert root.is_relative_to(SCRATCH)
        shutil.copytree(SKILL, root / "nsfc-benzi-audit")
        shutil.copyfile(SKILL / "LICENSE", root / "LICENSE")
        structure = validate(root)
        assert not structure["errors"], structure["errors"]

    rows = read_rows("01-network/samples.csv")
    total = sum(int(row["distinct_complete_days"]) for row in rows)
    assert total == 118 and total != 100
    plan = read_rows("01-network/validation-plan.csv")
    years = {row["year"] for row in plan}
    assert years == {"2024"}  # Same-year splitting cannot evidence a new year.
    pilot = sum(int(row["runs"]) for row in read_rows("02-revision/pilot.csv"))
    assert pilot == 18
    coverage = read_rows("02-revision/coverage.csv")
    questions = {row["question"] for row in coverage}
    tasks = {row["task"] for row in coverage}
    assert questions == {"Q1", "Q2"} and tasks == {"T1", "T2", "T3"}
    assert all(any(row["question"] == q and row["validation"] for row in coverage)
               for q in questions)
    summary = {
        "scope": "structure and evidence recomputation, not semantic review scoring",
        "upstream_structural_unit_tests": {"run": result.testsRun, "passed": result.testsRun},
        "adapted_package_structure": structure,
        "synthetic_data_replays": [
            {"case": "01-network", "distinct_days_table_total": total,
             "narrative_counts": [100, 118], "contradiction": True,
             "does_not_establish_original_data_truth": True},
            {"case": "01-network", "training_and_test_years": sorted(years),
             "cross_year_validation": False},
            {"case": "02-revision", "pilot_runs": pilot, "matches_draft": True},
            {"case": "02-revision", "questions": sorted(questions),
             "tasks": sorted(tasks), "all_questions_mapped_to_validation": True}
        ],
        "author_semantic_self_reviews": 2,
        "independence": "The semantic outputs were written by the adapting agent; not independently scored here."
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
