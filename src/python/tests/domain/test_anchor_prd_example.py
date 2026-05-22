# -*- coding: utf-8 -*-
"""
Anchor: PRD / Mom Test §3.1
입력: "배송이 너무 늦어요. 화가 납니다."
기대: sent → 부정 1, kw → 배송 1, filter(부정, 배송) ≥ 1, 분석·필터 일관
"""
import pytest
from feedback import Feedback
from text_analyzer import TextAnalyzer
from filters import filter_feedbacks


ANCHOR_TEXT = "배송이 너무 늦어요. 화가 납니다."


@pytest.fixture
def anchor_feedbacks():
    return [Feedback(ANCHOR_TEXT)]


@pytest.mark.p0
@pytest.mark.red
@pytest.mark.domain
class TestAnchorPrdExample:
    """test_plan TP-ANCHOR-01 ~ 04"""

    def test_sent_classifies_anchor_as_negative(self, anchor_feedbacks):
        result = TextAnalyzer().analyze_sentiments(anchor_feedbacks)

        assert result["부정"] == 1
        assert result["중립"] == 0
        assert result["긍정"] == 0

    def test_kw_classifies_anchor_as_shipping(self, anchor_feedbacks):
        result = TextAnalyzer().analyze_keywords(anchor_feedbacks)

        assert result["배송"] == 1

    def test_filter_negative_and_shipping_returns_at_least_one(
        self, anchor_feedbacks
    ):
        result = filter_feedbacks(anchor_feedbacks, "부정", "배송")

        assert len(result) >= 1
        assert result[0].text == ANCHOR_TEXT

    def test_sent_negative_count_matches_filter_negative_all(
        self, anchor_feedbacks
    ):
        sent_result = TextAnalyzer().analyze_sentiments(anchor_feedbacks)
        filtered = filter_feedbacks(anchor_feedbacks, "부정", "전체")

        assert sent_result["부정"] == len(filtered)
