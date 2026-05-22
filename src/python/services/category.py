# -*- coding: utf-8 -*-
"""Rule-based category matching — main keywords only (ADR-001, B-02 SSOT)."""
from constants import CATEGORY_KEYWORDS
from text_utils import contains_any

__all__ = [
    "RuleBasedCategoryStrategy",
    "matches_category",
]


class RuleBasedCategoryStrategy:
    """Category match via main keywords only (ADR-001)."""

    def matches(self, text: str, category: str) -> bool:
        sub_map = CATEGORY_KEYWORDS.get(category)
        if not sub_map or "main" not in sub_map:
            return False
        return contains_any(text, sub_map["main"])


_default_strategy = RuleBasedCategoryStrategy()


def matches_category(text: str, category: str) -> bool:
    """Single source of truth for category (B-02)."""
    return _default_strategy.matches(text, category)
