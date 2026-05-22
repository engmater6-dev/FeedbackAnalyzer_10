# -*- coding: utf-8 -*-
from pathlib import Path

import pytest
from services.analysis_service import TextAnalyzer
from services.csv_parser import parse_csv_content
from services.trend_service import (
    aggregate_sentiment_by_month,
    build_trend_results,
    has_trend_data,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
TREND_CSV = REPO_ROOT / "sample" / "test_feedback_trend.csv"
ANCHOR_TEXT = "배송이 너무 늦어요. 화가 납니다."


@pytest.mark.domain
class TestTrendService:
    def test_has_trend_data_false_without_dates(self):
        from feedback import Feedback

        assert has_trend_data([Feedback("hello")]) is False

    def test_aggregate_sentiment_by_month(self):
        feedbacks = parse_csv_content(TREND_CSV.read_text(encoding="utf-8"))
        TextAnalyzer().analyze_sentiments(feedbacks)
        by_month = aggregate_sentiment_by_month(feedbacks)
        assert len(by_month) >= 3
        assert sum(sum(m.values()) for m in by_month.values()) == len(feedbacks)

    def test_january_includes_negative_anchor(self):
        feedbacks = parse_csv_content(TREND_CSV.read_text(encoding="utf-8"))
        TextAnalyzer().analyze_sentiments(feedbacks)
        by_month = aggregate_sentiment_by_month(feedbacks)
        assert by_month.get("2026-01", {}).get("부정", 0) >= 1

    def test_build_trend_results_empty_for_manual_input(self):
        from feedback import Feedback

        fb = Feedback(ANCHOR_TEXT)
        TextAnalyzer().analyze_sentiments([fb])
        sent_trend, kw_trend = build_trend_results([fb])
        assert sent_trend == {}
        assert kw_trend == {}

    def test_build_trend_results_after_sample_upload(self):
        feedbacks = parse_csv_content(TREND_CSV.read_text(encoding="utf-8"))
        analyzer = TextAnalyzer()
        analyzer.analyze_sentiments(feedbacks)
        analyzer.analyze_keywords(feedbacks)
        sent_trend, kw_trend = build_trend_results(feedbacks)
        assert "2026-01" in sent_trend
        assert "2026-02" in sent_trend
        assert "2026-03" in sent_trend
        assert sent_trend["2026-01"]["부정"] >= 1
        assert any(sum(m.values()) > 0 for m in kw_trend.values())
