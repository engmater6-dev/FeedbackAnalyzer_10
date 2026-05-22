# 테스트 계획서 — Feedback Analyzer

| 항목 | 내용 |
|------|------|
| 문서 ID | TP-01 |
| 버전 | **1.1** (Phase 3-A) |
| 작성 | 시니어 QA 리드 |
| 일자 | 2026-05-22 |
| 대상 브랜치 | **`green`** (Green 완료) · Phase 3 Refactor: `refactor` |
| TDD 단계 | Red ✅ → **Green ✅** → Refactor ⏳ |
| Green Gate (2026-05-22) | **39 passed** · line cov **97.42%** · Golden Master **pass** |
| 기술 스택 | Python 3.11+, pytest, pytest-cov, pydantic (선택·Phase 2+) |
| 근거 문서 | [PRD.md](PRD.md), [README.md](../README.md), [MOM_TEST.md](MOM_TEST.md), [CODE_SMELL.md](CODE_SMELL.md), [report/02.green.md](../report/02.green.md) |

---

## 1. 목적·범위

본 계획서는 **선정 샘플 예제**를 중심으로 Phase 1(Red) ~ Phase 2(Green) 테스트 범위·우선순위·커버리지·측정 전략을 정의한다.  
**v1.1:** Green Gate 달성 상태·명령·Mom Test §8 연동을 반영한다 (Phase 3-A).

| 구분 | 포함 | 제외 (별도 계획) |
|------|------|------------------|
| In-Scope | 감정·카테고리 분석, `filter_feedbacks`, 세션·모델, Flask 핵심 라우트 | Trend 시각화, File DB CRUD (Phase 5) |
| Out-of-Scope (초기) | E2E 브라우저, 부하·보안, ML/NLP | — |

**완료 정의 (DoD)**

- 샘플 예제 관련 단위·통합 테스트 **Green**
- Domain 모듈 커버리지 **≥ 95%**
- Boundary(앱·라우트) 커버리지 **≥ 85%**
- Mom Test §8 재검증 체크리스트 샘플 예제 항목 **Pass** (v1.1: 자동 4항목 완료, [MOM_TEST.md](MOM_TEST.md) §8)

**Green Gate 달성 (2026-05-22 · `green`)**

| 항목 | 결과 |
|------|------|
| 전체 테스트 | **39 passed** |
| 커버리지 (Gate) | **97.42%** (`--cov-fail-under=90`) |
| Domain Anchor 6 | Pass |
| Boundary IT | Pass (`test_routes_analyze_filter`, CSV 등) |
| Golden Master | `golden_master_expected.txt` + `test_golden_master` |

---

## 2. 선정 샘플 예제 (Anchor Test Case)

| 항목 | 내용 |
|------|------|
| **기능 이름** | PRD 대표 시나리오 — 텍스트 피드백 감정·카테고리 분석 및 복합 필터 |
| **README 요구사항** | **주요 기능 4번** — 피드백 필터링 (감정·카테고리 드롭다운) |
| **연관 요구사항** | 2번(키워드 분류), 3번(감정 분류), PRD F-04/F-05/F-06, B-01/B-02 |
| **입력** | 텍스트: `"배송이 너무 늦어요. 화가 납니다."` / 필터: 감정=`부정`, 키워드=`배송` |
| **기대 출력** | `sent` → 부정 1, 중립 0, 긍정 0 · `kw` → 배송 1 · `filter_feedbacks(..., "부정", "배송")` → **≥ 1건**, 분석·필터 건수 일치 |
| **Red 기준선 (참고)** | `sent` → 중립 1 · `filter` → **0건** (Mom Test §3.1) |
| **Green As-Is (현재)** | `sent` → 부정 1 · `filter(부정, 배송)` → **≥1건** — **Pass** |
| **스멜·버그 ID** | B-01, B-02 — **Resolved** (Green) |

### 선택 근거 (요약)

- PRD·Mom Test·CODE_SMELL가 **동일 입력·기대값**으로 정의한 유일한 대표 케이스이며, 감정·카테고리·필터 규칙 불일치를 한 번에 검증한다.
- Phase 2 Green 완료 여부를 판별하는 **단일 합격 기준(Gate)** 으로 사용한다.

