# Mom Test 보고서 — Feedback Analyzer

| 항목 | 내용 |
|------|------|
| 문서 버전 | 1.1 (Phase 3-A 초안) |
| 일자 | 2026-05-22 |
| 방법 | Rob Fitzpatrick *The Mom Test* 원칙 + 실제 코드·pytest 검증 |
| 대상 | 제품 가설(README/PRD) vs 구현 (`green` / `refactor`) |
| 브랜치 | `green` (Green 완료) · Phase 3 문서 작업: `refactor` |
| 자동 검증 | **39 passed** · cov **97.42%** · Golden Master pass ([test_plan.md](test_plan.md), [report/02.green.md](../report/02.green.md)) |

---

## 1. Mom Test란 (본 프로젝트 적용 방식)

**잘못된 질문**: “이 피드백 분석기 쓰실 거예요?” “Trend 기능 필요하세요?”  
**올바른 질문**: “지난달 고객 VOC는 어디에 모으셨나요?” “불만 급증을 어떻게 알았나요?” “그때 뭘 손으로 하셨나요?”

본 문서는 **실제 사용자 인터뷰 대신**, 문서·코드에 박힌 **가설을 Mom Test 규칙으로 검증**하고, 런타임으로 **거짓 긍정(말만 되는 기능)** 을 찾았다.

---

## 2. 검증한 핵심 가설

| ID | 가설 (문서/기능 설명) | Red (`spec`/`red`) | Green 재판정 (2026-05-22) |
|----|----------------------|--------------------|---------------------------|
| H-01 | “고객 피드백을 감정·카테고리로 분류한다” | ⚠️ 규칙 불일치 | ⚠️ **부분 검증** — SSOT 통일·Anchor Pass. ML 아님·키워드 한계는 잔존 |
| H-02 | “중립 필터로 중립 피드백만 볼 수 있다” | ❌ 기각 | ✅ **검증** — `classify_sentiment()` 단일화, Domain 회귀 Pass |
| H-03 | “배송 관련 피드백을 필터한다” | ⚠️ PRD 예시 실패 | ✅ **검증** (Anchor·`품질` main) — **main-only** 설계, sub-only 본문은 정책 이슈(DEF-016) |
| H-04 | “부정+배송 조합으로 문제 VOC를 찾는다” | ❌ 기각 | ✅ **검증** — PRD 예시 `filter(부정, 배송)` ≥1건 (B-01, B-02) |
| H-05 | “CSV `text` 컬럼으로 업로드한다” | ❌ 0열만 | ✅ **검증** — `_parse_csv_to_feedbacks`, IT Pass (B-04) |
| H-06 | “실습용 리팩토링 챌린지” | ✅ 검증 | ✅ **유지** — Phase 3 스멸 잔여가 커리큘럼과 일치 |

---

## 3. 런타임 검증 결과 (증거)

> **§3.1~3.3** — TDD **Red** 기준선(2026-05-22 초기). **Green 재검증**은 §3.4·§8·pytest Gate.

### 3.1 PRD 시나리오 예시 (가장 중요) — Red 기준선

**입력**: `"배송이 너무 늦어요. 화가 납니다."`  
**문서 기대**: 감정=부정, 카테고리=배송

| 검사 | 실제 결과 |
|------|-----------|
| `TextAnalyzer.sent()` | `긍정:0, 중립:1, 부정:0` ← **부정 아님** |
| `TextAnalyzer.kw()` | `배송:1` ← 카테고리는 맞음 |
| `filter_feedbacks(..., '부정', '배송')` | **0건** |

**원인 (Mom Test 관점의 “진짜 문제”)**  
- 사용자는 “화가 난다”고 말하지만, 시스템은 사전에 `화남`만 등록 → **실제 불만 언어와 키워드 사전 괴리**.  
- 필터는 별도 `S_KEYWORDS` 사용 → 분석·필터가 같은 문장을 다르게 해석.

→ **“감정 분석 기능이 있다”는 말은 맞지만, 의사결정에 쓸 수준은 아니다.**

### 3.2 중립 필터 (미션 3 버그) — Red 기준선

**입력 3건**: 보통/괜찮/특별한 불만 없음 등

| 검사 | 실제 결과 |
|------|-----------|
| `sent()` | 중립 2, 부정 1 |
| `filter(..., '중립')` | **1건만** 통과 |

→ 사용자 인터뷰에서 나올 말: *“중립만 보려는데 왜 개수가 달라요?”* — **기능 신뢰 붕괴**.

### 3.3 배송 카테고리 — Red 기준선

**입력**: `배송이 너무 늦어요`, `택배가 빨라요 좋아요`

| 검사 | 실제 결과 |
|------|-----------|
| `kw()` | 배송 2 |
| `filter(..., '배송')` | 2건 |

→ 이 샘플에서는 통과. 다만 `filter`가 `main` 키워드를 스킵하므로 **“배송”만 포함된 짧은 문장**은 놓칠 수 있음 (구조적 리스크).

### 3.4 Green 재검증 (2026-05-22 · `green` 브랜치)

