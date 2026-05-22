# ADR-001: 카테고리 매칭 — main 키워드만 사용

| 항목 | 내용 |
|------|------|
| 상태 | **Accepted** (2026-05-22, Phase 3-B) |
| 결함 | DEF-016 |
| 구현 | `text_analyzer.matches_category()`, `filters.filter_feedbacks` |
| 대안 | sub 키워드(`time`, `type`, `status` 등)까지 OR 매칭 |

---

## 맥락

`constants.CATEGORY_KEYWORDS`는 카테고리마다 `main`과 여러 `sub` 맵을 가진다. Red 시점에는 `filter_feedbacks`가 `sub_key == "main"`을 **스킵**해 `kw()`와 불일치했다. Green에서 `matches_category()`가 **`main` 리스트만** substring 매칭하도록 통일했다 (B-02).

Mom Test·Domain 테스트 `"품질"` only, `"배송이 너무 늦어요..."` 등은 이 정책 하에 **Pass**한다.

---

## 결정

**v1(실습·Green~Phase 3)에서는 카테고리 판정에 `main` 키워드만 사용한다.**  
`sub` 맵은 분류 체계·향후 확장용 메타데이터로 두고, 런타임 매칭에는 포함하지 않는다.

```text
matches_category(text, category) :=
  ∃ kw ∈ CATEGORY_KEYWORDS[category]["main"] : kw in text
```

- `TextAnalyzer.kw()` · `filter_feedbacks()` · Golden Master는 동일 함수를 사용한다.
- Phase 5에서 Mom Test 인터뷰 결과 **Trend/DB Go**일 때만 sub 확장을 재검토한다.

---

## 근거

| 항목 | 설명 |
|------|------|
| SSOT | 한 함수로 집계·필터 일치 (B-02, DEF-004) |
| 테스트 | `test_filters_regression`, TP-ANCHOR, Golden `[category_main_only]` 고정 |
| 범위 | 실습 목표는 버그 수정·리팩터링이지 NLP 정밀 분류가 아님 |
| 리스크 통제 | sub까지 OR 하면 `constants` 변경 시 Shotgun Surgery·회귀 증가 |

---

## 결과·트레이드오프

### 장점

- 분석(`kw`)과 필터 건수 **항상 일치**
- 키워드 추가 시 `constants`의 `main`만 수정하면 됨

### 제한 (의도적)

- 본문에 **main에 없는** 표현만 있으면 해당 카테고리 0건 (예: 향후 sub 전용 신조어만 있는 문장)
- 다중 카테고리 동시 매칭 가능 (한 피드백이 배송·품질 모두 +1) — 집계는 **건수 합**이지 단일 라벨이 아님

### 예시

| 본문 | 배송 `kw` | 비고 |
|------|-----------|------|
| `품질` | 0 | 품질 카테고리 1 |
| `배송이 너무 늦어요` | 1 | `배송` ∈ main |
| `택배가 빨라요` | 1 | `택배` ∈ main |
| (가상) sub 전용 용어만 | 0 | **Won't fix** until ADR 재개 |

---

## Phase 5 재검토 조건

다음이 **모두** 충족될 때 ADR-002로 sub 확장 검토:

1. Mom Test 인터뷰에서 “sub 태그로 세분 필터” 니즈 **Go**
2. `matches_category` 변경 + Domain·Golden Master `--force` 갱신
3. [defect_list.md](defect_list.md) DEF-016 **완료** 또는 **Won't fix** 명시

**현재 (Phase 5 · `new_feature`):** sub 확장 **No-Go** — 문서화로 DEF-016 **완료** 처리. Trend·감정 DB는 별도(R-09/R-10).

---

## 참고

- [PRD.md](PRD.md) §2.5
- [CODE_SMELL.md](CODE_SMELL.md) S-F03, S-T05
- `src/python/text_analyzer.py` — `matches_category()`
