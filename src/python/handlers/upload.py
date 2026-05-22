# -*- coding: utf-8 -*-
from flask import Blueprint, request

from handlers._common import begin_page_request
from handlers._deps import text_analyzer
from html_renderer import render_page
from logger import Logger
from models.session import get_session
from services.csv_parser import parse_csv_content
from services.trend_service import build_trend_results

bp = Blueprint("upload", __name__)


@bp.route("/upload", methods=["POST"])
def upload():
    begin_page_request()
    try:
        session = get_session()
        feedbacks = session.get_current_feedbacks()
        file = request.files.get("file")
        added = 0
        if file and file.filename:
            content = file.read().decode("utf-8-sig")
            parsed = parse_csv_content(content)
            added = len(parsed)
            feedbacks.extend(parsed)
            session.update_current_feedbacks(feedbacks)
            session.set_download_feedbacks(feedbacks)
            Logger.log_info("파일이 성공적으로 업로드되었습니다.")
            if added == 0:
                Logger.log_warning("CSV에서 읽을 수 있는 피드백이 없습니다.")

        sentiment_results = {}
        keyword_results = {}
        trend_sentiment = {}
        trend_keyword = {}
        if feedbacks:
            sentiment_results = text_analyzer.analyze_sentiments(feedbacks)
            keyword_results = text_analyzer.analyze_keywords(feedbacks)
            trend_sentiment, trend_keyword = build_trend_results(feedbacks)

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
            trend_sentiment=trend_sentiment,
            trend_keyword=trend_keyword,
            feedbacks=feedbacks,
        )
    except Exception as e:
        Logger.log_error(f"파일 업로드 오류: {e}")
        return render_page(error="파일 업로드 중 오류가 발생했습니다.")
