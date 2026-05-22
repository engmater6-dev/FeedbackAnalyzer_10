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
def reset_session(tmp_path):
    reset_app_session()
    Logger._ui_logs = []
    Logger.show_warning_on_page = True
    Logger.show_error_on_page = True
    Logger.show_info_on_page = False

    from services import keyword_db
    from services.sentiment import invalidate_sentiment_cache

    db_file = tmp_path / "sentiment_keywords.db"
    keyword_db.set_db_path(str(db_file))
    keyword_db.reset_db_connection()
    keyword_db.ensure_db_ready()
    invalidate_sentiment_cache()

    yield

    keyword_db.reset_db_connection()
    keyword_db.set_db_path(None)
    invalidate_sentiment_cache()
    reset_app_session()
    Logger._ui_logs = []
    Logger.show_warning_on_page = True
    Logger.show_error_on_page = True
    Logger.show_info_on_page = False
