#!/usr/bin/env python3
"""Run all available LeetCode verification tests."""

from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent


def run(command, cwd=ROOT):
    print("$", " ".join(map(str, command)))
    subprocess.run(command, cwd=cwd, check=True)


def main():
    # Python
    run([sys.executable, "-m", "pytest", "tests/test_1.py", "-q"])

    # C++
    with tempfile.TemporaryDirectory() as tmp:
        exe = Path(tmp) / "two_sum_cpp_tests"
        run(["g++", "-std=c++17", "-Wall", "-Wextra", "-pedantic",
             "tests/1_test.cpp", "-o", str(exe)])
        run([str(exe)])

    # Java
    with tempfile.TemporaryDirectory() as tmp:
        run(["javac", "-d", tmp, "1/Solution1.java", "tests/Solution1Test.java"])
        run(["java", "-cp", tmp, "Solution1Test"])

    print("\nAll LeetCode verification tests passed.")


if __name__ == "__main__":
    main()