---

## 3. pytest 단위 테스트 — 범위·우선순위

### 3.1 레이어 분류

| 레이어 | 모듈 | 역할 | 커버리지 목표 |
|--------|------|------|---------------|
| **Domain** | `text_analyzer`, `filters`, `constants`, `feedback`, `session` | 비즈니스 규칙·집계·필터 | **≥ 95%** |
| **Boundary** | `app` (라우트·CSV·렌더), `logger` | HTTP·I/O·프레젠테이션 경계 | **≥ 85%** |
| ~~**Dead**~~ | ~~`file_handler`~~ | **삭제됨** (3-C-3) — 다운로드는 `app`/`Session` | — |

### 3.2 우선순위 매트릭스

| 우선순위 | ID | 대상 | 테스트 초점 | 샘플 예제 연관 |
|----------|-----|------|-------------|----------------|
| **P0** | UT-01 | `TextAnalyzer.sent()` | Anchor 입력 → 부정 1건 | 직접 |
| **P0** | UT-02 | `TextAnalyzer.kw()` | Anchor 입력 → 배송 1건 | 직접 |
| **P0** | UT-03 | `filter_feedbacks()` | Anchor + `부정`/`배송` → ≥1건 | 직접 |
| **P0** | UT-04 | 분석·필터 일관성 | 동일 `Feedback` 리스트에 대해 `sent` 부정 수 = `filter(부정)` 건수 | 직접 |
| **P1** | UT-05 | `constants` | `SENTIMENT_KEYWORDS`에 중립·부정 키워드(`화가` 등) SSOT | Green 시 |
| **P1** | UT-06 | `filters` | `S_KEYWORDS` 미사용·`constants` 단일 소스 (Green 후) | B-01 |
| **P1** | UT-07 | 카테고리 `main` | `"배송"` only 본문 → `kw`·`filter(배송)` 일치 | B-02 |
| **P2** | UT-08 | `Feedback`, `Session` | 생성·누적·클래스 변수 상태 | 기반 |
| **P2** | UT-09 | `_contains_any` | 긍정/부정/중립 경계 substring | 유틸 |
| **P2** | UT-10 | 중립 3건 샘플 | `sent` 중립 수 = `filter(중립)` (Mom Test §8) | 회귀 |

### 3.3 P0 테스트 케이스 명세 (Anchor)

| TC ID | Given | When | Then |
|-------|-------|------|------|
| TP-ANCHOR-01 | `feedbacks = [Feedback("배송이 너무 늦어요. 화가 납니다.")]` | `TextAnalyzer().sent(feedbacks)` | `result["부정"] == 1`, `result["중립"] == 0`, `result["긍정"] == 0` |
| TP-ANCHOR-02 | 동일 Given | `TextAnalyzer().kw(feedbacks)` | `result["배송"] == 1` |
| TP-ANCHOR-03 | 동일 Given | `filter_feedbacks(feedbacks, "부정", "배송")` | `len(result) >= 1`, `result[0].text`에 배송·부정 키워드 매칭 |
| TP-ANCHOR-04 | 동일 Given | `sent` 후 `filter(부정, 전체)` | 부정 건수 == `filter` 반환 건수 |

**Red 단계:** TP-ANCHOR-01, 03은 **의도적 실패**로 커밋 (`red` 브랜치).  
**Green 단계:** Phase 2 완료 — TP-ANCHOR-01~04 **Pass** (2026-05-22, `green`).

### 3.4 pydantic 적용 (권장)

| 용도 | 모델 예시 | 비고 |
|------|-----------|------|
| 테스트 픽스처 | `FilterCriteria(sentiment: Literal["전체","긍정","중립","부정"], keyword: str)` | 잘못된 조합 조기 검증 |
| Phase 2+ API 경계 | `AnalyzeRequest`, `SentimentStats` | Flask form → 스키마 검증 |
| 단위 테스트 | `FeedbackInput(text: str)` with `min_length=1` | 빈 문자열 Boundary |

Domain 로직 자체는 pydantic **필수 아님**; Boundary·통합 테스트에서 입력 검증에 사용.

### 3.5 디렉터리·네이밍 (권장)

