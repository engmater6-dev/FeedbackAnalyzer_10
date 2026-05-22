# -*- coding: utf-8 -*-
from typing import List, Dict
from feedback import Feedback
from constants import CATEGORY_KEYWORDS
from analysis_strategies import classify_sentiment, matches_category

__all__ = ["TextAnalyzer", "classify_sentiment", "matches_category"]


class TextAnalyzer:
    def analyze_sentiments(self, feedbacks: List[Feedback]) -> Dict[str, int]:
        """Count feedbacks per sentiment label."""
        res = {"긍정": 0, "중립": 0, "부정": 0}
        for f in feedbacks:
            res[classify_sentiment(f.text)] += 1
        return res

    def analyze_keywords(self, feedbacks: List[Feedback]) -> Dict[str, int]:
        """Count feedbacks matching each category (main keywords)."""
        res = {cat: 0 for cat in CATEGORY_KEYWORDS}
        for f in feedbacks:
            for cat in CATEGORY_KEYWORDS:
                if matches_category(f.text, cat):
                    res[cat] += 1
        return res
