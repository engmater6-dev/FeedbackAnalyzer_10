# -*- coding: utf-8 -*-
from typing import Dict, List, Tuple

from constants import CATEGORY_KEYWORDS
from models.feedback import Feedback
from services.category import matches_category


def has_trend_data(feedbacks: List[Feedback]) -> bool:
    return any(fb.recorded_at for fb in feedbacks)


def _month_key(recorded_at: str) -> str:
    return recorded_at[:7]


def aggregate_sentiment_by_month(
    feedbacks: List[Feedback],
) -> Dict[str, Dict[str, int]]:
    """Monthly sentiment counts; requires feedback.sentiment set."""
    buckets: Dict[str, Dict[str, int]] = {}
    for fb in feedbacks:
        if not fb.recorded_at or not fb.sentiment:
            continue
        month = _month_key(fb.recorded_at)
        if month not in buckets:
            buckets[month] = {"긍정": 0, "중립": 0, "부정": 0}
        buckets[month][fb.sentiment] += 1
    return dict(sorted(buckets.items()))


def aggregate_keyword_by_month(
    feedbacks: List[Feedback],
) -> Dict[str, Dict[str, int]]:
    """Monthly category counts (main-only, ADR-001)."""
    buckets: Dict[str, Dict[str, int]] = {}
    for fb in feedbacks:
        if not fb.recorded_at:
            continue
        month = _month_key(fb.recorded_at)
        if month not in buckets:
            buckets[month] = {cat: 0 for cat in CATEGORY_KEYWORDS}
        for cat in CATEGORY_KEYWORDS:
            if matches_category(fb.text, cat):
                buckets[month][cat] += 1
    return dict(sorted(buckets.items()))


def build_trend_results(
    feedbacks: List[Feedback],
) -> Tuple[Dict[str, Dict[str, int]], Dict[str, Dict[str, int]]]:
    """Monthly trends after analyze_sentiments/keywords (sentiment/category set)."""
    if not has_trend_data(feedbacks):
        return {}, {}
    return (
        aggregate_sentiment_by_month(feedbacks),
        aggregate_keyword_by_month(feedbacks),
    )
