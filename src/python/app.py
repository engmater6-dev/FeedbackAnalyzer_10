# -*- coding: utf-8 -*-
import csv
import io
from datetime import datetime
from html import escape

from flask import Flask, request, Response

from feedback import Feedback
from constants import CATEGORIES
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


def _current_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _begin_page_request():
    """Per-request UI log buffer (avoids cross-request accumulation)."""
    Logger._ui_logs = []


def render_page(
    success: str = "",
    warning: str = "",
    error: str = "",
    sentiment_results: dict = None,
    keyword_results: dict = None,
    feedbacks: list = None,
) -> str:
    if sentiment_results is None:
        sentiment_results = {}
    if keyword_results is None:
        keyword_results = {}
    if feedbacks is None:
        feedbacks = []

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Feedback Analyzer</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; text-align: center; margin-bottom: 30px; }}
        .section {{ margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
        .form-group {{ margin-bottom: 15px; }}
        label {{ display: block; margin-bottom: 5px; font-weight: bold; color: #555; }}
        input[type="text"], textarea, select {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; box-sizing: border-box; }}
        textarea {{ min-height: 120px; height: auto; resize: vertical; white-space: pre-wrap; }}
        button {{ background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; margin-right: 10px; }}
        button:hover {{ background-color: #0056b3; }}
        .btn-success {{ background-color: #28a745; }}
        .btn-success:hover {{ background-color: #1e7e34; }}
        .alert-success {{ background-color: #d4edda; border-color: #c3e6cb; color: #155724; padding: 10px; border-radius: 4px; }}
        .alert-warning {{ background-color: #fff3cd; border-color: #ffeaa7; color: #856404; padding: 10px; border-radius: 4px; }}
        .alert-danger {{ background-color: #f8d7da; border-color: #f5c6cb; color: #721c24; padding: 10px; border-radius: 4px; }}
        .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .stat-item {{ text-align: center; padding: 15px; background-color: #f8f9fa; border-radius: 5px; flex: 1; margin: 0 10px; }}
        .stat-number {{ font-size: 24px; font-weight: bold; color: #007bff; }}
        .stat-label {{ color: #666; margin-top: 5px; }}
    </style>
</head>
<body>
<div class="container">
    <h1>Feedback Analyzer</h1>
    <p style="text-align: center; color: #666;">고객 피드백 분석 시스템</p>"""

    if success:
        html += f'<p class="alert alert-success">{_current_timestamp()} : {escape(success)}</p>'

    # Input Section
    html += """
    <div class="section">
        <h3>피드백 입력</h3>
        <form action="/analyze" method="post">
            <div class="form-group">
                <label for="text">피드백 텍스트:</label>
                <textarea id="text" name="text" rows="6" placeholder="한 줄에 피드백 하나. Enter로 여러 줄 입력 가능합니다."></textarea>
            </div>
            <button type="submit">입력하기</button>
        </form>
    </div>"""

    # File Upload Section
    html += """
    <div class="section">
        <h3>CSV 파일 업로드 (선택사항)</h3>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <div class="form-group">
                <label for="file">CSV 파일 선택:</label>
                <input type="file" id="file" name="file" accept=".csv">
            </div>
            <button type="submit">업로드</button>
        </form>
    </div>"""

    # Filter Section
    cat_options = "".join(
        f'<option value="{cat}">{cat}</option>' for cat in CATEGORIES
    )
    html += f"""
    <div class="section">
        <h3>피드백 분석</h3>
        <form action="/filter" method="post">
            <div class="form-group">
                <label for="sentiment">감정 필터:</label>
                <select id="sentiment" name="sentiment">
                    <option value="전체">전체</option>
                    <option value="긍정">긍정</option>
                    <option value="중립">중립</option>
                    <option value="부정">부정</option>
                </select>
            </div>
            <div class="form-group">
                <label for="keyword">키워드 필터:</label>
                <select id="keyword" name="keyword">
                    <option value="전체">전체</option>
                    {cat_options}
                </select>
            </div>
            <button type="submit">분  석</button>
        </form>
    </div>"""

    if warning:
        html += f'<p class="alert alert-warning">{escape(warning)}</p>'

    # Results Section
    if sentiment_results or keyword_results:
        html += '<div class="section"><h3>분석 결과</h3>'
        if sentiment_results:
            html += '<h4>감정 분포</h4><div class="stats">'
            for label, count in sentiment_results.items():
                html += (
                    f'<div class="stat-item">'
                    f'<div class="stat-number">{count}</div>'
                    f'<div class="stat-label">{label}</div></div>'
                )
            html += "</div>"
        if keyword_results:
            html += '<h4>키워드 분포</h4><div class="stats">'
            for label, count in keyword_results.items():
                html += (
                    f'<div class="stat-item">'
                    f'<div class="stat-number">{count}</div>'
                    f'<div class="stat-label">{label}</div></div>'
                )
            html += "</div>"
        if Session.get_download_feedbacks():
            html += (
                '<a href="/download">'
                '<button class="btn-success">결과 다운로드</button></a>'
            )
        html += "</div>"

    if error:
        html += f'<p class="alert alert-danger">{escape(error)}</p>'

    for entry in Logger.get_page_logs():
        level = entry["level"]
        css = "alert-warning" if level == "warning" else "alert-danger"
        html += (
            f'<p class="alert {css}">{escape(entry["timestamp"])} '
            f'[{level.upper()}] {escape(entry["message"])}</p>'
        )

    html += "</div></body></html>"
    return html


@app.route("/", methods=["GET"])
def index():
    _begin_page_request()
    Session.init_session()
    feedbacks = Session.get_current_feedbacks()
    return render_page(success="피드백 분석기 시작", feedbacks=feedbacks)


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
            sentiment_results = text_analyzer.sent(feedbacks)
            keyword_results = text_analyzer.kw(feedbacks)
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
            sentiment_results = text_analyzer.sent(feedbacks)
            keyword_results = text_analyzer.kw(feedbacks)

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
                sentiment_results = text_analyzer.sent(filtered)
                keyword_results = text_analyzer.kw(filtered)
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
