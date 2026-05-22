# -*- coding: utf-8 -*-
import pytest
from logger import Logger


@pytest.mark.domain
class TestLogger:
    def test_warning_appears_on_page_when_enabled(self):
        Logger.show_warning_on_page = True
        Logger.log_warning("테스트 경고")
        logs = Logger.get_page_logs()
        assert len(logs) == 1
        assert logs[0]["level"] == "warning"

    def test_warning_hidden_when_disabled(self):
        Logger._ui_logs = []
        Logger.show_warning_on_page = False
        Logger.log_warning("숨김")
        assert Logger.get_page_logs() == []
        Logger.show_warning_on_page = True

    def test_error_on_page(self):
        Logger.show_error_on_page = True
        Logger.log_error("테스트 오류")
        logs = Logger.get_page_logs()
        assert logs[0]["level"] == "error"

    def test_error_hidden_when_disabled(self):
        Logger._ui_logs = []
        Logger.show_error_on_page = False
        Logger.log_error("숨김")
        assert Logger.get_page_logs() == []
        Logger.show_error_on_page = True

    def test_debug_and_set_debug_mode(self):
        Logger.set_debug_mode(True)
        Logger.log_debug("debug msg")
        Logger.set_debug_mode(False)
        Logger.log_debug("hidden")

    def test_info_on_page_when_enabled(self):
        Logger._ui_logs = []
        Logger.show_info_on_page = True
        Logger.log_info("페이지 정보")
        logs = Logger.get_page_logs()
        assert len(logs) == 1
        assert logs[0]["level"] == "info"

    def test_info_hidden_when_disabled(self):
        Logger._ui_logs = []
        Logger.show_info_on_page = False
        Logger.log_info("stdout only")
        assert Logger.get_page_logs() == []

    def test_apply_display_settings(self):
        Logger.apply_display_settings(
            show_warning=False,
            show_error=True,
            show_info=True,
        )
        assert Logger.show_warning_on_page is False
        assert Logger.show_error_on_page is True
        assert Logger.show_info_on_page is True
