# -*- coding: utf-8 -*-
"""Rule-based sentiment classification (B-01 SSOT, R-10 DB)."""
from typing import Dict, List, Optional

from services.keyword_db import get_sentiment_keyword_map
from text_utils import contains_any

__all__ = [
    "RuleBasedSentimentStrategy",
    "classify_sentiment",
    "invalidate_sentiment_cache",
]

_keyword_cache: Optional[Dict[str, List[str]]] = None


def invalidate_sentiment_cache() -> None:
    global _keyword_cache
    _keyword_cache = None


def _sentiment_keywords() -> Dict[str, List[str]]:
    global _keyword_cache
    if _keyword_cache is None:
        _keyword_cache = get_sentiment_keyword_map()
    return _keyword_cache


class RuleBasedSentimentStrategy:
    """Keyword-order sentiment: 긍정 → 부정 → else 중립."""

    def classify(self, text: str) -> str:
        keywords = _sentiment_keywords()
        if contains_any(text, keywords["긍정"]):
            return "긍정"
        if contains_any(text, keywords["부정"]):
            return "부정"
        return "중립"


_default_strategy = RuleBasedSentimentStrategy()


def classify_sentiment(text: str) -> str:
    """Single source of truth for sentiment (B-01, DB-backed)."""
    return _default_strategy.classify(text)
