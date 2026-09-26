# LeetCode Practice & Automated Verification

Solutions to LeetCode problems in **C++17**, **Java 11+**, and **Python 3**.

The repository is organized by problem number. Each completed problem contains a solution, complexity notes, edge-case considerations, and automated verification tests.

## Progress

Progress toward 100 problems

**10 / 100 — 1%**

## Repository Structure

```text
.
├── 1/
│   ├── 1.cpp
│   ├── Solution1.java
│   └── 1.py
├── tests/
│   ├── test.py
├── .vscode/
│   └── tasks.json
├── verify.py
└── README.md
```

## Verification

From the repository root:

```bash
python3 verify.py
```

This runs the Python, C++, and Java tests.

In VS Code, run **Terminal → Run Task → LeetCode: verify all**.

## Requirements

- C++17 compiler (`g++`)
- Java 11+
- Python 3
- `pytest`

Install pytest if needed:

```bash
python3 -m pip install pytest
```

## Concepts Covered

- Arrays
- Hash maps / hash tables
- One-pass lookup
- Time/space complexity analysis
- Edge-case testing
