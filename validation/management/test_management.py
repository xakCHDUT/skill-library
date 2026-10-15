from pathlib import Path
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
import urllib.error

ROOT = Path(__file__).resolve().parents[2]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


catalog_checker = load("check_catalog")
upstream_checker = load("check_upstream")


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="catalog-test-", dir=Path(__file__).parent)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        folder = self.root / "skills" / "example"
        folder.mkdir(parents=True)
        (folder / "SKILL.md").write_text("---\nname: example\ndescription: A synthetic skill.\n---\nBody\n", encoding="utf-8")
        (folder / "LICENSE").write_text("MIT\n", encoding="utf-8")
        (folder / "PROVENANCE.md").write_text("Synthetic source.\n", encoding="utf-8")
        (folder / "validation.json").write_text('{"passed":true}\n', encoding="utf-8")
        self.catalog = {"schema_version": 1, "validated_at": "2026-10-15", "skills": [{
            "id": "example", "category": "test", "license": "MIT", "status": "validated",
            "upstream": {"repository": "example/skills", "path": "skills/example", "commit": "a" * 40, "fork": "https://github.com/example/fork"},
            "validation": {"summary": "Synthetic check", "report": "skills/example/validation.json"}}]}

    def run_check(self):
        path = self.root / "catalog.json"
        path.write_text(json.dumps(self.catalog), encoding="utf-8")
        return catalog_checker.validate(self.root, path)

    def test_valid_small_catalog(self):
        self.assertEqual(self.run_check()["status"], "passed")

    def test_missing_license_and_short_pin(self):
        (self.root / "skills/example/LICENSE").unlink()
        self.catalog["skills"][0]["upstream"]["commit"] = "a" * 7
        report = self.run_check()
        self.assertEqual(len(report["errors"]), 2)

    def test_orphan_and_duplicate(self):
        (self.root / "skills/orphan").mkdir()
        self.catalog["skills"].append(self.catalog["skills"][0])
        errors = self.run_check()["errors"]
        self.assertTrue(any("duplicate" in error for error in errors))
        self.assertTrue(any("orphan" in error for error in errors))

    def test_report_cannot_escape(self):
        self.catalog["skills"][0]["validation"]["report"] = "../outside.txt"
        self.assertTrue(any("escapes" in error for error in self.run_check()["errors"]))

    def test_generated_directory_and_credential_file(self):
        (self.root / "node_modules").mkdir()
        (self.root / ".env").write_text("SAMPLE=value")
        errors = self.run_check()["errors"]
        self.assertTrue(any("dependency directory" in error for error in errors))
        self.assertTrue(any("credential" in error for error in errors))

    def test_secret_is_redacted(self):
        secret = "gh" + "p_" + "A" * 36
        (self.root / "sample.txt").write_text(secret)
        errors = self.run_check()["errors"]
        self.assertTrue(any("token" in error for error in errors))
        self.assertNotIn(secret, json.dumps(errors))

    def test_machine_path_is_detected(self):
        value = "C:" + chr(92) + "Users" + chr(92) + "SyntheticPerson" + chr(92) + "notes"
        (self.root / "sample.txt").write_text(value)
        self.assertTrue(any("local user" in error for error in self.run_check()["errors"]))

    def test_multiline_description(self):
        (self.root / "skills/example/SKILL.md").write_text("---\nname: example\ndescription: >\n  Test a useful\n  behavior.\n---\n", encoding="utf-8")
        self.assertEqual(self.run_check()["status"], "passed")


class UpstreamTests(unittest.TestCase):
    def fixture(self):
        return {"skills": [
            {"id": "a", "upstream": {"repository": "example/skills", "commit": "a" * 40}},
            {"id": "b", "upstream": {"repository": "example/skills", "commit": "b" * 40}}]}

    def test_deduplicates_and_encodes_branch(self):
        calls = []
        def fetch(url, timeout):
            calls.append(url)
            return {"default_branch": "release/current", "archived": False} if len(calls) == 1 else {"sha": "a" * 40}
        result = upstream_checker.check(self.fixture(), fetch=fetch)
        self.assertEqual(len(calls), 2)
        self.assertTrue(calls[1].endswith("release%2Fcurrent"))
        skills = result["repositories"][0]["skills"]
        self.assertFalse(skills[0]["head_differs"])
        self.assertTrue(skills[1]["head_differs"])

    def test_network_error_is_reported(self):
        def fetch(url, timeout):
            raise urllib.error.URLError("test")
        result = upstream_checker.check(self.fixture(), fetch=fetch)
        self.assertEqual(result["repositories"][0]["status"], "error")

    def test_invalid_pin_rejected_before_network(self):
        source = self.fixture()
        source["skills"][0]["upstream"]["commit"] = "short"
        with self.assertRaises(ValueError):
            upstream_checker.check(source, fetch=lambda *_: self.fail("Network should not run"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
