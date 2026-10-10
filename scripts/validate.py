#!/usr/bin/env python3
"""Offline, standard-library checks for the bulletin board publication candidate.

Passing checks are not human approval, source verification, or full secret scanning.
"""
from __future__ import annotations

import datetime as dt
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"
REQUIRED = ("README.md", "PUBLICATION.md", "_config.yml", "index.html", "about.md",
            "feed.xml", "_layouts/default.html", "_layouts/post.html", "assets/site.css")
SCANNED_SUFFIXES = {".html", ".xml", ".md", ".css", ".yml", ".py"}
issues: list[str] = []


def check(condition: bool, location: str, message: str) -> None:
    if not condition:
        issues.append(f"{location}: {message}")


for file in REQUIRED:
    check((ROOT / file).is_file(), file, "required file missing")
check(POSTS.is_dir(), "_posts", "posts directory missing")
posts = sorted(POSTS.glob("*.md")) if POSTS.is_dir() else []
check(bool(posts), "_posts", "no dated bulletins")

for post in posts:
    data = post.read_text(encoding="utf-8")
    name = post.name
    match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md", name)
    check(match is not None, name, "use YYYY-MM-DD-kebab-case.md")
    if match:
        try:
            dt.date(*map(int, match.groups()))
        except ValueError:
            issues.append(f"{name}: invalid filename date")
    check(data.startswith("---\n"), name, "front matter required")
    parts = data.split("---\n", 2)
    front = parts[1] if len(parts) >= 3 else ""
    body = parts[2] if len(parts) >= 3 else ""
    for key in ("layout", "title", "date", "author", "category", "summary"):
        check(re.search(rf"(?m)^{key}:\s*\S+", front) is not None, name,
              f"front matter {key!r} required")
    check(re.search(r"(?m)^layout:\s*post\s*$", front) is not None,
          name, "layout must be post")
    check(bool(body.strip()), name, "article body empty")
    check("https://www.anthropic.com/news/2026-usage-policy-update" in body
          if "anthropic" in name or "ai-safety" in name else True,
          name, "missing primary-source link")

# Broad leakage indicators only; this is not comprehensive content inspection.
BAD_PATTERNS = (
    (re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"), "private key marker"),
    (re.compile(r"\b(?:ghp|gho|github_pat)_[A-Za-z0-9_]{12,}"), "possible GitHub token"),
    (re.compile(r"(?i)\b(?:password|api[_-]?key|secret)\s*[:=]\s*[\"']?\S{12,}"), "possible secret"),
)
for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts or path.suffix not in SCANNED_SUFFIXES:
        continue
    rel = path.relative_to(ROOT).as_posix()
    if rel == "scripts/validate.py":
        # Checking the detector against itself would flag its example expressions.
        continue
    content = path.read_text(encoding="utf-8")
    for pattern, message in BAD_PATTERNS:
        check(pattern.search(content) is None, rel, message)
    if path.suffix in (".md", ".html", ".xml"):
        check("http://" not in content.replace("http://www.w3.org/2005/Atom", ""), rel, "non-HTTPS link present")

if issues:
    print("FAIL — bulletin board candidate validation")
    for issue in issues:
        print(" -", issue)
    sys.exit(1)
print(f"PASS — {len(posts)} bulletin(s), required files and bounded leakage heuristics checked")
print("Human editorial, privacy, attribution, and publication gates still required.")
