# -*- coding: utf-8 -*-
from flask import Blueprint, request

from handlers._common import begin_page_request
from html_renderer import render_page
from logger import Logger
from models.session import get_session
from services.keyword_db import add_word, delete_word, list_all
from services.sentiment import invalidate_sentiment_cache

bp = Blueprint("keywords", __name__)


@bp.route("/settings/keywords", methods=["POST"])
def settings_keywords():
    begin_page_request()
    success = ""
    warning = ""
    action = request.form.get("action", "")
    label = request.form.get("label", "")
    word = request.form.get("word", "").strip()

    if action == "add":
        if add_word(label, word):
            invalidate_sentiment_cache()
            Logger.log_info(f"감정 키워드 추가: {label} / {word}")
            success = f"감정 키워드 '{word}'({label})이(가) 추가되었습니다."
        else:
            warning = "키워드를 추가하지 못했습니다. 라벨·중복·빈 값을 확인하세요."
    elif action == "delete":
        try:
            word_id = int(request.form.get("word_id", "0"))
        except ValueError:
            word_id = 0
        if delete_word(word_id):
            invalidate_sentiment_cache()
            Logger.log_info(f"감정 키워드 삭제: id={word_id}")
            success = "감정 키워드가 삭제되었습니다."
        else:
            warning = "삭제할 키워드를 찾지 못했습니다."

    feedbacks = get_session().get_current_feedbacks()
    return render_page(
        success=success,
        warning=warning,
        keyword_entries=list_all(),
        feedbacks=feedbacks,
    )
