# -*- coding: utf-8 -*-
from flask import Blueprint, request

from handlers._common import begin_page_request
from handlers._deps import text_analyzer
from html_renderer import render_page
from logger import Logger
from models.feedback import Feedback
from models.session import get_session
from services.trend_service import build_trend_results

bp = Blueprint("analyze", __name__)


@bp.route("/analyze", methods=["POST"])
def analyze():
    begin_page_request()
    try:
        session = get_session()
        feedbacks = session.get_current_feedbacks()
        text = request.form.get("text", "")

        for line in text.splitlines():
            line = line.strip()
            if line:
                feedbacks.append(Feedback(line))

        session.update_current_feedbacks(feedbacks)
        session.set_download_feedbacks(feedbacks)

        for fb in feedbacks:
            Logger.log_info(fb.text)

        Logger.log_info(f"현재 {len(feedbacks)}개의 피드백이 입력되었습니다.")

        success = f"{len(feedbacks)}개의 피드백이 입력되었습니다."
        sentiment_results = {}
        keyword_results = {}

        trend_sentiment = {}
        trend_keyword = {}
        if feedbacks:
            sentiment_results = text_analyzer.analyze_sentiments(feedbacks)
            keyword_results = text_analyzer.analyze_keywords(feedbacks)
            trend_sentiment, trend_keyword = build_trend_results(feedbacks)
            Logger.log_info("감성 분석 완료")
            Logger.log_info("키워드 분석 완료")

        return render_page(
            success=success,
            sentiment_results=sentiment_results,
            keyword_results=keyword_results,
            trend_sentiment=trend_sentiment,
            trend_keyword=trend_keyword,
            feedbacks=feedbacks,
        )
    except Exception as e:
        Logger.log_error(f"오류 발생: {e}")
        return render_page(error="처리 중 오류가 발생했습니다.")
