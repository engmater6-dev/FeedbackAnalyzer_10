# -*- coding: utf-8 -*-
import csv
import io
import re

from models.feedback import Feedback

_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def is_trend_csv(content: str) -> bool:
    """True when header row includes both date and text columns."""
    reader = csv.reader(io.StringIO(content))
    rows = [row for row in reader if row]
    if not rows:
        return False
    header = [cell.strip().lower() for cell in rows[0]]
    return "text" in header and "date" in header


def parse_trend_csv_to_feedbacks(content: str) -> list:
    """Parse date,text CSV into Feedback with recorded_at (R-09)."""
    reader = csv.reader(io.StringIO(content))
    rows = [row for row in reader if row]
    if not rows:
        return []

    header = [cell.strip().lower() for cell in rows[0]]
    if "text" not in header:
        return []

    text_col = header.index("text")
    date_col = header.index("date") if "date" in header else None
    data_rows = rows[1:]

    feedbacks = []
    for row in data_rows:
        if len(row) <= text_col:
            continue
        text = row[text_col].strip()
        if not text:
            continue
        recorded_at = None
        if date_col is not None and len(row) > date_col:
            raw_date = row[date_col].strip()
            if raw_date and _DATE_PATTERN.match(raw_date):
                recorded_at = raw_date
        feedbacks.append(Feedback(text, recorded_at=recorded_at))
    return feedbacks
