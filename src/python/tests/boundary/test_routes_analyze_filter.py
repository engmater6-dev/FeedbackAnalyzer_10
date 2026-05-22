# -*- coding: utf-8 -*-
"""IT-01~04: Flask boundary tests (test_plan)."""
import io

import pytest

from models.session import get_session

ANCHOR_TEXT = "배송이 너무 늦어요. 화가 납니다."


@pytest.mark.boundary
@pytest.mark.p0
class TestRoutesAnalyzeFilter:
    """IT-01, IT-02: Anchor via HTTP."""

    def test_get_index(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "Feedback Analyzer" in response.get_data(as_text=True)

    def test_post_analyze_anchor_text(self, client):
        response = client.post("/analyze", data={"text": ANCHOR_TEXT})
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert "감정 분포" in html
        assert "키워드 분포" in html
        assert len(get_session().get_current_feedbacks()) == 1
        assert len(get_session().get_download_feedbacks()) == 1

    def test_post_filter_negative_shipping(self, client):
        client.post("/analyze", data={"text": ANCHOR_TEXT})
        response = client.post(
            "/filter",
            data={"sentiment": "부정", "keyword": "배송"},
        )
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert "분석 결과" in html
        assert len(get_session().get_download_feedbacks()) >= 1

    def test_post_analyze_multiline(self, client):
        response = client.post(
            "/analyze",
            data={"text": "좋습니다\n배송이 너무 늦어요. 화가 납니다."},
        )
        assert response.status_code == 200
        assert len(get_session().get_current_feedbacks()) == 2


@pytest.mark.boundary
class TestRoutesUploadDownload:
    """IT-03, IT-04."""

    def test_post_upload_text_header_csv(self, client):
        csv_body = f"text\n{ANCHOR_TEXT}\n"
        response = client.post(
            "/upload",
            data={"file": (io.BytesIO(csv_body.encode("utf-8-sig")), "feedbacks.csv")},
            content_type="multipart/form-data",
        )
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert "업로드 완료" in html or "피드백" in html
        assert len(get_session().get_current_feedbacks()) >= 1
        assert "감정 분포" in html

    def test_get_download_after_filter(self, client):
        client.post("/analyze", data={"text": ANCHOR_TEXT})
        client.post(
            "/filter",
            data={"sentiment": "부정", "keyword": "배송"},
        )
        response = client.get("/download")
        body = response.get_data(as_text=True)

        assert response.status_code == 200
        assert "text" in body
        assert ANCHOR_TEXT in body

    def test_get_download_empty_shows_warning(self, client):
        response = client.get("/download")
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert "다운로드할 피드백이 없습니다" in html

    def test_post_filter_no_feedbacks_warning(self, client):
        response = client.post(
            "/filter",
            data={"sentiment": "부정", "keyword": "배송"},
        )
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert "분석할 피드백이 없습니다" in html

    def test_post_filter_no_match_warning(self, client):
        client.post("/analyze", data={"text": "최고입니다 만족"})
        response = client.post(
            "/filter",
            data={"sentiment": "부정", "keyword": "배송"},
        )
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert "필터링 결과가 없습니다" in html

    def test_post_upload_empty_rows_warning(self, client):
        response = client.post(
            "/upload",
            data={"file": (io.BytesIO("text\n\n".encode("utf-8-sig")), "empty.csv")},
            content_type="multipart/form-data",
        )
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert "CSV" in html and "피드백" in html
        assert "WARNING" in html or "읽을 수 있는" in html

    def test_post_upload_without_file(self, client):
        response = client.post("/upload", data={})
        assert response.status_code == 200

    def test_post_analyze_empty_text(self, client):
        response = client.post("/analyze", data={"text": "   \n  "})
        assert response.status_code == 200
        assert len(get_session().get_current_feedbacks()) == 0


@pytest.mark.boundary
class TestRoutesErrors:
    def test_analyze_exception_renders_error(self, client, monkeypatch):
        def _raise():
            raise RuntimeError("test failure")

        class _BrokenSession:
            def get_current_feedbacks(self):
                raise RuntimeError("test failure")

        monkeypatch.setattr("handlers.analyze.get_session", lambda: _BrokenSession())
        response = client.post("/analyze", data={"text": "x"})
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert "오류가 발생" in html

    def test_upload_exception_renders_error(self, client, monkeypatch):
        def _fail(_content):
            raise ValueError("parse")

        monkeypatch.setattr("handlers.upload.parse_csv_content", _fail)
        response = client.post(
            "/upload",
            data={"file": (io.BytesIO(b"text\nx"), "a.csv")},
            content_type="multipart/form-data",
        )
        html = response.get_data(as_text=True)
        assert "업로드 중 오류" in html

    def test_filter_exception_renders_error(self, client, monkeypatch):
        get_session().update_current_feedbacks([__import__("feedback").Feedback("x")])

        def _fail(*_args, **_kwargs):
            raise RuntimeError("filter failed")

        monkeypatch.setattr("handlers.filter_route.filter_feedbacks", _fail)
        response = client.post(
            "/filter",
            data={"sentiment": "전체", "keyword": "전체"},
        )
        html = response.get_data(as_text=True)
        assert "오류가 발생" in html


@pytest.mark.boundary
class TestLogSettings:
    """3-C-4: Logger warning/error/info page toggles."""

    def test_log_settings_form_on_index(self, client):
        html = client.get("/").get_data(as_text=True)
        assert "로그 표시 설정" in html
        assert 'action="/settings/logs"' in html

    def test_disable_warning_hides_buffered_log(self, client):
        client.post("/settings/logs", data={})
        html = client.get("/download").get_data(as_text=True)
        assert "다운로드할 피드백" in html
        assert "[WARNING]" not in html

    def test_enable_warning_shows_buffered_log(self, client):
        client.post("/settings/logs", data={"show_warning": "on"})
        html = client.get("/download").get_data(as_text=True)
        assert "[WARNING]" in html

    def test_enable_info_shows_on_analyze(self, client):
        client.post(
            "/settings/logs",
            data={"show_warning": "on", "show_error": "on", "show_info": "on"},
        )
        html = client.post("/analyze", data={"text": "테스트"}).get_data(as_text=True)
        assert "[INFO]" in html
