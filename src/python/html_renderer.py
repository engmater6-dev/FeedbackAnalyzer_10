# -*- coding: utf-8 -*-
"""HTML presentation layer (Phase 3-C-2: extracted from app.render_page)."""
from datetime import datetime
from html import escape
from typing import Dict, List, Optional

from constants import CATEGORIES
from logger import Logger
from models.session import get_session


def _current_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class HtmlRenderer:
    """Builds dashboard HTML from analysis results and flash messages."""

    def render(
        self,
        success: str = "",
        warning: str = "",
        error: str = "",
        sentiment_results: Optional[Dict[str, int]] = None,
        keyword_results: Optional[Dict[str, int]] = None,
        trend_sentiment: Optional[Dict[str, Dict[str, int]]] = None,
        trend_keyword: Optional[Dict[str, Dict[str, int]]] = None,
        feedbacks: Optional[List] = None,
    ) -> str:
        if sentiment_results is None:
            sentiment_results = {}
        if keyword_results is None:
            keyword_results = {}
        if trend_sentiment is None:
            trend_sentiment = {}
        if trend_keyword is None:
            trend_keyword = {}
        if feedbacks is None:
            feedbacks = []

        html = self._document_start()

        if success:
            html += (
                f'<p class="alert alert-success">'
                f"{_current_timestamp()} : {escape(success)}</p>"
            )

        html += self._input_section()
        html += self._upload_section()
        html += self._filter_section()
        html += self._log_settings_section()

        if warning:
            html += f'<p class="alert alert-warning">{escape(warning)}</p>'

        html += self._results_section(sentiment_results, keyword_results)
        html += self._trend_section(trend_sentiment, trend_keyword)

        if error:
            html += f'<p class="alert alert-danger">{escape(error)}</p>'

        html += self._page_logs_section()
        html += "</div></body></html>"
        return html

    @staticmethod
    def _document_start() -> str:
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Feedback Analyzer</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; margin-bottom: 30px; }
        .section { margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; }
        input[type="text"], textarea, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; box-sizing: border-box; }
        textarea { min-height: 120px; height: auto; resize: vertical; white-space: pre-wrap; }
        button { background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; margin-right: 10px; }
        button:hover { background-color: #0056b3; }
        .btn-success { background-color: #28a745; }
        .btn-success:hover { background-color: #1e7e34; }
        .alert-success { background-color: #d4edda; border-color: #c3e6cb; color: #155724; padding: 10px; border-radius: 4px; }
        .alert-warning { background-color: #fff3cd; border-color: #ffeaa7; color: #856404; padding: 10px; border-radius: 4px; }
        .alert-danger { background-color: #f8d7da; border-color: #f5c6cb; color: #721c24; padding: 10px; border-radius: 4px; }
        .alert-info { background-color: #d1ecf1; border-color: #bee5eb; color: #0c5460; padding: 10px; border-radius: 4px; }
        .stats { display: flex; justify-content: space-around; margin: 20px 0; }
        .stat-item { text-align: center; padding: 15px; background-color: #f8f9fa; border-radius: 5px; flex: 1; margin: 0 10px; }
        .stat-number { font-size: 24px; font-weight: bold; color: #007bff; }
        .stat-label { color: #666; margin-top: 5px; }
        .trend-month { margin-bottom: 20px; }
        .trend-month-title { font-weight: bold; color: #333; margin-bottom: 8px; }
        .trend-bar-row { display: flex; align-items: center; margin: 4px 0; font-size: 13px; }
        .trend-bar-label { width: 48px; color: #555; }
        .trend-bar-track { flex: 1; height: 18px; background: #eee; border-radius: 3px; margin: 0 8px; overflow: hidden; }
        .trend-bar-fill { height: 100%; border-radius: 3px; min-width: 2px; }
        .trend-bar-fill.positive { background-color: #28a745; }
        .trend-bar-fill.neutral { background-color: #6c757d; }
        .trend-bar-fill.negative { background-color: #dc3545; }
        .trend-bar-fill.category { background-color: #007bff; }
        .trend-bar-count { width: 32px; text-align: right; color: #333; }
        .upload-hint { font-size: 13px; color: #666; margin-top: 8px; }
    </style>
</head>
<body>
<div class="container">
    <h1>Feedback Analyzer</h1>
    <p style="text-align: center; color: #666;">고객 피드백 분석 시스템</p>"""

    @staticmethod
    def _input_section() -> str:
        return """
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

    @staticmethod
    def _upload_section() -> str:
        return """
    <div class="section">
        <h3>CSV 파일 업로드 (선택사항)</h3>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <div class="form-group">
                <label for="file">CSV 파일 선택:</label>
                <input type="file" id="file" name="file" accept=".csv">
            </div>
            <button type="submit">업로드</button>
        </form>
        <p class="upload-hint">Trend CSV: 첫 행에 <code>date,text</code> 헤더 — 월별 감정·키워드 추이가 표시됩니다.</p>
    </div>"""

    def _filter_section(self) -> str:
        cat_options = "".join(
            f'<option value="{cat}">{cat}</option>' for cat in CATEGORIES
        )
        return f"""
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

    @staticmethod
    def _stats_block(title: str, results: Dict[str, int]) -> str:
        block = f"<h4>{title}</h4><div class=\"stats\">"
        for label, count in results.items():
            block += (
                f'<div class="stat-item">'
                f'<div class="stat-number">{count}</div>'
                f'<div class="stat-label">{label}</div></div>'
            )
        block += "</div>"
        return block

    def _results_section(
        self,
        sentiment_results: Dict[str, int],
        keyword_results: Dict[str, int],
    ) -> str:
        if not sentiment_results and not keyword_results:
            return ""

        html = '<div class="section"><h3>분석 결과</h3>'
        if sentiment_results:
            html += self._stats_block("감정 분포", sentiment_results)
        if keyword_results:
            html += self._stats_block("키워드 분포", keyword_results)
        if get_session().get_download_feedbacks():
            html += (
                '<a href="/download">'
                '<button class="btn-success">결과 다운로드</button></a>'
            )
        html += "</div>"
        return html

    @staticmethod
    def _sentiment_bar_class(label: str) -> str:
        if label == "긍정":
            return "positive"
        if label == "부정":
            return "negative"
        return "neutral"

    def _trend_bars(
        self,
        month: str,
        counts: Dict[str, int],
        bar_class_fn,
    ) -> str:
        total = sum(counts.values()) or 1
        html = f'<div class="trend-month"><div class="trend-month-title">{escape(month)}</div>'
        for label, count in counts.items():
            if count <= 0:
                continue
            width = int(100 * count / total)
            css = bar_class_fn(label)
            html += (
                f'<div class="trend-bar-row">'
                f'<span class="trend-bar-label">{escape(label)}</span>'
                f'<div class="trend-bar-track">'
                f'<div class="trend-bar-fill {css}" style="width:{width}%;"></div>'
                f"</div>"
                f'<span class="trend-bar-count">{count}</span></div>'
            )
        html += "</div>"
        return html

    def _trend_section(
        self,
        trend_sentiment: Dict[str, Dict[str, int]],
        trend_keyword: Dict[str, Dict[str, int]],
    ) -> str:
        if not trend_sentiment and not trend_keyword:
            return ""

        html = '<div class="section"><h3>월별 추이 (Trend)</h3>'
        if trend_sentiment:
            html += "<h4>감정 추이</h4>"
            for month, counts in trend_sentiment.items():
                html += self._trend_bars(
                    month, counts, self._sentiment_bar_class
                )
        if trend_keyword:
            html += "<h4>키워드 추이 (건수 &gt; 0)</h4>"
            for month, counts in trend_keyword.items():
                filtered = {k: v for k, v in counts.items() if v > 0}
                if filtered:
                    html += self._trend_bars(
                        month,
                        filtered,
                        lambda _label: "category",
                    )
        html += "</div>"
        return html

    def _log_settings_section(self) -> str:
        def checked(flag: bool) -> str:
            return " checked" if flag else ""

        return f"""
    <div class="section">
        <h3>로그 표시 설정</h3>
        <form action="/settings/logs" method="post">
            <div class="form-group">
                <label><input type="checkbox" name="show_warning" value="on"{checked(Logger.show_warning_on_page)}> Warning 페이지 표시</label>
            </div>
            <div class="form-group">
                <label><input type="checkbox" name="show_error" value="on"{checked(Logger.show_error_on_page)}> Error 페이지 표시</label>
            </div>
            <div class="form-group">
                <label><input type="checkbox" name="show_info" value="on"{checked(Logger.show_info_on_page)}> Info 페이지 표시 (선택)</label>
            </div>
            <button type="submit">설정 저장</button>
        </form>
    </div>"""

    @staticmethod
    def _page_logs_section() -> str:
        css_by_level = {
            "warning": "alert-warning",
            "error": "alert-danger",
            "info": "alert-info",
        }
        html = ""
        for entry in Logger.get_page_logs():
            level = entry["level"]
            css = css_by_level.get(level, "alert-info")
            html += (
                f'<p class="alert {css}">{escape(entry["timestamp"])} '
                f'[{level.upper()}] {escape(entry["message"])}</p>'
            )
        return html


_renderer = HtmlRenderer()


def render_page(
    success: str = "",
    warning: str = "",
    error: str = "",
    sentiment_results: dict = None,
    keyword_results: dict = None,
    trend_sentiment: dict = None,
    trend_keyword: dict = None,
    feedbacks: list = None,
) -> str:
    """Backward-compatible facade for Flask routes."""
    return _renderer.render(
        success=success,
        warning=warning,
        error=error,
        sentiment_results=sentiment_results,
        keyword_results=keyword_results,
        trend_sentiment=trend_sentiment,
        trend_keyword=trend_keyword,
        feedbacks=feedbacks,
    )
