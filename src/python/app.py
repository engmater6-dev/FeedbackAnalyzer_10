# -*- coding: utf-8 -*-
import csv
import io

from flask import Flask, request, Response

from feedback import Feedback
from html_renderer import render_page
from session import Session
from text_analyzer import TextAnalyzer
from filters import filter_feedbacks
from logger import Logger

app = Flask(__name__)

text_analyzer = TextAnalyzer()


def _parse_csv_to_feedbacks(content: str) -> list:
    """B-04: use `text` column when header present, else column 0."""
    reader = csv.reader(io.StringIO(content))
    rows = [row for row in reader if row]
    if not rows:
        return []

    header = [cell.strip().lower() for cell in rows[0]]
    if "text" in header:
        text_col = header.index("text")
        data_rows = rows[1:]
    else:
        text_col = 0
        data_rows = rows

    feedbacks = []
    for row in data_rows:
        if len(row) > text_col:
            text = row[text_col].strip()
            if text:
                feedbacks.append(Feedback(text))
    return feedbacks


def _begin_page_request():
    """Per-request UI log buffer (avoids cross-request accumulation)."""
    Logger._ui_logs = []


@app.route("/", methods=["GET"])
def index():
    _begin_page_request()
    Session.init_session()
    feedbacks = Session.get_current_feedbacks()
    return render_page(success="피드백 분석기 시작", feedbacks=feedbacks)


@app.route("/settings/logs", methods=["POST"])
def settings_logs():
    _begin_page_request()
    Logger.apply_display_settings(
        show_warning=request.form.get("show_warning") == "on",
        show_error=request.form.get("show_error") == "on",
        show_info=request.form.get("show_info") == "on",
    )
    feedbacks = Session.get_current_feedbacks()
    return render_page(
        success="로그 표시 설정이 저장되었습니다.",
        feedbacks=feedbacks,
    )


@app.route("/analyze", methods=["POST"])
def analyze():
    _begin_page_request()
    try:
        feedbacks = Session.get_current_feedbacks()
        text = request.form.get("text", "")

        for line in text.splitlines():
            line = line.strip()
            if line:
                feedbacks.append(Feedback(line))

        Session.update_current_feedbacks(feedbacks)
        Session.set_download_feedbacks(feedbacks)

        for fb in feedbacks:
            Logger.log_info(fb.text)

        Logger.log_info(f"현재 {len(feedbacks)}개의 피드백이 입력되었습니다.")

        success = f"{len(feedbacks)}개의 피드백이 입력되었습니다."
        sentiment_results = {}
        keyword_results = {}

        if feedbacks:
            sentiment_results = text_analyzer.analyze_sentiments(feedbacks)
            keyword_results = text_analyzer.analyze_keywords(feedbacks)
            Logger.log_info("감성 분석 완료")
            Logger.log_info("키워드 분석 완료")

        return render_page(
            success=success,
            sentiment_results=sentiment_results,
            keyword_results=keyword_results,
            feedbacks=feedbacks,
        )
    except Exception as e:
        Logger.log_error(f"오류 발생: {e}")
        return render_page(error="처리 중 오류가 발생했습니다.")


@app.route("/upload", methods=["POST"])
def upload():
    _begin_page_request()
    try:
        feedbacks = Session.get_current_feedbacks()
        file = request.files.get("file")
        added = 0
        if file and file.filename:
            content = file.read().decode("utf-8-sig")
            parsed = _parse_csv_to_feedbacks(content)
            added = len(parsed)
            feedbacks.extend(parsed)
            Session.update_current_feedbacks(feedbacks)
            Session.set_download_feedbacks(feedbacks)
            Logger.log_info("파일이 성공적으로 업로드되었습니다.")
            if added == 0:
                Logger.log_warning("CSV에서 읽을 수 있는 피드백이 없습니다.")

        sentiment_results = {}
        keyword_results = {}
        if feedbacks:
            sentiment_results = text_analyzer.analyze_sentiments(feedbacks)
            keyword_results = text_analyzer.analyze_keywords(feedbacks)

        if added:
            success = (
                f"CSV {added}건 업로드 완료. 총 {len(feedbacks)}개 피드백 — "
                "아래 분석 결과를 확인하세요."
            )
        else:
            success = f"{len(feedbacks)}개의 피드백이 입력되었습니다."

        return render_page(
            success=success,
            sentiment_results=sentiment_results,
            keyword_results=keyword_results,
            feedbacks=feedbacks,
        )
    except Exception as e:
        Logger.log_error(f"파일 업로드 오류: {e}")
        return render_page(error="파일 업로드 중 오류가 발생했습니다.")


@app.route("/filter", methods=["POST"])
def filter_route():
    _begin_page_request()
    try:
        feedbacks = Session.get_current_feedbacks()
        sentiment = request.form.get("sentiment", "전체")
        keyword = request.form.get("keyword", "전체")

        if feedbacks:
            filtered = filter_feedbacks(feedbacks, sentiment, keyword)
            if filtered:
                Session.set_download_feedbacks(filtered)
                sentiment_results = text_analyzer.analyze_sentiments(filtered)
                keyword_results = text_analyzer.analyze_keywords(filtered)
                Logger.log_info(f"필터링 결과: {len(filtered)}개의 피드백")
                return render_page(
                    sentiment_results=sentiment_results,
                    keyword_results=keyword_results,
                    feedbacks=filtered,
                )
            else:
                Logger.log_warning("필터링 결과가 없습니다.")
                return render_page(warning="필터링 결과가 없습니다.")
        else:
            Logger.log_warning("분석할 피드백이 없습니다.")
            return render_page(warning="분석할 피드백이 없습니다.")
    except Exception as e:
        Logger.log_error(f"오류 발생: {e}")
        return render_page(error="처리 중 오류가 발생했습니다.")


@app.route("/download", methods=["GET"])
def download():
    _begin_page_request()
    rows = Session.get_download_feedbacks()
    if not rows:
        Logger.log_warning("다운로드할 피드백이 없습니다.")
        return render_page(warning="다운로드할 피드백이 없습니다.")

    output = io.StringIO()
    output.write("\ufeff")  # UTF-8 BOM
    output.write("text\n")
    for fb in rows:
        output.write(fb.text + "\n")

    return Response(
        output.getvalue(),
        mimetype="text/csv; charset=UTF-8",
        headers={"Content-Disposition": "attachment; filename=filtered_feedback.csv"},
    )


if __name__ == "__main__":
    Logger.log_info("서버가 http://localhost:8080 에서 시작됩니다.")
    app.run(host="0.0.0.0", port=8080)
