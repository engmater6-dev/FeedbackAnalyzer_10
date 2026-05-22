# -*- coding: utf-8 -*-
from pathlib import Path

import pytest
from services.csv_parser import parse_csv_content
from services.trend_csv_parser import (
    is_trend_csv,
    parse_trend_csv_to_feedbacks,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
TREND_CSV = REPO_ROOT / "sample" / "test_feedback_trend.csv"


@pytest.mark.domain
class TestTrendCsvParser:
    def test_is_trend_csv_true_for_date_text_header(self):
        content = "date,text\n2026-01-01,hello\n"
        assert is_trend_csv(content) is True

    def test_is_trend_csv_false_for_text_only(self):
        content = "text\nhello\n"
        assert is_trend_csv(content) is False

    def test_parse_trend_sets_recorded_at(self):
        content = "date,text\n2026-02-01,최고입니다\n"
        rows = parse_trend_csv_to_feedbacks(content)
        assert len(rows) == 1
        assert rows[0].recorded_at == "2026-02-01"
        assert rows[0].text == "최고입니다"

    def test_invalid_date_ignored_text_kept(self):
        content = "date,text\nbad-date,안녕\n"
        rows = parse_trend_csv_to_feedbacks(content)
        assert len(rows) == 1
        assert rows[0].recorded_at is None

    def test_sample_file_via_parse_csv_content(self):
        content = TREND_CSV.read_text(encoding="utf-8")
        rows = parse_csv_content(content)
        assert len(rows) >= 12
        assert sum(1 for fb in rows if fb.recorded_at) >= 12
