#!/usr/bin/env python3
"""Validate a local skill library without modifying it. License: MIT."""
from pathlib import Path
import argparse
import json
import os
import re
import sys

ID_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
REPO_RE = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
PIN_RE = re.compile(r"[0-9a-fA-F]{40}\Z")
FORBIDDEN_DIRS = {"node_modules", "venv", ".venv", "virtualenv", "__pycache__", ".npm", ".cache"}
CREDENTIAL_FILES = {".env", ".npmrc", ".pypirc", ".netrc", "credentials.json", "secrets.json", "token.json", "id_rsa", "id_ed25519", "id_ecdsa"}
FORBIDDEN_SUFFIXES = {".p12", ".pfx", ".key", ".exe", ".dll", ".pyd", ".so", ".dylib"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico"}
SECRET_PATTERNS = [
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("API token", re.compile(r"\bsk-(?:proj-|ant-[A-Za-z0-9-]*-)?[A-Za-z0-9_-]{24,}\b")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
]
LOCAL_PATH_PATTERNS = [
    re.compile(r"(?<![A-Za-z0-9])(?:[A-Za-z]:[\\/]+)(?:Users|CodexHome|OneDrive|npm-global|Obsidian)(?:[\\/]+|\b)", re.I),
    re.compile(r"(?<![A-Za-z0-9/])/(?:Users|home)/[A-Za-z0-9._-]+(?:/|\b)"),
]


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def resolve_local(root, value):
    if not nonempty(value) or ":" in value or "\\" in value:
        raise ValueError("expected a repository-relative slash-separated path")
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("path escapes the repository")
    result = (root / relative).resolve()
    if not result.is_relative_to(root):
        raise ValueError("path escapes the repository")
    return result


def scalar(frontmatter, key):
    match = re.search(rf"^{re.escape(key)}:[ \t]*(.*)$", frontmatter, re.M)
    if not match:
        return None
    value = match.group(1).strip()
    if value in {"|", ">", "|-", ">-", "|+", ">+"}:
        rest = frontmatter[match.end():].splitlines()
        lines = []
        for line in rest:
            if line and not line[0].isspace():
                break
            if line.strip():
                lines.append(line.strip())
        return " ".join(lines)
    return value.strip("\"'")


def validate(root, catalog_path):
    errors = []
    scanned = 0
    binary_assets = 0
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        return {"status": "failed", "errors": [f"Cannot read catalog: {type(exc).__name__}"], "skills_checked": 0}
    if not isinstance(catalog, dict) or catalog.get("schema_version") != 1:
        errors.append("catalog: schema_version must be 1")
    if not isinstance(catalog, dict):
        return {"status": "failed", "errors": errors, "skills_checked": 0}
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(catalog.get("validated_at", ""))):
        errors.append("catalog: validated_at must use YYYY-MM-DD")
    skills = catalog.get("skills")
    if not isinstance(skills, list):
        return {"status": "failed", "errors": errors + ["catalog: skills must be an array"], "skills_checked": 0}
    ids = set()
    for index, item in enumerate(skills):
        label = f"skills[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label}: must be an object")
            continue
        identifier = item.get("id", "")
        if not isinstance(identifier, str) or not ID_RE.fullmatch(identifier):
            errors.append(f"{label}: invalid skill id")
            continue
        label = identifier
        if identifier in ids:
            errors.append(f"{label}: duplicate catalog id")
        ids.add(identifier)
        for field in ("category", "license", "status"):
            if not nonempty(item.get(field)):
                errors.append(f"{label}: missing {field}")
        upstream = item.get("upstream", {})
        if not isinstance(upstream, dict):
            errors.append(f"{label}: upstream must be an object")
            upstream = {}
        if not isinstance(upstream.get("repository"), str) or not REPO_RE.fullmatch(upstream["repository"]):
            errors.append(f"{label}: upstream.repository must be owner/repository")
        if not isinstance(upstream.get("commit"), str) or not PIN_RE.fullmatch(upstream["commit"]):
            errors.append(f"{label}: upstream.commit must be a full 40-hex pin")
        for field in ("path", "fork"):
            if not nonempty(upstream.get(field)):
                errors.append(f"{label}: missing upstream.{field}")
        folder = root / "skills" / identifier
        entry = folder / "SKILL.md"
        if not entry.is_file():
            errors.append(f"{label}: missing SKILL.md")
        else:
            text = entry.read_text(encoding="utf-8-sig")
            front = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
            if not front:
                errors.append(f"{label}: missing YAML frontmatter")
            else:
                if scalar(front.group(1), "name") != identifier:
                    errors.append(f"{label}: frontmatter name must match catalog id")
                if not nonempty(scalar(front.group(1), "description")):
                    errors.append(f"{label}: missing frontmatter description")
        if not any((folder / name).is_file() for name in ("LICENSE", "LICENSE.txt", "LICENSE.md")):
            errors.append(f"{label}: missing retained license file")
        if not (folder / "PROVENANCE.md").is_file():
            errors.append(f"{label}: missing PROVENANCE.md")
        validation = item.get("validation", {})
        if not isinstance(validation, dict) or not nonempty(validation.get("summary")):
            errors.append(f"{label}: missing validation.summary")
        try:
            report = resolve_local(root, validation.get("report") if isinstance(validation, dict) else None)
            if not report.is_file():
                raise ValueError("file does not exist")
        except ValueError as exc:
            errors.append(f"{label}: validation.report {exc}")
    skills_dir = root / "skills"
    present = {p.name for p in skills_dir.iterdir() if p.is_dir()} if skills_dir.is_dir() else set()
    for name in sorted(present - ids):
        errors.append(f"{name}: skill directory missing from catalog")
    for directory, dirs, files in os.walk(root, followlinks=False):
        current = Path(directory)
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in list(dirs):
            path = current / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink() or name.lower() in FORBIDDEN_DIRS:
                errors.append(f"{relative}: symlink or generated dependency directory")
                dirs.remove(name)
        for name in files:
            if name == ".git":
                continue
            path = current / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                errors.append(f"{relative}: symlink is not permitted")
                continue
            lower = name.lower()
            if lower in CREDENTIAL_FILES or path.suffix.lower() in FORBIDDEN_SUFFIXES or (lower.startswith('.env.') and not lower.endswith(('.example', '.sample', '.template'))):
                errors.append(f"{relative}: credential or runtime binary filename")
            data = path.read_bytes()
            if path.suffix.lower() in IMAGE_SUFFIXES:
                binary_assets += 1
                continue
            try:
                content = data.decode("utf-8-sig")
            except UnicodeDecodeError:
                errors.append(f"{relative}: unexpected non-UTF-8 binary file")
                continue
            scanned += 1
            for kind, pattern in SECRET_PATTERNS:
                if pattern.search(content):
                    errors.append(f"{relative}: possible {kind} (value redacted)")
            if any(pattern.search(content) for pattern in LOCAL_PATH_PATTERNS):
                errors.append(f"{relative}: hardcoded local user or installation path")
    return {"status": "failed" if errors else "passed", "skills_checked": len(ids),
            "text_files_scanned": scanned, "image_assets_not_text_scanned": binary_assets,
            "errors": errors, "scope": "structural and heuristic checks; not a complete security audit"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--catalog", default="catalog.json")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        report = validate(root, resolve_local(root, args.catalog))
    except (OSError, ValueError, UnicodeError):
        report = {"status": "failed", "errors": ["Cannot read one or more local files"], "skills_checked": 0}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
