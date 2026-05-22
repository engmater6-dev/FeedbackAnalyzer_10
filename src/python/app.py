# -*- coding: utf-8 -*-
from flask import Flask

from handlers import register_blueprints
from logger import Logger
from services.csv_parser import parse_csv_to_feedbacks

app = Flask(__name__)
register_blueprints(app)

# Compatibility shim for tests importing from app
_parse_csv_to_feedbacks = parse_csv_to_feedbacks


if __name__ == "__main__":
    Logger.log_info("서버가 http://localhost:8080 에서 시작됩니다.")
    app.run(host="0.0.0.0", port=8080)
