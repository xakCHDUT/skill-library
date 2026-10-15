#!/usr/bin/env python3
"""Read public GitHub default-branch heads; never install, merge or push. MIT."""
from pathlib import Path
import argparse
import datetime
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
COMMIT = re.compile(r"[0-9a-fA-F]{40}\Z")


def get_json(url, timeout):
    request = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "skill-library-upstream-check/1.0",
        "X-GitHub-Api-Version": "2022-11-28",
    }, method="GET")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def check(catalog, timeout=15, fetch=get_json):
    grouped = {}
    for item in catalog.get("skills", []):
        upstream = item.get("upstream", {})
        repository = upstream.get("repository", "")
        pin = upstream.get("commit", "")
        if not isinstance(repository, str) or not REPOSITORY.fullmatch(repository):
            raise ValueError("upstream.repository must be owner/repository")
        if not isinstance(pin, str) or not COMMIT.fullmatch(pin):
            raise ValueError("upstream.commit must be a full 40-hex pin")
        grouped.setdefault(repository, []).append((item.get("id"), pin.lower()))
    results = []
    for repository, skills in sorted(grouped.items()):
        base = f"https://api.github.com/repos/{repository}"
        result = {"repository": repository}
        try:
            metadata = fetch(base, timeout)
            branch = metadata.get("default_branch")
            if not isinstance(branch, str) or not branch:
                raise ValueError("Repository has no default branch")
            head = fetch(base + "/commits/" + urllib.parse.quote(branch, safe=""), timeout)
            sha = head.get("sha", "")
            if not isinstance(sha, str) or not COMMIT.fullmatch(sha):
                raise ValueError("Unexpected commit response")
            result.update({"status": "checked", "default_branch": branch, "head": sha,
                           "archived": metadata.get("archived", False),
                           "skills": [{"id": identifier, "pinned_commit": pin,
                                       "head_differs": pin != sha.lower(),
                                       "compare_url": f"https://github.com/{repository}/compare/{pin}...{sha}"}
                                      for identifier, pin in skills]})
        except urllib.error.HTTPError as exc:
            result.update(status="error", error=f"GitHub HTTP {exc.code}; public API may be unavailable or rate-limited")
        except (urllib.error.URLError, TimeoutError, OSError):
            result.update(status="error", error="Network request failed or timed out")
        except (ValueError, TypeError, AttributeError):
            result.update(status="error", error="Unexpected GitHub API response")
        results.append(result)
    return {"checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "mode": "read_only", "repositories": results,
            "note": "A different HEAD is a review signal, not a recommendation to upgrade. No files or remote refs were changed."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=Path(__file__).resolve().parents[1] / "catalog.json")
    parser.add_argument("--timeout", type=int, default=15)
    args = parser.parse_args()
    if not 1 <= args.timeout <= 60:
        parser.error("--timeout must be between 1 and 60 seconds")
    try:
        catalog = json.loads(args.catalog.read_text(encoding="utf-8-sig"))
        if not isinstance(catalog, dict) or catalog.get("schema_version") != 1 or not isinstance(catalog.get("skills"), list):
            raise ValueError("Unsupported catalog schema")
        report = check(catalog, timeout=args.timeout)
    except (OSError, ValueError, TypeError, AttributeError):
        print(json.dumps({"mode": "read_only", "error": "Cannot read a valid catalog"}, indent=2))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if any(row["status"] == "error" for row in report["repositories"]) else 0


if __name__ == "__main__":
    sys.exit(main())