```
src/python/
├── tests/
│   ├── conftest.py              # Feedback 픽스처, Session reset
│   ├── domain/
│   │   ├── test_anchor_prd_example.py   # P0 Anchor
│   │   ├── test_text_analyzer.py
│   │   ├── test_filters.py
│   │   └── test_constants.py
│   └── boundary/
│       ├── test_routes_analyze_filter.py
│       └── test_csv_upload.py
└── pytest.ini
```

---

## 4. 통합·Boundary 테스트 범위

| 우선순위 | ID | 엔드포인트 | 검증 |
|----------|-----|------------|------|
| P1 | IT-01 | `POST /analyze` | Anchor 텍스트 POST → HTML/세션에 부정·배송 집계 반영 |
| P1 | IT-02 | `POST /filter` | `sentiment=부정`, `keyword=배송` → 결과 건수 ≥1 |
| P2 | IT-03 | `GET /download` | 필터 후 CSV non-empty (B-03) |
| P2 | IT-04 | `POST /upload` | `text` 헤더 CSV (B-04, Boundary) |

통합 테스트는 Flask `test_client` 사용. Domain P0 Green 이후 IT-01/02 착수 권장.

---

## 5. 커버리지 목표

### 5.1 목표치

| 구분 | 대상 패키지·파일 | 목표 | 실패 시 조치 |
|------|------------------|------|--------------|
| **Domain** | `text_analyzer`, `filters`, `constants`, `feedback`, `session` | **line ≥ 95%**, branch ≥ 90% | P0 테스트·누락 분기 추가 |
| **Boundary** | `app`, `logger` | **line ≥ 85%**, branch ≥ 80% | 라우트·에러 경로 IT 추가 |
| **전체 (Gate)** | Domain + Boundary 합산 | **line ≥ 90%** (PRD R-01) | README Phase 1 DoD |

~~`file_handler.py`~~: 삭제 완료 (3-C-3).

### 5.2 Domain vs Boundary 산정 규칙

- **Domain**: 순수 함수·클래스 메서드, Flask/request 미참조 코드 경로.
- **Boundary**: `@app.route`, `render_page`, multipart, `send_file`, stderr/print 로깅 경로.
- Anchor 예제는 **Domain P0 4건 Pass** = Domain Gate; **IT-02 Pass** = Boundary Gate.

### 5.3 제외·omit 목록

| 경로 | 사유 |
|------|------|
| `if __name__ == "__main__"` | 실행 진입점 |
| ~~`file_handler.py`~~ | 삭제됨 (3-C-3) |
| `.venv/**` | 서드파티 |
| `tests/**` | 자체 코드 |

---

## 6. 측정 전략 (pytest-cov)

### 6.1 의존성 설치

작업 디렉터리: `src/python`

```bash
pip install pytest pytest-cov pydantic
```

`requirements-dev.txt` 분리 권장 (운영 `requirements.txt`는 flask 유지).

### 6.2 pytest.ini (권장 설정)

```ini
[pytest]
testpaths = tests
pythonpath = .
addopts = -ra --strict-markers

markers =
    p0: anchor / release gate
    domain: domain layer only
    boundary: flask / io
    red: expected fail until phase 2
```

### 6.3 실행 명령 (프로젝트 실제 경로)

> 템플릿의 `unit_converter`는 본 프로젝트에 해당 없음. 아래는 Feedback Analyzer 기준.

**Domain only (95% Gate)**

```bash
cd src/python
pytest tests/domain/ \
  --cov=text_analyzer \
  --cov=filters \
  --cov=constants \
  --cov=feedback \
  --cov=session \
  --cov-report=term-missing \
  --cov-fail-under=95
```

**Boundary (85% Gate)**

```bash
pytest tests/boundary/ \
  --cov=app \
  --cov=logger \
  --cov-report=term-missing \
  --cov-fail-under=85
```

**전체 + PRD 90% Gate**

```bash
pytest tests/ \
  --cov=text_analyzer \
  --cov=filters \
  --cov=constants \
  --cov=feedback \
  --cov=session \
  --cov=app \
  --cov=logger \
  --cov-report=term-missing \
  --cov-report=html:../../report/coverage_html \
  --cov-fail-under=90
```

**Anchor만 (CI 스모크)**

