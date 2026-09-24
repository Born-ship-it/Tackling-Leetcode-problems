# Fetching LeetCode descriptions

This repo includes a small scraper that fetches the descriptions for LeetCode
problem IDs 1 through 100 from LeetCode's GraphQL endpoint.

## Setup

From the repository root:

```powershell
python -m pip install -r scripts/requirements.txt
```

## Fetch all first 100

```powershell
python scripts/fetch_leetcode_descriptions.py
```

This creates:

```text
descriptions/
├── 001-two-sum.md
├── 002-add-two-numbers.md
├── ...
└── 100-*.md
```

If a matching problem folder already exists, for example `1/README.md`, the
script also replaces/adds that README's `## Description` section.

Your existing solution, complexity, edge-case, and verification sections are
left untouched.

## Fetch only a range

```powershell
python scripts/fetch_leetcode_descriptions.py --start 1 --end 10
```

## Only generate description files

```powershell
python scripts/fetch_leetcode_descriptions.py --no-readmes
```

## Notes

- The script uses problem IDs 1 through 100, not the first 100 entries in the
  current LeetCode problemset ordering.
- Re-running the script is safe; description files are regenerated and README
  Description sections are replaced rather than duplicated.
- Internet access is required.
