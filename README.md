# Feedback Analyzer

![feedback_analyzer](./feedback_analyzer.png)

고객 피드백 분석 시스템은 자연어 기반 고객 피드백 데이터를 수집, 분류, 시각화하는 기능을 제공하는 Python(Flask) 기반 웹 애플리케이션입니다.

> **실습 프로젝트**: 의도적인 코드 스멜·안티패턴이 포함되어 있습니다.  
> - 제품 요구사항: [doc/PRD.md](doc/PRD.md)  
> - 학습 로드맵: [project_purpose.md](project_purpose.md)  
> - Mom Test: [doc/MOM_TEST.md](doc/MOM_TEST.md)  
> - 코드 스멜 분석: [doc/CODE_SMELL.md](doc/CODE_SMELL.md)  
> - 테스트 계획: [doc/test_plan.md](doc/test_plan.md)

> **현재 분석 방식**: 규칙 기반 키워드 substring 매칭 (ML/NLP 아님). “감정 분석·시각화·검색”은 [Mom Test](doc/MOM_TEST.md) 기준으로 실제 능력보다 넓게 표현되어 있을 수 있습니다.

## 주요 기능

- 텍스트 피드백 입력 (수동/CSV 업로드)
- 키워드 기반 피드백 분류 (규칙 기반)
- 감정 분류 (긍정/부정/중립, 키워드 매칭)
- 피드백 필터링 (감정·카테고리 드롭다운)
- 분석 결과 요약 (건수 통계)
- 결과 CSV 다운로드 (필터 성공 후)

## 요구사항

- Python 3.9 이상
- pip

## 설치 및 실행 방법 (가상환경)

### 1. 저장소 클론

```bash
git clone [repository-url]
cd FeedbackAnalyzer_10
```

### 2. 가상환경 생성

#### Windows

```bash
cd src/python
python -m venv .venv
```

#### macOS / Linux

```bash
cd src/python
python3 -m venv .venv
```

### 3. 가상환경 활성화

#### Windows (PowerShell)

```powershell
.venv\Scripts\Activate.ps1
```

#### Windows (CMD)

```cmd
.venv\Scripts\activate.bat
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

> 활성화되면 터미널 프롬프트 앞에 `(.venv)`가 표시됩니다.

### 4. 의존성 설치

```bash
pip install -r requirements.txt
```

테스트 도입 시 (Phase 1):

```bash
pip install -r requirements-dev.txt
```

### 5. 서버 실행

```bash
python app.py
```

서버가 시작되면 브라우저에서 `http://localhost:8080` 으로 접속합니다.

### 6. 가상환경 비활성화

```bash
deactivate
```

## 프로젝트 구조

```
FeedbackAnalyzer_10/
├── doc/
│   ├── PRD.md                 # 제품 요구사항 정의서
│   ├── MOM_TEST.md            # Mom Test 검증 보고서
│   ├── CODE_SMELL.md          # src 코드 스멜 분석
│   └── test_plan.md           # 테스트 계획서
├── report/                    # Red/Green 단계 산출물 (green_step0~5, 01.red 등)
├── sample/                    # 샘플 CSV (test_feedback_trend.csv 등)
├── src/python/
│   ├── app.py                 # Flask, render_page (God Function)
│   ├── feedback.py            # Feedback 모델
│   ├── text_analyzer.py       # classify_sentiment(), matches_category(), sent(), kw()
│   ├── filters.py             # filter_feedbacks() — constants·analyzer 규칙 공유
│   ├── session.py             # current_feedbacks, download_feedbacks (B-03)
│   ├── logger.py              # stdout + warning/error UI (B-06)
│   ├── constants.py           # SENTIMENT_KEYWORDS, CATEGORY_KEYWORDS (SSOT)
│   ├── file_handler.py        # 미사용 (Lava Flow)
│   ├── pytest.ini
│   ├── requirements.txt
│   ├── requirements-dev.txt   # pytest, pytest-cov, pydantic
│   └── tests/
│       ├── conftest.py
│       ├── domain/              # Anchor 6 tests — Green Gate 통과
│       │   ├── test_anchor_prd_example.py
│       │   └── test_filters_regression.py
│       └── boundary/            # IT-01~04 (Flask test_client)
├── project_purpose.md         # 8단계 미션
└── README.md
```

## 사용 방법

1. `http://localhost:8080` 접속
2. 피드백 텍스트 입력 또는 CSV 업로드
3. 감정/키워드 필터로 「분석」 실행
4. 필요 시 「결과 다운로드」— 마지막 입력·필터 결과 (`Session.download_feedbacks`)

