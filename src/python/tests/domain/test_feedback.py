# -*- coding: utf-8 -*-
import pytest
from feedback import Feedback
from services.analysis_service import TextAnalyzer


@pytest.mark.domain
class TestFeedback:
    def test_text_property(self):
        fb = Feedback("hello")
        assert fb.text == "hello"

    def test_sentiment_category_setters(self):
        fb = Feedback("x")
        assert fb.sentiment is None
        assert fb.category is None
        fb.sentiment = "부정"
        fb.category = "배송"
        assert fb.sentiment == "부정"
        assert fb.category == "배송"

    def test_optional_init(self):
        fb = Feedback("x", sentiment="긍정", category="품질")
        assert fb.sentiment == "긍정"
        assert fb.category == "품질"

    def test_annotation_after_analyze(self):
        fb = Feedback("배송이 너무 늦어요. 화가 납니다.")
        TextAnalyzer().analyze_sentiments([fb])
        assert fb.sentiment == "부정"
        TextAnalyzer().analyze_keywords([fb])
        assert fb.category == "배송"
