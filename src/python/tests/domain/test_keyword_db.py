# -*- coding: utf-8 -*-
import pytest
from constants import SENTIMENT_KEYWORDS
from services import keyword_db
from services.keyword_db import (
    add_word,
    delete_word,
    get_sentiment_keyword_map,
    list_all,
    seed_from_constants_if_empty,
)
from services.sentiment import classify_sentiment, invalidate_sentiment_cache


@pytest.mark.domain
class TestKeywordDb:
    def test_seed_loads_constants(self):
        expected = sum(
            len(SENTIMENT_KEYWORDS[label]) for label in ("긍정", "부정")
        )
        assert keyword_db.count_words() == expected
        assert seed_from_constants_if_empty() == 0

    def test_add_and_delete_word(self):
        assert add_word("긍정", "테스트키워드유니크123")
        invalidate_sentiment_cache()
        assert classify_sentiment("테스트키워드유니크123 문장") == "긍정"
        row = next(r for r in list_all() if r["word"] == "테스트키워드유니크123")
        assert delete_word(int(row["id"]))
        invalidate_sentiment_cache()
        assert classify_sentiment("테스트키워드유니크123 문장") == "중립"

    def test_add_duplicate_returns_false(self):
        unique = "중복테스트단어777"
        assert add_word("긍정", unique)
        assert add_word("긍정", unique) is False

    def test_get_sentiment_keyword_map_matches_labels(self):
        kw_map = get_sentiment_keyword_map()
        assert "긍정" in kw_map and "부정" in kw_map
        assert "화가" in kw_map["부정"]
