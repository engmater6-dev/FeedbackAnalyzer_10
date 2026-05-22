# -*- coding: utf-8 -*-
"""Compatibility shim — use models.feedback in new code."""
from models.feedback import Feedback  # noqa: F401

__all__ = ["Feedback"]
