# -*- coding: utf-8 -*-
from flask import Flask

from handlers.analyze import bp as analyze_bp
from handlers.dashboard import bp as dashboard_bp
from handlers.download import bp as download_bp
from handlers.filter_route import bp as filter_bp
from handlers.keywords import bp as keywords_bp
from handlers.settings import bp as settings_bp
from handlers.upload import bp as upload_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(keywords_bp)
    app.register_blueprint(analyze_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(filter_bp)
    app.register_blueprint(download_bp)
