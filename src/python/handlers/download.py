# -*- coding: utf-8 -*-
import io

from flask import Blueprint, Response

from handlers._common import begin_page_request
from html_renderer import render_page
from logger import Logger
from models.session import get_session

bp = Blueprint("download", __name__)


@bp.route("/download", methods=["GET"])
def download():
    begin_page_request()
    rows = get_session().get_download_feedbacks()
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
