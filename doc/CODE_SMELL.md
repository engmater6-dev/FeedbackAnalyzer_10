# 코드 스멜 분석 보고서 — `src/python/`

| 항목 | 내용 |
|------|------|
| 일자 | 2026-05-22 |
| 갱신 | Phase 3-B — Green 해소 스멜 표기 |
| 기준 문서 | [PRD.md](PRD.md), [MOM_TEST.md](MOM_TEST.md), [README.md](../README.md), [ADR-001](ADR-001-category-main-only.md) |
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

**Red 시 핵심 원인**: 감정·카테고리 규칙이 `constants` / `filters.S_KEYWORDS` / analyzer에 **이중화**.  
**Green 후**: `classify_sentiment()`, `matches_category()` SSOT — 아래 **✅ Green** 항목은 Phase 2에서 해소, Phase 3-C에서 구조 스멜 잔여.

---

## 1.1 Green 해소 요약 (2026-05-22)

| 스멜 ID | PRD | Green 조치 | 상태 |
|---------|-----|------------|------|
| S-F01, S-F02 | B-01 | `S_KEYWORDS` 제거, `classify_sentiment()` | ✅ |
| S-F03, S-T05 | B-02 | `matches_category()` main-only ([ADR-001](ADR-001-category-main-only.md)) | ✅ |
| S-T04 | B-01 | 감정 else→중립, `화가` 등 constants | ✅ |
| S-A03, S-A04 | B-03 | `fil_data` 제거 → Session | ✅ |
| S-A06 | B-04 | `_parse_csv_to_feedbacks` ([CSV_FORMAT](CSV_FORMAT.md)) | ✅ |
| S-A07 | B-05 | upload 후 sent/kw | ✅ |
| S-F04 | — | `filters` print 제거 | ✅ |
| S-L02 | B-06 | Logger 페이지 warning/error/info 토글 | ✅ 3-C-4 |
| S-T02 | — | `global_sent`/`global_kw` 클래스 변수 제거 (3-C-1) | ✅ |
| S-A01, S-A02 | — | `HtmlRenderer` / `html_renderer.py` (3-C-2) | ✅ |
| S-FH01, S-FH02 | — | `file_handler.py` 삭제 (3-C-3) | ✅ |
| S-T01, S-T03 | — | 네이밍·contains_any (3-C-5~6) | ✅ |
| — | — | `analysis_strategies` (3-C-7) | ✅ |

**Phase 3-C:** ✅ 완료 · Phase 4~6·문서 DEF-020~022 잔여

---

## 2. 파일별 스멜

### 2.1 `app.py`

| ID | 스멜 | 심각도 | 위치·설명 |
|----|------|--------|-----------|
| S-A01 | God Function | High | ~~`render_page()` in app~~ → **✅ 3-C-2** `html_renderer.HtmlRenderer` |
| S-A02 | God Module | High | ~~프레젠테이션 혼재~~ → **✅ 3-C-2** app=라우팅·I/O, html_renderer=UI |
| S-A03 | 전역 `fil_data` | High | ~~B-03~~ → **✅ Green** Session.download |
| S-A04 | 불필요한 `global fil_data` | Low | ~~제거됨~~ **✅ Green** |
| S-A05 | Primitive Obsession | Med | `list`, `dict`만 전달, 도메인 모델 빈약 |
| S-A06 | CSV 스펙 불일치 | Med | ~~B-04~~ → **✅ Green** [CSV_FORMAT](CSV_FORMAT.md) |
| S-A07 | 업로드 후 분석 누락 | Low | ~~B-05~~ → **✅ Green** |

### 2.2 `text_analyzer.py`

| ID | 스멜 | 심각도 | 위치·설명 |
|----|------|--------|-----------|
| S-T01 | 부적절한 네이밍 | Med | ~~`sent`, `kw`~~ → **✅ 3-C-5** `analyze_sentiments`/`analyze_keywords` |
| S-T02 | 클래스 변수 부작용 | High | ~~`global_sent`, `global_kw`~~ → **✅ 3-C-1** 제거 |
| S-T03 | 중복 `_contains_any` | High | ~~중복~~ → **✅ 3-C-6** `text_utils.contains_any` |
| S-T04 | 불완전한 감정 규칙 | High | ~~B-01~~ → **✅ Green** `classify_sentiment()` |
| S-T05 | `kw()` main만 매칭 | High | ~~B-02~~ → **✅ Green** `matches_category()` ([ADR-001](ADR-001-category-main-only.md)) |

### 2.3 `filters.py`

| ID | 스멜 | 심각도 | 위치·설명 |
|----|------|--------|-----------|
| S-F01 | 데이터 3중 정의 | **Critical** | ~~`S_KEYWORDS`~~ → **✅ Green** 제거 |
| S-F02 | 감정 규칙 불일치 | **Critical** | ~~이중 규칙~~ → **✅ Green** SSOT |
| S-F03 | 카테고리 `main` 스킵 | **Critical** | ~~filter 스킵~~ → **✅ Green** main-only 정책 |
| S-F04 | Debug 잔류 | Med | ~~print~~ → **✅ Green** 제거 |
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
| S-L02 | warning/error 미표시 (B-06) | Med | ~~B-06~~ → **✅ Green** (UI 토글 DEF-008 잔여) |

### 2.8 `file_handler.py` — **제거됨 (3-C-3)**

| ID | 스멜 | 상태 |
|----|------|------|
| S-FH01 | Lava Flow / Dead Code | **✅ 삭제** — CSV 다운로드는 `app.download` + `Session` |
| S-FH02 | print만 하는 save | **✅ 삭제** |

---

## 3. 안티패턴 ↔ 코드

| 안티패턴 | 코드 |
|----------|------|
| God Function | ~~`app.render_page`~~ → `html_renderer.HtmlRenderer` ✅ |
| Spaghetti Code | Session + ~~fil_data~~ + ~~global_sent/kw~~ (✅) |
| Shotgun Surgery | ~~S_KEYWORDS~~ + constants (감정 ✅, 카테고리 main SSOT) |
| Feature Envy | filters → CATEGORY_KEYWORDS 구조 |
| Lava Flow | ~~file_handler.py~~ **✅ 제거** |

---

## 4. 스멜 → PRD 버그 → Mom Test

| 스멜 | PRD | Mom Test |
|------|-----|----------|
| S-F01, S-F02, S-T04 | B-01 | H-02 ✅ Green |
| S-F03, S-T05 | B-02 | H-03, H-04 ✅ Green |
| S-A03 | B-03 | ✅ |
| S-A06 | B-04 | H-05 ✅ Green |
| S-A07 | B-05 | ✅ |
| S-L02 | B-06 | ✅ |

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

1. ~~`classify_sentiment()` 단일화~~ — **✅ Green**  
2. ~~`matches_category()` main 통일~~ — **✅ Green** ([ADR-001](ADR-001-category-main-only.md))  
3. ~~`fil_data` 제거~~ — **✅ Green**  
4. ~~`render_page` → HtmlRenderer~~ — **✅ 3-C-2**  
5. pytest + Mom Test §8 — **✅ Green** (39 passed, Golden Master)  
6. ~~`global_sent/kw`~~ — **✅ 3-C-1** · ~~`file_handler`~~ — **✅ 3-C-3** · ~~네이밍·contains_any·전략~~ — **✅ 3-C-5~7**  

---

## 7. 참고

- [MOM_TEST.md](MOM_TEST.md)
- [PRD.md](PRD.md) §4, §5
