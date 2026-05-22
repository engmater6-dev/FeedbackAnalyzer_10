# -*- coding: utf-8 -*-
from flask import Blueprint

from handlers._common import begin_page_request
from html_renderer import render_page
from models.session import Session

bp = Blueprint("dashboard", __name__)


@bp.route("/", methods=["GET"])
def index():
    begin_page_request()
    Session.init_session()
    feedbacks = Session.get_current_feedbacks()
    return render_page(success="피드백 분석기 시작", feedbacks=feedbacks)
