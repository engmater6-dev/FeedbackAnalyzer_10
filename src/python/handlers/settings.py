# -*- coding: utf-8 -*-
from flask import Blueprint, request

from handlers._common import begin_page_request
from html_renderer import render_page
from logger import Logger
from models.session import Session

bp = Blueprint("settings", __name__)


@bp.route("/settings/logs", methods=["POST"])
def settings_logs():
    begin_page_request()
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
