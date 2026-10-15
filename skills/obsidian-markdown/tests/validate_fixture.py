"""File-level checks for the synthetic vault; not an Obsidian renderer."""
from pathlib import Path
import argparse
import copy
import datetime
import json
import re
import yaml


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def read_note(file):
    text = file.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    assert frontmatter, f"Missing frontmatter: {file.name}"
    return yaml.load(frontmatter.group(1), Loader=UniqueLoader), text[frontmatter.end():]


def validate_links(vault, text):
    checked = 0
    for match in re.finditer(r"!?\[\[([^\]]+)\]\]", text):
        target = match.group(1).split("|", 1)[0]
        name, _, anchor = target.partition("#")
        file = vault / name
        if not file.suffix:
            file = file.with_suffix(".md")
        assert file.is_file(), f"Missing link: {name}"
        target_text = file.read_text(encoding="utf-8")
        if anchor.startswith("^"):
            assert re.search(r"(?:^|\s)" + re.escape(anchor) + r"(?:\s|$)", target_text), "Missing block"
        elif anchor:
            headings = re.findall(r"^#{1,6}\s+(.+)$", target_text, re.M)
            assert anchor in headings, "Missing heading"
        checked += 1
    return checked


def validate_filter(value):
    if isinstance(value, str):
        assert value.strip()
        return
    assert isinstance(value, dict) and len(value) == 1, "Filter needs one logical operator"
    key, children = next(iter(value.items()))
    assert key in {"and", "or", "not"}, "Unknown filter operator"
    assert isinstance(children, list) and children, "Filter operands must be a nonempty list"
    for child in children:
        validate_filter(child)


def validate_base(base):
    assert isinstance(base, dict)
    validate_filter(base["filters"])
    formulas = base.get("formulas", {})
    assert isinstance(formulas, dict)
    assert all(isinstance(v, str) for v in formulas.values())
    assert isinstance(base["views"], list) and base["views"]
    for view in base["views"]:
        assert view["type"] in {"table", "cards", "list", "map"}
        for column in view.get("order", []):
            assert isinstance(column, str)
            if column.startswith("formula."):
                assert column[8:] in formulas, "Undefined formula"


def run(vault):
    checks = []
    notes = {p: read_note(p) for p in sorted(vault.rglob("*.md"))}
    assert len(notes) == 3
    checks.append("three Markdown files have valid unique-key YAML frontmatter")
    for properties, _ in notes.values():
        assert isinstance(properties["title"], str)
        assert isinstance(properties["tags"], list) and all(isinstance(x, str) for x in properties["tags"])
        assert isinstance(properties["aliases"], list)
    checks.append("title, tags and aliases retain their intended property types")
    research = [p for p, _ in notes.values() if "score" in p]
    assert len(research) == 2
    assert all(type(p["score"]) is int and isinstance(p["date"], datetime.date) for p in research)
    checks.append("sample scores and dates parse as numbers and dates")
    link_count = sum(validate_links(vault, text) for _, text in notes.values())
    assert link_count == 6
    checks.append("six note, heading, block and Base embed targets resolve")
    base = yaml.load((vault / "阅读库.base").read_text(encoding="utf-8"), Loader=UniqueLoader)
    validate_base(base)
    checks.append("Base YAML structure, filter shape and formula references validate")
    assert all(column in {"file.name", "formula.reading_status", "score", "source"} for column in base["views"][0]["order"])
    assert all("score" in p and "source" in p for p in research)
    checks.append("all sample table columns have corresponding note or formula properties")
    for name, callback in [
        ("duplicate YAML keys are rejected", lambda: yaml.load("score: 1\nscore: 2", Loader=UniqueLoader)),
        ("broken note links are rejected", lambda: validate_links(vault, "[[missing-note]]")),
        ("missing heading anchors are rejected", lambda: validate_links(vault, "[[资料/现金流观察#不存在]]")),
        ("missing block anchors are rejected", lambda: validate_links(vault, "[[资料/现金流观察#^missing]]")),
    ]:
        try:
            callback()
        except (AssertionError, ValueError):
            checks.append(name)
        else:
            raise AssertionError(f"Negative check did not fail: {name}")
    invalid = copy.deepcopy(base)
    invalid["views"][0]["order"].append("formula.missing")
    try:
        validate_base(invalid)
    except AssertionError:
        checks.append("undefined formula references are rejected")
    else:
        raise AssertionError("Undefined formula was accepted")
    invalid = copy.deepcopy(base)
    invalid["filters"] = {"and": ["true"], "or": ["false"]}
    try:
        validate_base(invalid)
    except AssertionError:
        checks.append("ambiguous multi-operator filter objects are rejected")
    else:
        raise AssertionError("Ambiguous filter was accepted")
    return {"status": "passed", "checks_passed": len(checks), "checks": checks,
            "scope": "synthetic fixture file checks only", "renderer_verified": False,
            "formula_evaluation_verified": False, "private_data_used": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("vault", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.vault)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered)
