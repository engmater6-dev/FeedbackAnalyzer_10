# -*- coding: utf-8 -*-
import csv
import io

from models.feedback import Feedback
from services.trend_csv_parser import is_trend_csv, parse_trend_csv_to_feedbacks


def parse_csv_to_feedbacks(content: str) -> list:
    """B-04: use `text` column when header present, else column 0."""
    reader = csv.reader(io.StringIO(content))
    rows = [row for row in reader if row]
    if not rows:
        return []

    header = [cell.strip().lower() for cell in rows[0]]
    if "text" in header:
        text_col = header.index("text")
        data_rows = rows[1:]
    else:
        text_col = 0
        data_rows = rows

    feedbacks = []
    for row in data_rows:
        if len(row) > text_col:
            text = row[text_col].strip()
            if text:
                feedbacks.append(Feedback(text))
    return feedbacks


def parse_csv_content(content: str) -> list:
    """B-04 standard CSV, or date,text trend CSV when header has both columns."""
    if is_trend_csv(content):
        return parse_trend_csv_to_feedbacks(content)
    return parse_csv_to_feedbacks(content)