**근거:** Domain Anchor 6건 · boundary IT · `pytest tests/ --cov-fail-under=90` · Golden Master `golden_master_expected.txt`

| 검사 | Green 결과 | 테스트·PRD |
|------|------------|------------|
| PRD 예시 `sent` | 부정 1, 중립 0, 긍정 0 | TP-ANCHOR-01, B-01 |
| PRD 예시 `filter(부정, 배송)` | ≥1건 | TP-ANCHOR-03, B-01/B-02 |
| 중립 3건 | `sent` 중립 수 = `filter(중립)` | UT-10, `test_filters_regression` |
| `"품질"` only | `kw` = `filter(품질)` | B-02, `matches_category()` |
| CSV `text` 헤더 | 업로드·집계 IT Pass | B-04, IT-04 |
| 전체 회귀 | **39 passed**, cov **97.42%** | [report/02.green.md](../report/02.green.md) |

**Mom Test 해석:** 문서·PRD에 적힌 **대표 시나리오**는 자동 검증으로 **신뢰 회복**. 다만 §4.1의 “시각화·검색·ML 감정분석” 과장, Phase 3 구조 부채(God Function 등)는 **실무 Go**를 막는 요인으로 남음 → §7 **Partial Go**.

---

## 4. Mom Test 규칙별 진단

### 4.1 “아이디어에 대해 말하게 하지 말라”

| 문서 표현 | 문제 |
|-----------|------|
| “분석 결과 시각화” | 실제는 숫자 박스 2개 — **차트·테이블·그래프 없음** (PRD의 “그래프”는 미구현) |
| “검색 기능” | 키워드 드롭다운 필터만 — **자유 검색 없음** |
| “감정 분석” | ML/NLP가 아닌 substring 매칭 — **학습자·강사에게는 OK, 고객에게는 과장** |

### 4.2 “과거 행동·구체적 사실을 물어라” (가상 인터뷰 스크립트)

**CS/운영 담당자에게 물어볼 질문 예시**

1. 지난 분기 VOC는 Excel·Zendesk·설문 중 어디에 있었나요?  
2. “배송 불만”을 찾을 때 지금은 Ctrl+F인가요, 태그인가요?  
3. 감정 라벨은 누가, 얼마나 자주 붙이나요? 자동 분류 결과를 **그대로 보고서에 쓰나요**?  
4. 키워드 목록을 바꿀 때 배포 없이 바꿀 수 있어야 하나요? → **R-10 File DB 가설의 근거**

**기대 답이 나오면 제품이 살아남는 조건**  
- 반복 수작업(엑셀 피벗, 눈으로 분류)에 **시간·비용**이 이미 든다.  
- 자동 분류 정확도보다 **“빠른 1차 스크리닝”** 이 목표다.

### 4.3 “칭찬·가능성은 증거가 아니다”

| “좋아 보이는” 요소 | 실제 증거 |
|-------------------|-----------|
| Trend 시각화 (Phase 5) | ✅ `sample/test_feedback_trend.csv` · 월별 막대 UI — **1차 스크리닝 보조** 수준 |
| 90% 테스트 커버리지 | **학습 성공 지표**이지 고객 가치 지표는 아님 |
| File DB 키워드 CRUD | ✅ SQLite·CRUD 구현 — 운영 거버넌스·인터뷰 검증은 Phase 6 선택 |

### 4.4 “돈·시간·평판이 걸린 문제인가?”

| 페르소나 | Mom Test 결론 |
|----------|----------------|
| **학습자** | ✅ 시간 투자 가치 있음 (리팩토링·TDD) |
| **실무 CS 리더** | ⚠️ **Partial** — Anchor·IT 통과, 1차 스크리닝 가능. 추이·고급 시각화·인터뷰 검증 전까지 보고서 완전 대체는 어려움 |
| **경영진** | ❌ “대시보드”만으로는 의사결정 근거 부족 (추이·신뢰도·샘플링 필요) |

---

## 5. 잘못된 질문 vs Mom Test 질문 (실습팀용)

| 피하기 (Bad) | 대신하기 (Good) |
|--------------|-----------------|
| 이 기능 좋을 것 같나요? | 지난주 배송 불만 몇 건이었고, 어떻게 집계했나요? |
| 중립 필터 필요해요? | “애매한 리뷰”는 보통 어떻게 처리하나요? 버리나요, 별도 탭? |
| Trend 차트 넣을까요? | 월별 VOC 보고서 만드는 데 몇 시간 걸리나요? |
| SQLite로 키워드 관리할까요? | 키워드 바꿀 때 마지막으로 누가, 언제, 왜 바꿨나요? |

---

## 6. 제품·문서 권고 (Mom Test 후속)

### 6.1 즉시 (신뢰 회복 — Phase 2)

1. PRD 예시 문장이 **실행 시 부정+배송 1건** 나오도록 키워드·필터 통일 (B-01, B-02).  
2. README “주요 기능”에 **규칙 기반·키워드 매칭** 한 줄 명시 (과장 방지).  
3. “시각화” → 현재는 **“건수 요약”** 으로 표현 완화 또는 간단 차트 추가.

### 6.2 인터뷰 3명 이상 후 결정 (Phase 5)

