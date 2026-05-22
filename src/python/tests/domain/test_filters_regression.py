# -*- coding: utf-8 -*-
"""
README Phase 1 Red — 회귀 시나리오
- 중립 3건: sent 중립 수 = filter(중립) 건수 (Mom Test §3.2)
- "품질" only: kw 품질 = filter(품질) 건수 (B-02 main 스킵, sub에 plain 품질 없음)
"""
import pytest
from feedback import Feedback
from text_analyzer import TextAnalyzer
from filters import filter_feedbacks


NEUTRAL_THREE_TEXTS = [
    "보통이에요",
    "괜찮아요",
    "특별한 불만 없음",
]


@pytest.fixture
def neutral_three_feedbacks():
    return [Feedback(t) for t in NEUTRAL_THREE_TEXTS]


@pytest.fixture
def category_main_only_feedbacks():
    return [Feedback("품질")]


@pytest.mark.p0
@pytest.mark.red
@pytest.mark.domain
class TestNeutralFilterConsistency:
    """test_plan UT-10 / Mom Test §3.2"""

    def test_sent_neutral_count_equals_filter_neutral_count(
        self, neutral_three_feedbacks
    ):
        sent_result = TextAnalyzer().sent(neutral_three_feedbacks)
        filtered = filter_feedbacks(neutral_three_feedbacks, "중립", "전체")

        assert sent_result["중립"] == len(filtered)


@pytest.mark.p0
@pytest.mark.red
@pytest.mark.domain
class TestCategoryMainOnlyConsistency:
    """test_plan UT-07 / B-02 main 키워드 스킵"""

    def test_kw_category_count_equals_filter_category_count(
        self, category_main_only_feedbacks
    ):
        kw_result = TextAnalyzer().kw(category_main_only_feedbacks)
        filtered = filter_feedbacks(
            category_main_only_feedbacks, "전체", "품질"
        )

        assert kw_result["품질"] == len(filtered)
