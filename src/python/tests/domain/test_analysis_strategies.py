# -*- coding: utf-8 -*-
import pytest
from analysis_strategies import (
    RuleBasedSentimentStrategy,
    RuleBasedCategoryStrategy,
    classify_sentiment,
    matches_category,
)


@pytest.mark.domain
class TestAnalysisStrategies:
    def test_sentiment_strategy_anchor(self):
        text = "배송이 너무 늦어요. 화가 납니다."
        assert RuleBasedSentimentStrategy().classify(text) == "부정"
        assert classify_sentiment(text) == "부정"

    def test_category_strategy_main_only(self):
        assert RuleBasedCategoryStrategy().matches("품질", "품질") is True
        assert matches_category("품질", "품질") is True
