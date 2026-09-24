#!/usr/bin/env python3
"""
Fetch LeetCode problem descriptions for IDs 1..100.

Output:
  descriptions/001-two-sum.md
  descriptions/002-add-two-numbers.md
  ...

If a matching problem folder exists, its README.md is also updated with a
"## Description" section. Existing sections are preserved.

Requirements:
  python -m pip install requests

Usage:
  python scripts/fetch_leetcode_descriptions.py
  python scripts/fetch_leetcode_descriptions.py --start 1 --end 100
  python scripts/fetch_leetcode_descriptions.py --no-readmes
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

GRAPHQL_URL = "https://leetcode.com/graphql"
PROBLEMSET_URL = "https://leetcode.com/api/problems/all/"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 LeetCode practice repo scraper",
    "Referer": "https://leetcode.com/problemset/",
}

QUESTION_QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionFrontendId
    title
    titleSlug
    difficulty
    content
  }
}
"""


def clean_html(raw: str) -> str:
    """Convert LeetCode HTML content to readable Markdown-ish text."""
    text = raw

    # Code blocks first, so their inner tags are not destroyed.
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


def slug_filename(problem_id: int, slug: str) -> str:
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


def update_readme(problem_id: int, description: str) -> bool:
    readme = ROOT / str(problem_id) / "README.md"
    if not readme.exists():
        return False

    original = readme.read_text(encoding="utf-8")
    heading = "## Description"
    block = f"{heading}\n\n{description.strip()}\n"

    start = original.find(heading)
    if start >= 0:
        next_heading = original.find("\n## ", start + len(heading))
        if next_heading >= 0:
            updated = original[:start] + block + original[next_heading + 1 :]
        else:
            updated = original[:start] + block
    else:
        separator = "" if original.endswith("\n\n") else "\n"
        updated = original + separator + block

    readme.write_text(updated.rstrip() + "\n", encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=100)
    parser.add_argument(
        "--no-readmes",
        action="store_true",
        help="Only create files in descriptions/; do not modify problem READMEs.",
    )
    args = parser.parse_args()

    if not 1 <= args.start <= args.end:
        parser.error("--start must be <= --end")

    print(f"Fetching LeetCode problems {args.start}..{args.end}...")

    session = requests.Session()

    try:
        problems = fetch_problem_list(session)
    except requests.RequestException as exc:
        print(f"ERROR: Could not fetch LeetCode problem list: {exc}", file=sys.stderr)
        return 1

    DESCRIPTION_DIR.mkdir(exist_ok=True)

    failed = []
    updated_readmes = 0

    for problem_id in range(args.start, args.end + 1):
        problem = problems.get(problem_id)

        if not problem:
            failed.append((problem_id, "problem ID not found"))
            continue

        try:
            question = fetch_question(session, problem["slug"])
            description = clean_html(question.get("content") or "")

            if not description:
                raise RuntimeError("empty description")

            output = DESCRIPTION_DIR / slug_filename(
                problem_id, question["titleSlug"]
            )

            front_matter = (
                f"# {question['questionFrontendId']}. {question['title']}\n\n"
                f"**Difficulty:** {question['difficulty']}\n\n"
            )
            output.write_text(
                front_matter + description + "\n",
                encoding="utf-8",
            )

            if not args.no_readmes and update_readme(problem_id, description):
                updated_readmes += 1

            print(f"[{problem_id:3}] {question['title']}")
            time.sleep(0.15)

        except (requests.RequestException, RuntimeError, KeyError) as exc:
            failed.append((problem_id, str(exc)))
            print(f"[{problem_id:3}] FAILED: {exc}", file=sys.stderr)

    print()
    print(f"Descriptions written: {args.end - args.start + 1 - len(failed)}")
    print(f"Problem READMEs updated: {updated_readmes}")

    if failed:
        print("\nFailures:")
        for problem_id, reason in failed:
            print(f"  {problem_id}: {reason}")
        return 1

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
