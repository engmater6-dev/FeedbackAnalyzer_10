# -*- coding: utf-8 -*-
"""SQLite store for sentiment keywords (R-10, S-C01/S-C02)."""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional

from constants import SENTIMENT_KEYWORDS

VALID_LABELS = ("긍정", "부정")
_DEFAULT_DIR = Path(__file__).resolve().parent.parent / "data"

_connection: Optional[sqlite3.Connection] = None
_db_path_override: Optional[str] = None
_db_initialized = False


def get_db_path() -> Path:
    if _db_path_override:
        return Path(_db_path_override)
    env = os.environ.get("FEEDBACK_KEYWORD_DB")
    if env:
        return Path(env)
    return _DEFAULT_DIR / "sentiment_keywords.db"


def set_db_path(path: Optional[str]) -> None:
    global _db_path_override, _connection, _db_initialized
    _db_path_override = path
    reset_db_connection()
    _db_initialized = False


def reset_db_connection() -> None:
    global _connection, _db_initialized
    if _connection is not None:
        _connection.close()
        _connection = None
    _db_initialized = False


def get_connection() -> sqlite3.Connection:
    global _connection
    if _connection is None:
        path = get_db_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        _connection = sqlite3.connect(str(path), check_same_thread=False)
        _connection.row_factory = sqlite3.Row
    return _connection


def init_db() -> None:
    conn = get_connection()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS sentiment_keyword (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL CHECK (label IN ('긍정', '부정')),
            word TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_sentiment_label
            ON sentiment_keyword(label);
        """
    )
    conn.commit()


def ensure_db_ready() -> None:
    global _db_initialized
    if _db_initialized:
        return
    init_db()
    seed_from_constants_if_empty()
    _db_initialized = True


def _raw_word_count() -> int:
    row = get_connection().execute(
        "SELECT COUNT(*) AS c FROM sentiment_keyword"
    ).fetchone()
    return int(row["c"])


def count_words() -> int:
    ensure_db_ready()
    return _raw_word_count()


def seed_from_constants_if_empty() -> int:
    if _raw_word_count() > 0:
        return 0
    conn = get_connection()
    added = 0
    for label, words in SENTIMENT_KEYWORDS.items():
        if label not in VALID_LABELS:
            continue
        for word in words:
            try:
                conn.execute(
                    "INSERT INTO sentiment_keyword (label, word) VALUES (?, ?)",
                    (label, word),
                )
                added += 1
            except sqlite3.IntegrityError:
                pass
    conn.commit()
    return added


def list_all() -> List[Dict[str, object]]:
    ensure_db_ready()
    rows = get_connection().execute(
        "SELECT id, label, word, created_at FROM sentiment_keyword "
        "ORDER BY label, word"
    ).fetchall()
    return [
        {
            "id": row["id"],
            "label": row["label"],
            "word": row["word"],
            "created_at": row["created_at"],
        }
        for row in rows
    ]


def add_word(label: str, word: str) -> bool:
    if label not in VALID_LABELS:
        return False
    word = word.strip()
    if not word:
        return False
    ensure_db_ready()
    try:
        get_connection().execute(
            "INSERT INTO sentiment_keyword (label, word) VALUES (?, ?)",
            (label, word),
        )
        get_connection().commit()
        return True
    except sqlite3.IntegrityError:
        return False


def delete_word(word_id: int) -> bool:
    ensure_db_ready()
    cur = get_connection().execute(
        "DELETE FROM sentiment_keyword WHERE id = ?", (word_id,)
    )
    get_connection().commit()
    return cur.rowcount > 0


def get_sentiment_keyword_map() -> Dict[str, List[str]]:
    ensure_db_ready()
    result: Dict[str, List[str]] = {"긍정": [], "부정": []}
    for row in list_all():
        result[row["label"]].append(str(row["word"]))
    return result
