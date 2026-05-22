# -*- coding: utf-8 -*-
from typing import List, Optional

from models.feedback import Feedback

_app_session: Optional["Session"] = None


def get_session() -> "Session":
    """Return the application-scoped session singleton."""
    global _app_session
    if _app_session is None:
        _app_session = Session()
    return _app_session


def reset_app_session() -> "Session":
    """Replace the singleton with a fresh session (tests, request reset)."""
    global _app_session
    _app_session = Session()
    return _app_session


class Session:
    """Per-application feedback state (instance-based, S-S01)."""

    def __init__(self) -> None:
        self._current_feedbacks: List[Feedback] = []
        self._download_feedbacks: List[Feedback] = []

    def init_session(self) -> None:
        self._current_feedbacks = []
        self._download_feedbacks = []

    def get_current_feedbacks(self) -> List[Feedback]:
        return self._current_feedbacks

    def update_current_feedbacks(self, feedbacks: List[Feedback]) -> None:
        self._current_feedbacks = feedbacks

    def set_download_feedbacks(self, feedbacks: List[Feedback]) -> None:
        self._download_feedbacks = list(feedbacks)

    def get_download_feedbacks(self) -> List[Feedback]:
        return self._download_feedbacks
