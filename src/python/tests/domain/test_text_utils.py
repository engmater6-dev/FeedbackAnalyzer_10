# -*- coding: utf-8 -*-
import pytest
from text_utils import contains_any


@pytest.mark.domain
class TestTextUtils:
    def test_contains_any_match(self):
        assert contains_any("배송 지연", ["배송", "택배"]) is True

    def test_contains_any_no_match(self):
        assert contains_any("만족", ["배송"]) is False
