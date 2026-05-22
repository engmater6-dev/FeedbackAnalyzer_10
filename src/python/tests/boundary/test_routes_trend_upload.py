# -*- coding: utf-8 -*-
"""Trend CSV upload boundary (R-09)."""
import io
from pathlib import Path

import pytest

from models.session import get_session

REPO_ROOT = Path(__file__).resolve().parents[4]
TREND_CSV = REPO_ROOT / "sample" / "test_feedback_trend.csv"


@pytest.mark.boundary
class TestRoutesTrendUpload:
    def test_upload_trend_sample_shows_monthly_section(self, client):
        content = TREND_CSV.read_bytes()
        response = client.post(
            "/upload",
            data={"file": (io.BytesIO(content), "test_feedback_trend.csv")},
            content_type="multipart/form-data",
        )
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert "월별 추이" in html
        assert "2026-01" in html
        assert "2026-02" in html
        assert "감정 추이" in html
        assert len(get_session().get_current_feedbacks()) >= 12

    def test_upload_text_only_csv_no_trend_section(self, client):
        csv_body = "text\n보통이에요\n"
        response = client.post(
            "/upload",
            data={"file": (io.BytesIO(csv_body.encode("utf-8")), "plain.csv")},
            content_type="multipart/form-data",
        )
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert "월별 추이" not in html
        assert get_session().get_current_feedbacks()[0].recorded_at is None
