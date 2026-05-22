# -*- coding: utf-8 -*-
import pytest
from feedback import Feedback
from session import Session
from logger import Logger


@pytest.fixture
def anchor_feedback():
    return [Feedback("배송이 너무 늦어요. 화가 납니다.")]


@pytest.fixture
def client():
    from app import app

    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_session():
    Session.current_feedbacks = []
    Session.download_feedbacks = []
    Logger._ui_logs = []
    Logger.show_warning_on_page = True
    Logger.show_error_on_page = True
    Logger.show_info_on_page = False
    yield
    Session.current_feedbacks = []
    Session.download_feedbacks = []
    Logger._ui_logs = []
    Logger.show_warning_on_page = True
    Logger.show_error_on_page = True
    Logger.show_info_on_page = False
