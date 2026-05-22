# -*- coding: utf-8 -*-
import pytest
from feedback import Feedback
from logger import Logger
from models.session import reset_app_session


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
    reset_app_session()
    Logger._ui_logs = []
    Logger.show_warning_on_page = True
    Logger.show_error_on_page = True
    Logger.show_info_on_page = False
    yield
    reset_app_session()
    Logger._ui_logs = []
    Logger.show_warning_on_page = True
    Logger.show_error_on_page = True
    Logger.show_info_on_page = False
