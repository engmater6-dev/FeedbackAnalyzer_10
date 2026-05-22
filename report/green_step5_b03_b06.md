# Green Step 5 — B-03~B-06 적용

| 항목 | 내용 |
|------|------|
| 일자 | 2026-05-22 |
| 브랜치 | `green` |
| 목적 | Phase 2 README 항목 — 다운로드·CSV·업로드 UX·로그 UI |

## 변경

| PRD | 작업 | 파일 |
|-----|------|------|
| B-03 | `fil_data` 제거 → `Session.download_feedbacks` | `app.py`, `session.py` |
| B-04 | CSV `text` 헤더 컬럼 파싱 (`_parse_csv_to_feedbacks`) | `app.py` |
| B-05 | 업로드 직후 `sent`/`kw` 집계·안내 문구 | `app.py` |
| B-06 | warning/error 페이지 표시, level별 on/off 플래그 | `logger.py`, `app.py` |

## 검증

```bash
pytest tests/domain/test_anchor_prd_example.py tests/domain/test_filters_regression.py -v
```

| 항목 | 결과 |
|------|------|
| Domain Gate | 6 passed |

## 수동 확인 (권장)

- `/analyze` 후 `/download` — 입력 피드백 포함
- `/filter` 후 `/download` — 필터 결과만
- CSV 헤더 `text` 컬럼 업로드
- 필터 0건 시 warning이 페이지에 표시

## 다음

Step 6: cov 90%+, boundary 통합 테스트
