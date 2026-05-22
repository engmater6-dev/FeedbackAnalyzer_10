# -*- coding: utf-8 -*-
import pytest
from feedback import Feedback
from filters import filter_feedbacks


@pytest.mark.domain
class TestFiltersUnit:
    def test_filter_sentiment_only(self):
        data = [
            Feedback("최고입니다"),
            Feedback("배송이 너무 늦어요. 화가 납니다."),
        ]
        result = filter_feedbacks(data, "부정", "전체")
        assert len(result) == 1

    def test_filter_keyword_only(self):
        data = [Feedback("품질"), Feedback("가격이 비싸요")]
        result = filter_feedbacks(data, "전체", "품질")
        assert len(result) == 1
        assert result[0].text == "품질"
