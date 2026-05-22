# -*- coding: utf-8 -*-
"""
Generate or refresh tests/golden_master_expected.txt (Golden Master baseline).

Usage (from src/python):
    python scripts/generate_golden_master.py
    python scripts/generate_golden_master.py --check   # compare only, no write

After intentional output changes:
    python scripts/generate_golden_master.py --force
    git add tests/golden_master_expected.txt
"""
from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tests.golden_master_capture import capture_golden_master_output  # noqa: E402

GOLDEN_PATH = ROOT / "tests" / "golden_master_expected.txt"


def main() -> int:
    parser = argparse.ArgumentParser(description="Golden Master baseline generator")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing golden_master_expected.txt",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if actual differs from baseline (no write)",
    )
    args = parser.parse_args()

    actual = capture_golden_master_output()

    if not GOLDEN_PATH.exists():
        GOLDEN_PATH.write_text(actual, encoding="utf-8")
        print(f"Created baseline: {GOLDEN_PATH}")
        print("Run: git add tests/golden_master_expected.txt")
        return 0

    expected = GOLDEN_PATH.read_text(encoding="utf-8")
    if actual == expected:
        print(f"OK: baseline matches ({GOLDEN_PATH})")
        return 0

    if args.check or not args.force:
        print(f"MISMATCH: {GOLDEN_PATH}", file=sys.stderr)
        diff = difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile="expected (golden_master_expected.txt)",
            tofile="actual (current capture)",
        )
        sys.stderr.writelines(diff)
        if not args.force:
            print(
                "\nTo approve new baseline: python scripts/generate_golden_master.py --force",
                file=sys.stderr,
            )
            return 1

    GOLDEN_PATH.write_text(actual, encoding="utf-8")
    print(f"Updated baseline: {GOLDEN_PATH}")
    print("Run: git add tests/golden_master_expected.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
