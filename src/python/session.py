# -*- coding: utf-8 -*-
from typing import List
from feedback import Feedback


class Session:
    current_feedbacks: List[Feedback] = []
    download_feedbacks: List[Feedback] = []

    @classmethod
    def init_session(cls):
        pass

    @classmethod
    def get_current_feedbacks(cls) -> List[Feedback]:
        return cls.current_feedbacks

    @classmethod
    def update_current_feedbacks(cls, feedbacks: List[Feedback]):
        cls.current_feedbacks = feedbacks

    @classmethod
    def set_download_feedbacks(cls, feedbacks: List[Feedback]):
        cls.download_feedbacks = list(feedbacks)

    @classmethod
    def get_download_feedbacks(cls) -> List[Feedback]:
        return cls.download_feedbacks
