# -*- coding: utf-8 -*-
"""Compatibility shim — use models.session in new code."""
from models.session import Session  # noqa: F401

__all__ = ["Session"]