## CSV 파일 형식

- 권장: 첫 행 헤더에 **`text`** 컬럼
- 구현 (B-04): 헤더에 `text`가 있으면 해당 컬럼 사용, 없으면 **0번 컬럼** 전 행 파싱
- 업로드 직후 감정·키워드 집계 표시 (B-05)

---

## To Do List

[project_purpose.md](project_purpose.md) 8단계 미션 + [CODE_SMELL.md](doc/CODE_SMELL.md) 스멜 ID를 매핑한 체크리스트입니다. **TDD: Red → Green → Refactor** 순서를 권장합니다.

### 진행 현황 (2026-05-22 · 브랜치 `green`)

| Phase | 상태 | 비고 |
|-------|------|------|
| Phase 0 | **대부분 완료** | 문서·스멜 분석 완료 · `python app.py` 수동 확인 `[ ]` |
| Phase 1 | **완료** | Domain 6 + IT 8 · **38 passed** · cov **97%** (`--cov-fail-under=90`) |
| Phase 2 | **B-01~B-06 완료** | Step 0~5 커밋 완료 · [report/](report/) 참고 |
| Phase 3~6 | **미착수** | Refactor·구조·Trend·DB·리뷰 |

**테스트 실행** (`src/python`):

```bash
# Domain Gate (스모크)
pytest tests/domain/test_anchor_prd_example.py tests/domain/test_filters_regression.py -v

# Phase 1 DoD (전체 + 커버리지 90%)
pytest tests/ --cov --cov-fail-under=90 -q
```

**Green 단계 커밋 이력 (`green` 브랜치):** Step 0~5 커밋 + Step 6 (테스트·UX)

---

## GREEN 단계 To-Do 리스트

[test_plan.md](doc/test_plan.md) Anchor Gate + README Phase 2 기준. 상세 로그: [report/green_step0_baseline.md](report/green_step0_baseline.md) ~ [report/green_step5_b03_b06.md](report/green_step5_b03_b06.md).

| Step | 작업 | PRD/스멜 | 상태 |
|------|------|----------|------|
| 0 | Red 기준선 재확인 (6 tests, 4 fail) | — | [x] |
| 1 | `S_KEYWORDS` 제거, `classify_sentiment()` SSOT | B-01 | [x] |
| 2 | `matches_category()` — `main` 규칙 `kw`·filter 통일 | B-02 | [x] |
| 3 | Domain Green Gate (6 passed) | — | [x] |
| 4 | `filters` print 제거, 멀티라인 textarea·줄 단위 입력 | S-F04, UX | [x] |
| 5 | `fil_data`→Session, CSV `text`, 업로드 분석, 로그 UI | B-03~B-06 | [x] |
| 6 | cov **90%+**, boundary IT (`/analyze` 등) | Phase 1 | [x] |

**Green 합격 조건 (Domain 최소)** — [x] PRD 예시 부정·배송 필터 · [x] 중립 3건 일치 · [x] `"품질"` main only 일치

---

### Phase 0 — 준비·스멜 인지 (약 1시간)

- [x] [doc/PRD.md](doc/PRD.md), [doc/MOM_TEST.md](doc/MOM_TEST.md), [doc/CODE_SMELL.md](doc/CODE_SMELL.md), [doc/test_plan.md](doc/test_plan.md) 읽기
- [x] 가상환경·`pip install -r requirements.txt` · `pip install -r requirements-dev.txt`
- [ ] `python app.py` → `http://localhost:8080` 확인
- [x] **버그 재현** (Mom Test §3) — Red 테스트로 고정 → **Green에서 수정 완료**
  - [x] PRD 예시 → `sent` 부정, `filter(부정,배송)` ≥1 (B-01, B-02)
  - [x] 중립 3건 → 분석·필터 건수 일치 (B-01)
  - [x] `"품질"` only → `kw` vs `filter(품질)` 일치 (B-02)
- [x] 스멜 체크: [CODE_SMELL.md](doc/CODE_SMELL.md) — `S_KEYWORDS`·`fil_data` 등 Green에서 일부 해소, God Function 등 Phase 3 잔여

### Phase 1 — 테스트 기반 구축 (약 2시간)

**목표**: 커버리지 **90%+**, 스멜 S-T02·S-F01~F03을 테스트로 고정

