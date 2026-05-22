# Green Step 0 — Red 기준선 재확인

| 항목 | 내용 |
|------|------|
| 일자 | 2026-05-22 |
| 브랜치 | `green` |
| 목적 | Green 착수 전 TDD Red Gate 동일 여부 확인 |

## 실행

```bash
cd src/python
pytest tests/domain/test_anchor_prd_example.py tests/domain/test_filters_regression.py -v
```

## 결과

| 항목 | 값 |
|------|-----|
| 수집 | 6 |
| **failed** | **4** |
| **passed** | **2** |
| 판정 | ✅ Red 기준선 유지 (Green Step 1~2 착수 가능) |

### Passed (2)

- `test_kw_classifies_anchor_as_shipping`
- `test_sent_negative_count_matches_filter_negative_all`

### Failed — 의도적 (4)

- `test_sent_classifies_anchor_as_negative` → B-01
- `test_filter_negative_and_shipping_returns_at_least_one` → B-01
- `test_sent_neutral_count_equals_filter_neutral_count` → B-01
- `test_kw_category_count_equals_filter_category_count` → B-02

## 다음

Step 1: B-01 (`S_KEYWORDS` 제거, `constants` 단일 감정 규칙)