```bash
pytest tests/domain/test_anchor_prd_example.py -m p0 -v
```

### 6.4 .coveragerc (omit·branch)

```ini
[run]
branch = True
source = text_analyzer, filters, constants, feedback, session, app, logger
omit =
    */tests/*

[report]
precision = 2
show_missing = True
skip_covered = False

[html]
directory = ../../report/coverage_html
```

### 6.5 측정 주기·게이트

| 시점 | 명령 | Gate |
|------|------|------|
| 매 커밋 (로컬) | Domain `pytest --cov` + Anchor P0 | TP-ANCHOR-* 의도 확인 |
| Phase 1 완료 | 전체 `--cov-fail-under=90` | README Phase 1 | ✅ **97.42%** |
| Phase 2 완료 | Anchor Green + Domain 95% | Mom Test §8 | ✅ §8 자동 4항목 |
| Phase 3 Refactor | 동일 Gate + Golden `--check` | [defect_list.md](defect_list.md) §6.3 | ⏳ |
| PR/merge | `term-missing` + html artifact | 누락 라인 리뷰 | — |

**Red 단계:** `--cov-fail-under` 비활성 또는 Anchor 실패만 허용.  
**Green 단계:** `--cov-fail-under=90` **활성** — 현재 **통과**.

### 6.6 term-missing 해석 가이드

| 누락 위치 | 조치 |
|-----------|------|
| `filters.py` L60-62 `main` continue | UT-07, TP-ANCHOR-03 |
| `text_analyzer` else → 중립 | UT-01, 키워드 보강 |
| `app.render_page` 분기 | IT-01/02 또는 Phase 3에서 템플릿 분리 후 재측정 |

---

## 7. TDD 단계별 실행 계획

| 단계 | 활동 | 산출 | Gate |
|------|------|------|------|
| **Red** | TP-ANCHOR-01~04 작성·실행 | 실패 로그·스냅샷 | 01·03 **Fail** 확인 | ✅ `red` |
| **Green** | B-01~B-06, `S_KEYWORDS` 제거, SSOT | **39 passed**, cov **97.42%** | Anchor **Pass** | ✅ `green` |
| **Refactor** | `_contains_any` 통합, 네이밍, `render_page` 분리 | cov ≥90% 유지 | 회귀 0 · GM `--check` | ⏳ `refactor` |

---

## 8. 리스크·가정

| 리스크 | 완화 |
|--------|------|
| `Session` 클래스 변수로 테스트 오염 | `conftest` autouse fixture로 매 테스트 reset |
| `filters` 내 `print` (S-F04) | stdout 캡처 또는 Green 시 제거 |
| God Function으로 Boundary 커버 85% 어려움 | 핵심 라우트 4개만 IT, 나머지 Phase 3 |
| substring 규칙 변경 시 Anchor 깨짐 | `constants` 단일 SSOT 테스트로 고정 |

**가정:** Python 3.11+, 테스트는 `src/python`을 cwd로 실행, 외부 API 없음.

---

## 9. 추적 매트릭스

| 테스트 ID | PRD | README | Mom Test | CODE_SMELL |
|-----------|-----|--------|----------|------------|
| TP-ANCHOR-01~04 | B-01, B-02, §2.3 | #3, #4 | §3.1, §8 | #1 |
| UT-10 | B-01 | #4 | §3.2 | #2 |
| IT-01~02 | F-02, F-06 | #4 | — | S-A02 |
| IT-04 | B-04 | #1 | H-05 | S-A06 |

---

## 10. 변경 이력

| 버전 | 일자 | 변경 |
|------|------|------|
| 1.0 | 2026-05-22 | 초안 — Anchor 샘플 예제 기반, Domain 95% / Boundary 85% |
| 1.1 | 2026-05-22 | Phase 3-A — 대상 브랜치 `green`, Gate 39 passed·cov 97.42%, §2 Green As-Is, §7 TDD Green ✅ |

---

## 11. 참고

- [MOM_TEST.md](MOM_TEST.md) §8 재검증 체크리스트  
- [CODE_SMELL.md](CODE_SMELL.md) §5 검증 시나리오  
- [PRD.md](PRD.md) §4 버그, §8 TDD 단계  
- [README.md](../README.md) Phase 1~2 To Do