- Trend: “시간 축”이 보고서에 필수인지 확인 후 구현.  
- File DB: 키워드를 **누가·얼마나 자주** 바꾸는지 확인 — 없으면 `constants.py` 단일화만으로 충분할 수 있음.

### 6.3 유지 (교육 목적)

- 의도적 스멸·8단계 미션은 Mom Test에서 **별도 세그먼트(학습자)** 로 ✅ 유지.  
- “운영 제품”과 “실습 베이스”를 README 첫머리에 **이중 포지셔닝** 유지하는 것이 적절함.

---

## 7. Mom Test 최종 판정

### 7.1 Red 시점 (2026-05-22 초기 · `spec`/`red`)

| 관점 | 판정 | 한 줄 요약 |
|------|------|------------|
| **교육 제품** | ✅ Pass | 버그·스멸이 커리큘럼과 일치 |
| **VOC 분석 도구 (실무)** | ❌ Fail | PRD 대표 시나리오 미동작 |
| **문서 정직성** | ⚠️ Partial | 기능명이 실제 능력보다 큼 |

**Go / No-Go (Red):** 실무 **No-Go** · 학습 **Go**.

### 7.2 Green 재판정 (Phase 3-A · 2026-05-22 · `green`)

| 관점 | 판정 | 한 줄 요약 |
|------|------|------------|
| **교육 제품** | ✅ Pass | Green·테스트·Golden Master 완료, Phase 3 Refactor 잔여 |
| **VOC 분석 도구 (실무)** | ⚠️ **Partial Go** | Domain·IT·PRD Anchor **Pass** — **1차 VOC 스크리닝** 수준. Trend·DB·인터뷰·구조 개선 전 **완전 대체 불가** |
| **문서 정직성** | ⚠️ Partial | README “건수 통계·규칙 기반” 완화(2026-05-22). 차트·자유 검색 표현은 Phase 5/6에서 정리 |

**Partial Go 근거 (자동 검증)**

1. **Domain Gate** — Mom Test §8 항목 1~3 + CSV: pytest Domain·Anchor **6 passed**.  
2. **Boundary Gate** — `/analyze`, `/filter`, `/upload`, `/download` IT Pass (B-03~B-06).  
3. **회귀** — 전체 **39 passed**, cov **97.42%**, Golden Master `--check` OK.  
4. **잔여 리스크** — 규칙 기반 substring 한계, main-only 카테고리(DEF-016), God Function·전역 상태(Phase 3), 실사용자 인터뷰 미수행.

**Go / No-Go (Green 후)**

| 대상 | 판정 |
|------|------|
| **학습 (Phase 3 Refactor)** | ✅ **Go** — 즉시 `refactor` 브랜치 착수 |
| **실무 1차 스크리닝 (파일럿)** | ⚠️ **Partial Go** — Anchor·필터·CSV 경로 신뢰. 보고서·경영 의사결정용은 Phase 5~6·인터뷰 후 |
| **실무 정식 배포** | **No-Go** — Phase 3~6 Gate·인터뷰(선택) 미충족 |

---

## 8. 재검증 체크리스트 (Green 후 · Phase 3-A)

**자동 검증 (pytest · 2026-05-22 `green`)**

- [x] PRD 예시 문장: `sent` → 부정, `filter(부정, 배송)` → ≥1건 — `test_anchor_prd_example`, TP-ANCHOR-01/03  
- [x] 중립 3건 샘플: `sent` 중립 수 = `filter(중립)` 건수 — `test_filters_regression`  
- [x] `"품질"` only 본문: `kw`와 `filter(품질)` 일치 (main-only) — Domain 회귀  
- [x] CSV `text` 헤더 파일 업로드 후 건수·집계 — `test_csv_parse`, boundary IT  
- [x] Golden Master 스냅샷 — `test_golden_master`, `generate_golden_master.py --check`

**수동·선택 (Phase 0 / Phase 6)**

- [ ] 브라우저 수동 E2E — `report/manual_e2e_phase0.md` (Phase 0 Gate)  
- [ ] 실 사용자 3인 인터뷰 노트 `report/` (선택 · Trend/DB Go/No-Go)

**명령 (유지보수)**

```bash
cd src/python
pytest tests/domain/test_anchor_prd_example.py tests/domain/test_filters_regression.py -v
pytest tests/ --cov --cov-fail-under=90 -q
python scripts/generate_golden_master.py --check
```

---

## 9. 참고

- [PRD.md](PRD.md) §4 버그 목록  
- [README.md](../README.md) To Do List Phase 0~6  
- [test_plan.md](test_plan.md) v1.1 — Green Gate  
- [defect_list.md](defect_list.md) DEF-020  
- [report/02.green.md](../report/02.green.md)  
- Rob Fitzpatrick, *The Mom Test* (2013)

---

## 10. 변경 이력

| 버전 | 일자 | 변경 |
|------|------|------|
| 1.0 | 2026-05-22 | 초안 — Red 기준선, VOC Fail |
| 1.1 | 2026-05-22 | Phase 3-A — §3.4 Green 재검증, §7 Partial Go, §8 자동 4항목 `[x]` |
