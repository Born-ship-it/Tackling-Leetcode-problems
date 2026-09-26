#!/usr/bin/env python3
"""
Fetch LeetCode official Solution Article/editorial content for problem IDs 1..100.

Output:
    editorial/001-two-sum.md
    editorial/002-add-two-numbers.md
    ...

The script uses LeetCode's GraphQL question query and requests the official
solution content exposed for each problem. Problems without an accessible
official solution are reported and skipped.

Usage:
    python scripts/fetch_leetcode_editorials.py
    python scripts/fetch_leetcode_editorials.py --start 1 --end 100
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTION_DIR = ROOT / "descriptions"
EDITORIAL_DIR = ROOT / "editorial"

GRAPHQL_URL = "https://leetcode.com/graphql"
PROBLEMSET_URL = "https://leetcode.com/api/problems/all/"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 LeetCode practice repo editorial scraper",
    "Referer": "https://leetcode.com/problemset/",
}

QUESTION_QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionFrontendId
    title
    titleSlug
    difficulty
    solution {
      id
      canSeeDetail
      content
      paidOnly
      rating
      ratingCount
    }
  }
}
"""


def clean_html(raw: str) -> str:
    """Convert LeetCode editorial HTML into readable Markdown-ish text."""
    text = raw

    # Preserve pre/code blocks before stripping tags.
    text = re.sub(
        r"<pre[^>]*><code[^>]*>(.*?)</code></pre>",
        lambda m: "\n```\n"
        + html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        + "\n```\n",
        text,
        flags=re.I | re.S,
    )

    replacements = [
        (r"<br\s*/?>", "\n"),
        (r"</p\s*>", "\n\n"),
        (r"<p[^>]*>", ""),
        (r"<li[^>]*>", "- "),
        (r"</li\s*>", "\n"),
        (r"<strong[^>]*>(.*?)</strong>", r"**\1**"),
        (r"<b[^>]*>(.*?)</b>", r"**\1**"),
        (r"<em[^>]*>(.*?)</em>", r"*\1*"),
        (r"<i[^>]*>(.*?)</i>", r"*\1*"),
        (r"<code[^>]*>(.*?)</code>", r"`\1`"),
        (r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', r"[\2](\1)"),
        (r"<h1[^>]*>(.*?)</h1>", r"\n\n# \1\n\n"),
        (r"<h2[^>]*>(.*?)</h2>", r"\n\n## \1\n\n"),
        (r"<h3[^>]*>(.*?)</h3>", r"\n\n### \1\n\n"),
        (r"<h4[^>]*>(.*?)</h4>", r"\n\n#### \1\n\n"),
    ]

    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.I | re.S)

    text = re.sub(r"<img[^>]*>", "", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)

    text = html.unescape(text).replace("\xa0", " ")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def filename(problem_id: int, slug: str) -> str:
    clean = re.sub(r"[^a-zA-Z0-9_-]+", "-", slug.lower()).strip("-")
    return f"{problem_id:03d}-{clean}.md"


def fetch_problem_list(session: requests.Session) -> dict[int, dict]:
    response = session.get(PROBLEMSET_URL, headers=HEADERS, timeout=30)
    response.raise_for_status()

    result = {}
    for item in response.json().get("stat_status_pairs", []):
        stat = item.get("stat", {})
        raw_id = stat.get("frontend_question_id")
        slug = stat.get("question__title_slug")

        if raw_id and slug and str(raw_id).isdigit():
            result[int(raw_id)] = {
                "id": int(raw_id),
                "slug": slug,
                "title": stat.get("question__title", ""),
            }

    return result


def fetch_question(session: requests.Session, slug: str) -> dict:
    payload = {
        "operationName": "questionData",
        "variables": {"titleSlug": slug},
        "query": QUESTION_QUERY,
    }

    response = session.post(
        GRAPHQL_URL,
        json=payload,
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()
    if data.get("errors"):
        raise RuntimeError(str(data["errors"]))

    question = (data.get("data") or {}).get("question")
    if not question:
        raise RuntimeError(f"No question returned for '{slug}'")

    return question


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=100)
    args = parser.parse_args()

    if not 1 <= args.start <= args.end:
        parser.error("--start must be <= --end")

    EDITORIAL_DIR.mkdir(exist_ok=True)

    session = requests.Session()

    print(f"Fetching official editorials for problems {args.start}..{args.end}...")

    try:
        problems = fetch_problem_list(session)
    except requests.RequestException as exc:
        print(f"ERROR: Could not fetch LeetCode problem list: {exc}", file=sys.stderr)
        return 1

    failed = []
    skipped = []

    for problem_id in range(args.start, args.end + 1):
        problem = problems.get(problem_id)

        if not problem:
            failed.append((problem_id, "problem ID not found"))
            continue

        try:
            question = fetch_question(session, problem["slug"])
            solution = question.get("solution")

            if not solution:
                skipped.append((problem_id, "no official solution exposed"))
                print(f"[{problem_id:3}] SKIPPED: no official solution")
                continue

            if solution.get("paidOnly"):
                skipped.append((problem_id, "official solution is marked paid-only"))
                print(f"[{problem_id:3}] SKIPPED: official solution is paid-only")
                continue

            if solution.get("canSeeDetail") is False:
                skipped.append((problem_id, "official solution detail is not accessible"))
                print(f"[{problem_id:3}] SKIPPED: solution detail not accessible")
                continue

            content = solution.get("content") or ""
            if not content.strip():
                skipped.append((problem_id, "official solution has no content"))
                print(f"[{problem_id:3}] SKIPPED: empty solution content")
                continue

            markdown = clean_html(content)
            output = EDITORIAL_DIR / filename(
                problem_id, question["titleSlug"]
            )

            header = (
                f"# {question['questionFrontendId']}. {question['title']} — "
                f"Official Editorial\n\n"
                f"**Difficulty:** {question['difficulty']}\n\n"
                f"**Source:** https://leetcode.com/problems/"
                f"{question['titleSlug']}/\n\n"
                f"---\n\n"
            )

            output.write_text(header + markdown + "\n", encoding="utf-8")
            print(f"[{problem_id:3}] {question['title']}")
            time.sleep(0.15)

        except (requests.RequestException, RuntimeError, KeyError) as exc:
            failed.append((problem_id, str(exc)))
            print(f"[{problem_id:3}] FAILED: {exc}", file=sys.stderr)

    print()
    print(f"Editorials written: {args.end - args.start + 1 - len(skipped) - len(failed)}")
    print(f"Skipped: {len(skipped)}")
    print(f"Failures: {len(failed)}")

    if skipped:
        print("\nSkipped problems:")
        for problem_id, reason in skipped:
            print(f"  {problem_id}: {reason}")

    if failed:
        print("\nFailures:")
        for problem_id, reason in failed:
            print(f"  {problem_id}: {reason}")
        return 1

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
