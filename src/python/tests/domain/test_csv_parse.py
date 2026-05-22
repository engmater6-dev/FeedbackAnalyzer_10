# -*- coding: utf-8 -*-
import pytest
from app import _parse_csv_to_feedbacks


@pytest.mark.domain
class TestCsvParse:
    def test_empty_content(self):
        assert _parse_csv_to_feedbacks("") == []

    def test_no_text_header_uses_column_zero(self):
        rows = _parse_csv_to_feedbacks("첫줄데이터\n둘째줄\n")
        assert len(rows) == 2
        assert rows[0].text == "첫줄데이터"
