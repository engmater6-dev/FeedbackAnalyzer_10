# -*- coding: utf-8 -*-
from flask import Blueprint

from handlers._common import begin_page_request
from html_renderer import render_page
from models.session import get_session

bp = Blueprint("dashboard", __name__)


@bp.route("/", methods=["GET"])
def index():
    begin_page_request()
    session = get_session()
    session.init_session()
    feedbacks = session.get_current_feedbacks()
    return render_page(success="피드백 분석기 시작", feedbacks=feedbacks)
