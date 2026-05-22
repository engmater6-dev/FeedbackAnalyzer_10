# -*- coding: utf-8 -*-
import pytest
from feedback import Feedback
from session import Session


@pytest.mark.domain
class TestSession:
    def test_update_and_get_feedbacks(self):
        items = [Feedback("a"), Feedback("b")]
        Session.update_current_feedbacks(items)
        assert len(Session.get_current_feedbacks()) == 2

    def test_download_feedbacks_copy(self):
        original = [Feedback("x")]
        Session.set_download_feedbacks(original)
        original.append(Feedback("y"))
        assert len(Session.get_download_feedbacks()) == 1

    def test_init_session_no_op(self):
        Session.init_session()