- [x] `tests/` + `pytest`, `pytest-cov` 설치 (`requirements-dev.txt`, `pytest.ini`, `conftest.py`)
- [x] **Red** — 실패 테스트 작성 (**TDD Red 단계 완료**, 브랜치 `red`)
- [x] **Green (Domain)** — Anchor·회귀 6건 **PASS** (브랜치 `green`)
  - [x] PRD 예시 · 중립 3건 · 카테고리 `main` only (Mom Test §8)
- [x] 단위 테스트 확장 — `test_session`, `test_logger`, `test_feedback`, `test_csv_parse` 등
- [x] 통합 테스트 — `tests/boundary/test_routes_analyze_filter.py` (IT-01~04)
- [x] `pytest tests/ --cov --cov-fail-under=90` → **97%+** ([report/green_step6_tests.md](report/green_step6_tests.md))

### Phase 2 — 버그 수정·UX (약 1.5시간)

**목표**: PRD B-01~B-06, Mom Test 실무 Go 재검증

| PRD | 스멜 | 작업 | 상태 |
|-----|------|------|------|
| B-01 | S-F01, S-F02, S-T04 | `S_KEYWORDS` 제거, `classify_sentiment()` 단일화 | [x] |
| B-02 | S-F03, S-T05 | `matches_category()` — `kw()`·filter `main` 통일 | [x] |
| B-03 | S-A03 | `fil_data` 제거 → `Session.download_feedbacks` | [x] |
| B-04 | S-A06 | CSV `text` 컬럼 헤더 파싱 | [x] |
| B-05 | S-A07 | 업로드 후 분석·안내 문구 | [x] |
| B-06 | S-L02 | warning/error 페이지 표시 (`Logger.show_*_on_page`) | [x] |

- [x] Domain 테스트 **Green** 확인 (6 passed)
- [x] 멀티라인 입력 UX (textarea `rows=6`, 줄 단위 `/analyze`)
- [x] `filters.py` 디버그 `print` 제거 (S-F04)

### Phase 3 — 코드 품질·스멜 제거 (약 2.5시간)

- [ ] 네이밍: `sent`→`analyze_sentiment`, `kw`→`analyze_keywords` (S-T01)
- [x] `fil_data` 제거 (B-03) / [ ] `global_sent`, `global_kw` (S-T02)
- [ ] `_contains_any()` 공통 유틸 1곳 (S-T03)
- [ ] `render_page()` 분리 → 템플릿/`HtmlRenderer` (S-A01, S-A02)
- [ ] `file_handler.py` 삭제 또는 `download` 연동 (S-FH01)
- [ ] 리팩토링 1건 추가 (전략 패턴·Extract Class 등)
- [ ] README 주요 기능 문구와 실제 동작 일치 (Mom Test §6.1)

### Phase 4 — 구조·모델 (선택)

- [ ] `handlers/`, `services/`, `models/` 분리 (PRD R-07)
- [ ] `services/sentiment.py`, `services/category.py` 추출
- [ ] `Feedback`에 sentiment, category, setter (S-FB01, S-FB02)
- [ ] `Session` 인스턴스 기반 상태 (S-S01, S-S02)

### Phase 5 — 확장 (약 3시간)

- [ ] `sample/test_feedback_trend.csv` 추가
- [ ] Trend 시각화 (Mom Test 인터뷰 후 Go/No-Go)
- [ ] 감정 키워드 File DB (SQLite) — `constants` 대체 (S-C01, S-C02)
- [ ] DB ↔ analyzer ↔ filter 연동

### Phase 6 — 리뷰·발표 (약 2시간)

- [ ] `report/`에 팀 리뷰·장단점 (스멜 개선 전/후)
- [ ] Mom Test §8 재검증 체크리스트 완료
- [ ] 발표 준비

---

### 스멜·버그 빠른 참조

| 증상 | 스멜 ID | Green | 파일 |
|------|---------|-------|------|
| 중립 필터 개수 불일치 | S-F01, S-F02 | ✅ B-01 | filters, text_analyzer |
| 배송+부정 0건 | S-F03, S-T04 | ✅ B-01, B-02 | filters, constants |
| 다운로드 빈/불일치 | S-A03 | ✅ B-03 | app, session |
| CSV text 무시 | S-A06 | ✅ B-04 | app |
| 로그 UI 없음 | S-L02 | ✅ B-06 | logger, app |
| God Function / 죽은 코드 | S-A01, S-FH01 | ⏳ Phase 3 | app, file_handler |

상세: [doc/CODE_SMELL.md](doc/CODE_SMELL.md) · PRD 버그: [doc/PRD.md](doc/PRD.md) §4
