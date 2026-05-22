# -*- coding: utf-8 -*-
from typing import Optional


class Feedback:
    def __init__(
        self,
        text: str,
        sentiment: Optional[str] = None,
        category: Optional[str] = None,
        recorded_at: Optional[str] = None,
    ):
        self._text = text
        self._sentiment = sentiment
        self._category = category
        self._recorded_at = recorded_at

    @property
    def text(self) -> str:
        return self._text

    @property
    def sentiment(self) -> Optional[str]:
        return self._sentiment

    @sentiment.setter
    def sentiment(self, value: str) -> None:
        self._sentiment = value

    @property
    def category(self) -> Optional[str]:
        return self._category

    @category.setter
    def category(self, value: Optional[str]) -> None:
        self._category = value

    @property
    def recorded_at(self) -> Optional[str]:
        return self._recorded_at
