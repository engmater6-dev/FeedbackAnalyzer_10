# -*- coding: utf-8 -*-
"""Shared text helpers (Phase 3-C-6)."""
from typing import List


def contains_any(text: str, keywords: List[str]) -> bool:
    """True if any keyword appears as a substring in text."""
    return any(kw in text for kw in keywords)
