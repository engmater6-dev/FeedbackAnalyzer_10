# Green Step 6 — 테스트·UX·커버리지

| 항목 | 내용 |
|------|------|
| 일자 | 2026-05-22 |
| 브랜치 | `green` |
| 목적 | DEF-010~014, Phase 1 DoD (cov 90%+, IT) |

## 변경

| DEF | 작업 |
|-----|------|
| DEF-010 | `.coveragerc`, 38 tests, **cov 97.42%** (`--cov-fail-under=90`) |
| DEF-011 | `tests/boundary/` IT-01~04 (skip 해제) |
| DEF-012 | `test_post_upload_text_header_csv` |
| DEF-013 | `_begin_page_request()` — 요청 단위 로그 버퍼 |
| DEF-014 | 빈 `/download` → warning HTML, 다운로드 버튼 조건부 |

## 검증

```bash
cd src/python
pytest tests/ --cov --cov-fail-under=90 -q
```

| 항목 | 결과 |
|------|------|
| Tests | **38 passed** |
| Coverage | **97.42%** |

## 잔여 (Phase 3+)

DEF-015~022, DEF-008 UI 토글, Phase 0 수동 `app.py` 확인
