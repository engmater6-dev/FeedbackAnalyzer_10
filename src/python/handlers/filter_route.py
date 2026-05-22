# -*- coding: utf-8 -*-
from flask import Blueprint, request

from handlers._common import begin_page_request
from handlers._deps import text_analyzer
from html_renderer import render_page
from logger import Logger
from models.session import Session
from services.filter_service import filter_feedbacks

bp = Blueprint("filter", __name__)


@bp.route("/filter", methods=["POST"])
def filter_route():
    begin_page_request()
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
