# -*- coding: utf-8 -*-
"""Sentiment keyword CRUD routes (R-10)."""
import pytest

from services.keyword_db import list_all
from services.sentiment import classify_sentiment, invalidate_sentiment_cache


@pytest.mark.boundary
class TestRoutesKeywords:
    def test_index_shows_keyword_management_section(self, client):
        response = client.get("/")
        html = response.get_data(as_text=True)
        assert response.status_code == 200
        assert "감정 키워드 관리" in html
        assert "SQLite" in html

    def test_add_keyword_affects_classification(self, client):
        unique = "경이로운최고키워드999"
        response = client.post(
            "/settings/keywords",
            data={"action": "add", "label": "긍정", "word": unique},
        )
        assert response.status_code == 200
        assert unique in response.get_data(as_text=True)
        invalidate_sentiment_cache()
        assert classify_sentiment(f"이거 {unique} 입니다") == "긍정"

    def test_delete_keyword_via_form(self, client):
        unique = "삭제대상키워드888"
        client.post(
            "/settings/keywords",
            data={"action": "add", "label": "부정", "word": unique},
        )
        invalidate_sentiment_cache()
        row = next(r for r in list_all() if r["word"] == unique)
        del_resp = client.post(
            "/settings/keywords",
            data={"action": "delete", "word_id": str(row["id"])},
        )
        assert del_resp.status_code == 200
        invalidate_sentiment_cache()
        assert classify_sentiment(f"문장 {unique} 끝") == "중립"
