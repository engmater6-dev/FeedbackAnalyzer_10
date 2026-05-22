# -*- coding: utf-8 -*-
from typing import Dict, List, Optional

from constants import CATEGORY_KEYWORDS
from models.feedback import Feedback
from services.category import matches_category
from services.sentiment import classify_sentiment

__all__ = [
    "TextAnalyzer",
    "classify_sentiment",
    "matches_category",
    "analyze_sentiments",
    "analyze_keywords",
    "primary_category",
    "annotate_feedbacks",
]


def primary_category(text: str) -> Optional[str]:
    """First matching category in CATEGORY_KEYWORDS order (ADR-001 main-only)."""
    for cat in CATEGORY_KEYWORDS:
        if matches_category(text, cat):
            return cat
    return None


def annotate_feedbacks(feedbacks: List[Feedback]) -> None:
    """Fill sentiment and primary category on each feedback (R-08)."""
    for fb in feedbacks:
        fb.sentiment = classify_sentiment(fb.text)
        fb.category = primary_category(fb.text)


class TextAnalyzer:
    def analyze_sentiments(self, feedbacks: List[Feedback]) -> Dict[str, int]:
        """Count feedbacks per sentiment label; updates feedback.sentiment."""
        annotate_feedbacks(feedbacks)
        res = {"긍정": 0, "중립": 0, "부정": 0}
        for f in feedbacks:
            res[f.sentiment] += 1
        return res

    def analyze_keywords(self, feedbacks: List[Feedback]) -> Dict[str, int]:
        """Count feedbacks matching each category (main keywords)."""
        annotate_feedbacks(feedbacks)
        res = {cat: 0 for cat in CATEGORY_KEYWORDS}
        for f in feedbacks:
            for cat in CATEGORY_KEYWORDS:
                if matches_category(f.text, cat):
                    res[cat] += 1
        return res


def analyze_sentiments(feedbacks: List[Feedback]) -> Dict[str, int]:
    return TextAnalyzer().analyze_sentiments(feedbacks)


def analyze_keywords(feedbacks: List[Feedback]) -> Dict[str, int]:
    return TextAnalyzer().analyze_keywords(feedbacks)
