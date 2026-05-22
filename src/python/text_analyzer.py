# -*- coding: utf-8 -*-
"""Compatibility shim — use services.analysis_service in new code."""
from services.analysis_service import (  # noqa: F401
    TextAnalyzer,
    classify_sentiment,
    matches_category,
)

__all__ = ["TextAnalyzer", "classify_sentiment", "matches_category"]
