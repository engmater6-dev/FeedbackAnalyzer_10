# -*- coding: utf-8 -*-
import pytest
from feedback import Feedback
from models.session import Session, get_session, reset_app_session


@pytest.mark.domain
class TestSession:
    def test_instance_update_and_get_feedbacks(self):
        session = Session()
        items = [Feedback("a"), Feedback("b")]
        session.update_current_feedbacks(items)
        assert len(session.get_current_feedbacks()) == 2

    def test_download_feedbacks_copy(self):
        session = Session()
        original = [Feedback("x")]
        session.set_download_feedbacks(original)
        original.append(Feedback("y"))
        assert len(session.get_download_feedbacks()) == 1

    def test_init_session_clears_lists(self):
        session = Session()
        session.update_current_feedbacks([Feedback("a")])
        session.set_download_feedbacks([Feedback("b")])
        session.init_session()
        assert session.get_current_feedbacks() == []
        assert session.get_download_feedbacks() == []

    def test_singleton_via_get_session(self):
        reset_app_session()
        get_session().update_current_feedbacks([Feedback("only")])
        assert len(get_session().get_current_feedbacks()) == 1

    def test_reset_app_session_isolates_state(self):
        get_session().update_current_feedbacks([Feedback("old")])
        reset_app_session()
        assert get_session().get_current_feedbacks() == []
