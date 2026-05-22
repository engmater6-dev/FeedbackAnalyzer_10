# -*- coding: utf-8 -*-
from typing import List, Dict
from feedback import Feedback
from constants import SENTIMENT_KEYWORDS, CATEGORY_KEYWORDS
from text_utils import contains_any


def classify_sentiment(text: str) -> str:
    """Single source of truth for sentiment (B-01)."""
    if contains_any(text, SENTIMENT_KEYWORDS["긍정"]):
        return "긍정"
    if contains_any(text, SENTIMENT_KEYWORDS["부정"]):
        return "부정"
    return "중립"


def matches_category(text: str, category: str) -> bool:
    """Single source of truth for category (B-02): main keywords only."""
    sub_map = CATEGORY_KEYWORDS.get(category)
    if not sub_map or "main" not in sub_map:
        return False
    return contains_any(text, sub_map["main"])


class TextAnalyzer:
    def sent(self, feedbacks: List[Feedback]) -> Dict[str, int]:
        res = {"긍정": 0, "중립": 0, "부정": 0}
        for f in feedbacks:
            res[classify_sentiment(f.text)] += 1
        return res

    def kw(self, feedbacks: List[Feedback]) -> Dict[str, int]:
        res = {cat: 0 for cat in CATEGORY_KEYWORDS}
        for f in feedbacks:
            for cat in CATEGORY_KEYWORDS:
                if matches_category(f.text, cat):
                    res[cat] += 1
        return res
