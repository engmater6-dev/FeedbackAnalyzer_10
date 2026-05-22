# -*- coding: utf-8 -*-
from logger import Logger


def begin_page_request():
    """Per-request UI log buffer (avoids cross-request accumulation)."""
    Logger._ui_logs = []
