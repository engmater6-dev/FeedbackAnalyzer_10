# -*- coding: utf-8 -*-
"""Compatibility shim — use services.filter_service in new code."""
from services.filter_service import filter_feedbacks  # noqa: F401

__all__ = ["filter_feedbacks"]
