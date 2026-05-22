# -*- coding: utf-8 -*-
import pytest
from feedback import Feedback
from session import Session


@pytest.fixture
def anchor_feedback():
    return [Feedback("배송이 너무 늦어요. 화가 납니다.")]


@pytest.fixture(autouse=True)
def reset_session():
    Session.current_feedbacks = []
    yield
    Session.current_feedbacks = []
