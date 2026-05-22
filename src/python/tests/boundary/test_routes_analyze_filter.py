# -*- coding: utf-8 -*-
import pytest


@pytest.mark.boundary
@pytest.mark.skip(reason="Domain Green 이후 IT-01/02")
class TestRoutesPlaceholder:
    def test_post_analyze_todo(self):
        pass

    def test_post_filter_todo(self):
        pass
