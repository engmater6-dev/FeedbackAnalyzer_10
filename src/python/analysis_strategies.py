# -*- coding: utf-8 -*-
"""Rule-based analysis strategies (Phase 3-C-7)."""
from constants import SENTIMENT_KEYWORDS, CATEGORY_KEYWORDS
from text_utils import contains_any


class RuleBasedSentimentStrategy:
    """Keyword-order sentiment: 긍정 → 부정 → else 중립."""

    def classify(self, text: str) -> str:
        if contains_any(text, SENTIMENT_KEYWORDS["긍정"]):
            return "긍정"
        if contains_any(text, SENTIMENT_KEYWORDS["부정"]):
            return "부정"
        return "중립"


class RuleBasedCategoryStrategy:
    """Category match via main keywords only (ADR-001)."""

    def matches(self, text: str, category: str) -> bool:
        sub_map = CATEGORY_KEYWORDS.get(category)
        if not sub_map or "main" not in sub_map:
            return False
        return contains_any(text, sub_map["main"])


_default_sentiment_strategy = RuleBasedSentimentStrategy()
_default_category_strategy = RuleBasedCategoryStrategy()


def classify_sentiment(text: str) -> str:
    """Single source of truth for sentiment (B-01)."""
    return _default_sentiment_strategy.classify(text)


def matches_category(text: str, category: str) -> bool:
    """Single source of truth for category (B-02)."""
    return _default_category_strategy.matches(text, category)
