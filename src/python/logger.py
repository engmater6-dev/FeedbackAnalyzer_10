# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List, Dict


class Logger:
    debug_mode = True
    show_warning_on_page = True
    show_error_on_page = True
    _ui_logs: List[Dict[str, str]] = []

    @staticmethod
    def _timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def _append_ui(cls, level: str, message: str):
        cls._ui_logs.append(
            {"level": level, "message": message, "timestamp": cls._timestamp()}
        )
        if len(cls._ui_logs) > 100:
            cls._ui_logs = cls._ui_logs[-100:]

    @classmethod
    def get_page_logs(cls) -> List[Dict[str, str]]:
        visible = []
        for entry in cls._ui_logs:
            if entry["level"] == "warning" and cls.show_warning_on_page:
                visible.append(entry)
            elif entry["level"] == "error" and cls.show_error_on_page:
                visible.append(entry)
        return visible

    @classmethod
    def log_info(cls, message: str):
        print(f"[{cls._timestamp()}] INFO: {message}")

    @classmethod
    def log_warning(cls, message: str):
        print(f"[{cls._timestamp()}] WARNING: {message}")
        cls._append_ui("warning", message)

    @classmethod
    def log_error(cls, message: str):
        import sys
        print(f"[{cls._timestamp()}] ERROR: {message}", file=sys.stderr)
        cls._append_ui("error", message)

    @classmethod
    def log_debug(cls, message: str):
        if cls.debug_mode:
            print(f"[{cls._timestamp()}] DEBUG: {message}")

    @classmethod
    def set_debug_mode(cls, mode: bool):
        cls.debug_mode = mode
