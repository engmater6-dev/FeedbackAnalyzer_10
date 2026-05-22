# 코드 스멜 분석 보고서 — `src/python/`

| 항목 | 내용 |
|------|------|
| 일자 | 2026-05-22 |
| 기준 문서 | [doc/PRD.md](../doc/PRD.md), [report/MOM_TEST.md](MOM_TEST.md), [README.md](../README.md) |
| 분석 대상 | `src/python/*.py` (8모듈) |

---

## 1. 요약

| 구분 | 개수 | 비고 |
|------|------|------|
| 구조·설계 스멜 | 12 | God Function, 전역 상태, 레이어 혼재 |
| 중복·일관성 스멜 | 6 | PRD B-01, B-02 직접 원인 |
| 네이밍·가독성 | 5 | README Phase 3 |
| 죽은 코드·미사용 | 4 | Lava Flow |
| 테스트·관측성 | 3 | 커버리지 90% 목표 |
| **버그 유발 스멜** | **4** | Mom Test 실무 ❌ Fail |

**핵심 원인**: 동일 도메인 규칙이 **3곳**에 다르게 존재 — `constants.py` / `filters.S_KEYWORDS` / `text_analyzer`·`filter_feedbacks` 분기.

---

## 2. 파일별 스멜

### 2.1 `app.py`

| ID | 스멜 | 심각도 | 위치·설명 |
|----|------|--------|-----------|
| S-A01 | God Function | High | `render_page()` ~135줄 — CSS·HTML·폼·결과 일체 |
| S-A02 | God Module | High | 라우팅·비즈니스·프레젠테이션·CSV 혼재 |
| S-A03 | 전역 `fil_data` | High | `/filter`만 갱신 → 다운로드 불일치 (B-03) |
| S-A04 | 불필요한 `global fil_data` | Low | `analyze`에서 선언만 하고 미사용 |
| S-A05 | Primitive Obsession | Med | `list`, `dict`만 전달, 도메인 모델 빈약 |
| S-A06 | CSV 스펙 불일치 | Med | 0번 컬럼·첫 행 무조건 스킵 (B-04) |
| S-A07 | 업로드 후 분석 누락 | Low | `/upload`가 `sent`/`kw` 미호출 (B-05) |

### 2.2 `text_analyzer.py`

| ID | 스멜 | 심각도 | 위치·설명 |
|----|------|--------|-----------|
| S-T01 | 부적절한 네이밍 | Med | `sent`, `kw` |
| S-T02 | 클래스 변수 부작용 | High | `global_sent`, `global_kw` |
| S-T03 | 중복 `_contains_any` | High | `filters.py`와 동일 |
| S-T04 | 불완전한 감정 규칙 | High | 중립 키워드 없음 → else만 중립 (B-01) |
| S-T05 | `kw()` main만 매칭 | High | `filter`와 sub/main 불일치 (B-02) |

### 2.3 `filters.py`

| ID | 스멜 | 심각도 | 위치·설명 |
|----|------|--------|-----------|
| S-F01 | 데이터 3중 정의 | **Critical** | `S_KEYWORDS` ≠ `constants.SENTIMENT_KEYWORDS` |
| S-F02 | 감정 규칙 불일치 | **Critical** | 3단계+중립 키워드 vs analyzer 2단계+else |
| S-F03 | 카테고리 `main` 스킵 | **Critical** | L60-62 `continue` on `main` |
| S-F04 | Debug 잔류 | Med | L69-70 `print(fb.text)` |
| S-F05 | Feature Envy | High | `CATEGORY_KEYWORDS` sub_key 순회 |
| S-F06 | 키워드 충돌 | Med | `괜찮`이 긍정·중립 양쪽 |

### 2.4 `constants.py`

| ID | 스멜 | 심각도 |
|----|------|--------|
| S-C01 | 하드코딩 | Med |
| S-C02 | 불완전한 SSOT | High — filters가 감정은 별도 사전 사용 |
| S-C03 | 과도한 중첩 dict | Low |

### 2.5 `session.py`

| ID | 스멜 | 심각도 |
|----|------|--------|
| S-S01 | 클래스 변수 전역 상태 | High |
| S-S02 | 빈 `init_session()` | Med |
| S-S03 | `update_current_feedbacks` 미사용 | Low |

### 2.6 `feedback.py`

| ID | 스멜 | 심각도 |
|----|------|--------|
| S-FB01 | Anemic Domain Model | Med |
| S-FB02 | setter·분석 결과 없음 | Low |

### 2.7 `logger.py`

| ID | 스멜 | 심각도 |
|----|------|--------|
| S-L01 | UI와 단절된 print Logger | Med |
| S-L02 | warning/error 미표시 (B-06) | Med |

### 2.8 `file_handler.py`

| ID | 스멜 | 심각도 |
|----|------|--------|
| S-FH01 | Lava Flow / Dead Code | Low |
| S-FH02 | print만 하는 save | Low |

---

## 3. 안티패턴 ↔ 코드

| 안티패턴 | 코드 |
|----------|------|
| God Function | `app.render_page` |
| Spaghetti Code | Session + fil_data + global_sent/kw |
| Shotgun Surgery | constants + S_KEYWORDS + analyzer |
| Feature Envy | filters → CATEGORY_KEYWORDS 구조 |
| Lava Flow | file_handler.py |

---

## 4. 스멜 → PRD 버그 → Mom Test

| 스멜 | PRD | Mom Test |
|------|-----|----------|
| S-F01, S-F02, S-T04 | B-01 | H-02 ❌ |
| S-F03, S-T05 | B-02 | H-03, H-04 ❌ |
| S-A03 | B-03 | 다운로드 신뢰 |
| S-A06 | B-04 | H-05 ❌ |
| S-A07 | B-05 | — |
| S-L02 | B-06 | — |

---

## 5. 검증 시나리오 (수정 후)

| # | 입력 | 기대 |
|---|------|------|
| 1 | `"배송이 너무 늦어요. 화가 납니다."` | sent→부정, filter(부정,배송)≥1 |
| 2 | 중립 샘플 3건 | sent 중립 수 = filter(중립) 건수 |
| 3 | `"배송"` only | kw 배송 = filter(배송) |
| 4 | CSV header `text` | 업로드 건수 = 파일 행 수 |

---

## 6. 리팩토링 권장 순서

1. `classify_sentiment()` 단일화 — `S_KEYWORDS` 제거  
2. `match_category()` 단일화 — main+sub 동일 규칙  
3. `fil_data` 제거 → 세션/DTO  
4. `render_page` → 템플릿/HtmlRenderer  
5. pytest + Mom Test §8 체크리스트 고정  

---

## 7. 참고

- [MOM_TEST.md](MOM_TEST.md)
- [doc/PRD.md](../doc/PRD.md) §4, §5
