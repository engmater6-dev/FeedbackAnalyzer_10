# -*- coding: utf-8 -*-
import pytest
from feedback import Feedback


@pytest.mark.domain
class TestFeedback:
    def test_text_property(self):
        fb = Feedback("hello")
        assert fb.text == "hello"
