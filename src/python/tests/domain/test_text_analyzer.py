# -*- coding: utf-8 -*-
import pytest
from feedback import Feedback
from text_analyzer import TextAnalyzer, classify_sentiment, matches_category


@pytest.mark.domain
class TestTextAnalyzerUnit:
    def test_classify_positive(self):
        assert classify_sentiment("최고입니다 정말 좋아요") == "긍정"

    def test_classify_neutral(self):
        assert classify_sentiment("보통이에요") == "중립"

    def test_matches_category_unknown(self):
        assert matches_category("배송", "없는카테고리") is False

    def test_kw_counts_multiple_categories(self):
        feedbacks = [Feedback("배송도 늦고 품질도 나쁩니다")]
        result = TextAnalyzer().analyze_keywords(feedbacks)
        assert result["배송"] >= 1
        assert result["품질"] >= 1
