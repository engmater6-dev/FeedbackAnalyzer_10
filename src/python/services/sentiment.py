# -*- coding: utf-8 -*-
"""Rule-based sentiment classification (B-01 SSOT)."""
from constants import SENTIMENT_KEYWORDS
from text_utils import contains_any

__all__ = [
    "RuleBasedSentimentStrategy",
    "classify_sentiment",
]


class RuleBasedSentimentStrategy:
    """Keyword-order sentiment: 긍정 → 부정 → else 중립."""

    def classify(self, text: str) -> str:
        if contains_any(text, SENTIMENT_KEYWORDS["긍정"]):
            return "긍정"
        if contains_any(text, SENTIMENT_KEYWORDS["부정"]):
            return "부정"
        return "중립"


_default_strategy = RuleBasedSentimentStrategy()


def classify_sentiment(text: str) -> str:
    """Single source of truth for sentiment (B-01)."""
    return _default_strategy.classify(text)
