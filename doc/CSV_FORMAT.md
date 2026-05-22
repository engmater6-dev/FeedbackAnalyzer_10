# CSV 업로드 형식 규격

| 항목 | 내용 |
|------|------|
| 문서 ID | SPEC-CSV-01 |
| 버전 | 1.0 (Phase 3-B) |
| 구현 | `app._parse_csv_to_feedbacks()` (B-04) |
| 결함 | DEF-015 (문서화), DEF-006 (구현 완료) |
| 테스트 | `tests/domain/test_csv_parse.py`, `test_post_upload_text_header_csv` |

---

## 1. 권장 형식 (표준)

첫 행에 **`text`** 컬럼 헤더를 둔 UTF-8 CSV.

```csv
text
배송이 너무 늦어요. 화가 납니다.
최고입니다 만족해요
```

| 규칙 | 내용 |
|------|------|
| 인코딩 | UTF-8 (BOM `utf-8-sig` 업로드 허용) |
| 헤더 | 첫 행, 셀 이름 `text` (**대소문자 무시** — 파서는 소문자 비교) |
| 데이터 | 2행부터, `text` 열의 비어 있지 않은 셀만 피드백으로 적재 |
| 빈 행 | 무시 (빈 줄·빈 셀만 있는 행 스킵) |

---

## 2. 레거시 형식 (헤더 없음)

헤더 행에 `text`가 **없으면** **0번 컬럼**을 모든 행에서 읽는다.

```csv
첫줄데이터
둘째줄
```

| 규칙 | 내용 |
|------|------|
| 헤더 없음 | **첫 행도 데이터**로 처리 (헤더 스킵 없음) |
| 컬럼 | 인덱스 `0`만 사용, 나머지 열 무시 |
| 용도 | 구버전 샘플·단일 열 메모 호환 |

> **주의:** 첫 줄이 컬럼명(`id,text`)인데 `text`가 소문자가 아니거나 다른 이름이면 레거시 모드로 들어가 첫 줄이 피드백 본문으로 들어갈 수 있다. **운영·실습에서는 §1 권장 형식만 사용.**

---

## 3. 파서 동작 요약

```text
rows = CSV 전체 (빈 row 제외)
if rows[0]에 "text" ∈ header (lower):
    text_col = index("text")
    data_rows = rows[1:]
else:
    text_col = 0
    data_rows = rows          # 첫 행 포함

각 data_row: row[text_col].strip() 비어 있지 않으면 Feedback 생성
```

---

## 4. 업로드 후 동작 (B-05)

| 단계 | 동작 |
|------|------|
| POST `/upload` | 파싱 → `Session.current_feedbacks` **교체** |
| 직후 | `sent` / `kw` 집계 후 HTML stats 표시 |
| 실패 | 파싱 0건 → warning 로그·안내 문구 |

---

## 5. 다운로드 형식

`GET /download` 응답 CSV:

```csv
text
<피드백 본문 1>
<피드백 본문 2>
```

항상 `text` 헤더 1행 + 본문 열 (표준 형식과 동일).

---

## 6. 검증·Mom Test

| 검사 | 기대 | 테스트 |
|------|------|--------|
| `text` 헤더 2행 | 피드백 1건 이상 | boundary IT |
| 헤더 없음 2행 | 2건, 첫 줄=첫 데이터 | `test_no_text_header_uses_column_zero` |
| 빈 파일 | 0건, warning | upload IT |

---

## 8. Trend 샘플 CSV (Phase 5, R-09)

학습·데모용: [sample/test_feedback_trend.csv](../sample/test_feedback_trend.csv)

| 컬럼 | 필수 | 형식 |
|------|------|------|
| `date` | Trend 샘플에서 권장 | `YYYY-MM-DD` — #11 추이 집계용 |
| `text` | ✅ | [§1](#1-권장-형식-표준)과 동일 |

```csv
date,text
2026-01-10,배송이 너무 늦어요. 화가 납니다.
```

| 단계 | 파서 동작 |
|------|-----------|
| `text`만 헤더 | B-04 `parse_csv_to_feedbacks` |
| `date`+`text` 헤더 | `parse_trend_csv_to_feedbacks` → `Feedback.recorded_at` |
| 업로드 진입점 | `parse_csv_content()` — 헤더 자동 판별 |
| UI | `services/trend_service` 월별 집계 → 대시보드 **월별 추이** 섹션 |

---

## 7. 변경 이력

| 버전 | 일자 | 변경 |
|------|------|------|
| 1.1 | 2026-05-22 | §8 Trend 샘플 `date,text` (R-09) |
| 1.0 | 2026-05-22 | Phase 3-B — B-04 구현 기준 명세 (DEF-015) |
