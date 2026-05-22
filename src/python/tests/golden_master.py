# -*- coding: utf-8 -*-
"""Golden Master (Approval) compare helpers for pytest."""
from __future__ import annotations

import difflib
from pathlib import Path

import pytest

from tests.golden_master_capture import capture_golden_master_output

GOLDEN_PATH = Path(__file__).resolve().parent / "golden_master_expected.txt"


def approve_golden_master(
    actual: str | None = None,
    *,
    golden_path: Path = GOLDEN_PATH,
) -> None:
    """
    Approve pattern:
      - No baseline file → write `actual` and fail (review + git add).
      - Baseline exists → strict string compare; diff + FAIL on mismatch.
    """
    if actual is None:
        actual = capture_golden_master_output()

    if not golden_path.exists():
        golden_path.write_text(actual, encoding="utf-8")
        pytest.fail(
            f"Golden Master baseline created at {golden_path.name}. "
            "Review the file, then: git add tests/golden_master_expected.txt "
            "and re-run pytest."
        )

    expected = golden_path.read_text(encoding="utf-8")
    if actual == expected:
        return

    diff_lines = difflib.unified_diff(
        expected.splitlines(keepends=True),
        actual.splitlines(keepends=True),
        fromfile=f"expected ({golden_path.name})",
        tofile="actual (current capture)",
    )
    diff_text = "".join(diff_lines)
    pytest.fail(
        "Golden Master mismatch.\n"
        f"Update baseline: python scripts/generate_golden_master.py --force\n\n"
        f"{diff_text}"
    )
