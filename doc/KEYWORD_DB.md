# 감정 키워드 File DB (SQLite)

| 항목 | 내용 |
|------|------|
| 문서 ID | SPEC-KW-DB-01 |
| PRD | R-10 |
| 구현 | `services/keyword_db.py`, `services/sentiment.py` |
| UI | `POST /settings/keywords`, 대시보드 **감정 키워드 관리** 섹션 |

---

## 1. 개요

- **런타임 SSOT:** SQLite `sentiment_keyword` 테이블
- **시드:** 최초 빈 DB 시 `constants.SENTIMENT_KEYWORDS` 1회 적재
- **카테고리 키워드:** `constants.CATEGORY_KEYWORDS` 유지 (ADR-001 main-only)

---

## 2. 스키마

```sql
CREATE TABLE sentiment_keyword (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL CHECK (label IN ('긍정', '부정')),
    word TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
```

| 컬럼 | 설명 |
|------|------|
| label | `긍정` 또는 `부정` |
| word | 본문 substring 매칭 (중립은 키워드 없음) |

---

## 3. 분류 규칙 (B-01 유지)

1. 긍정 키워드 매칭 → `긍정`
2. 부정 키워드 매칭 → `부정`
3. else → `중립`

`filter_service` · `TextAnalyzer` · Golden Master는 `classify_sentiment()` 단일 경로.

---

## 4. CRUD

| 동작 | HTTP | 필드 |
|------|------|------|
| 목록 | 대시보드 렌더 | `list_all()` |
| 추가 | `POST /settings/keywords` | `action=add`, `label`, `word` |
| 삭제 | `POST /settings/keywords` | `action=delete`, `word_id` |

CRUD 후 `invalidate_sentiment_cache()` 호출.

---

## 5. 파일 경로

| 환경 | 경로 |
|------|------|
| 기본 | `src/python/data/sentiment_keywords.db` |
| 테스트 | pytest `tmp_path` (conftest) |
| override | 환경 변수 `FEEDBACK_KEYWORD_DB` |

DB 파일은 git에 포함하지 않음 (`.gitignore`).

---

## 6. 검증

```bash
cd src/python
pytest tests/domain/test_keyword_db.py tests/boundary/test_routes_keywords.py -v
pytest tests/ --cov --cov-fail-under=90 -q
python scripts/generate_golden_master.py --check
```
