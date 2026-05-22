# -*- coding: utf-8 -*-
"""Compatibility shim — use services.sentiment / services.category in new code."""
from services.category import RuleBasedCategoryStrategy, matches_category
from services.sentiment import RuleBasedSentimentStrategy, classify_sentiment

__all__ = [
    "RuleBasedSentimentStrategy",
    "RuleBasedCategoryStrategy",
    "classify_sentiment",
    "matches_category",
]
