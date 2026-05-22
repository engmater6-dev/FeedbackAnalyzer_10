# -*- coding: utf-8 -*-
"""Phase 5-1: sample/test_feedback_trend.csv existence and B-04 text parsing."""
from pathlib import Path

import pytest
from app import _parse_csv_to_feedbacks

REPO_ROOT = Path(__file__).resolve().parents[4]
TREND_CSV = REPO_ROOT / "sample" / "test_feedback_trend.csv"
ANCHOR_TEXT = "배송이 너무 늦어요. 화가 납니다."
MIN_DATA_ROWS = 12


@pytest.mark.domain
class TestSampleTrendCsv:
    def test_trend_csv_file_exists(self):
        assert TREND_CSV.is_file(), f"missing: {TREND_CSV}"

    def test_trend_csv_header_and_row_count(self):
        lines = TREND_CSV.read_text(encoding="utf-8").strip().splitlines()
        assert lines[0].strip().lower() == "date,text"
        data_rows = [line for line in lines[1:] if line.strip()]
        assert len(data_rows) >= MIN_DATA_ROWS

    def test_trend_csv_parses_text_column_via_standard_parser(self):
        content = TREND_CSV.read_text(encoding="utf-8")
        feedbacks = _parse_csv_to_feedbacks(content)
        assert len(feedbacks) >= MIN_DATA_ROWS
        texts = [fb.text for fb in feedbacks]
        assert ANCHOR_TEXT in texts

    def test_trend_csv_covers_three_months(self):
        lines = TREND_CSV.read_text(encoding="utf-8").strip().splitlines()[1:]
        months = {line.split(",", 1)[0][:7] for line in lines if line.strip()}
        assert len(months) >= 3
