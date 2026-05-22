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
├── report/                    # 세션·커버리지 등 산출물
├── sample/                    # 샘플 CSV (test_feedback_trend.csv 등)
├── src/python/
│   ├── app.py                 # Flask, render_page (God Function)
│   ├── feedback.py            # Feedback 모델
│   ├── text_analyzer.py       # sent(), kw()
│   ├── filters.py             # filter_feedbacks(), S_KEYWORDS
│   ├── session.py             # Session.current_feedbacks
│   ├── logger.py              # print 기반 로깅
│   ├── constants.py           # 키워드·카테고리 상수
│   ├── file_handler.py        # 미사용 (Lava Flow)
│   ├── pytest.ini
│   ├── requirements.txt
│   ├── requirements-dev.txt   # pytest, pytest-cov, pydantic
│   └── tests/                 # Phase 1 (TDD Red 완료)
│       ├── conftest.py
│       ├── domain/
│       │   ├── test_anchor_prd_example.py
│       │   └── test_filters_regression.py
│       └── boundary/          # 스텁 (Green 이후)
├── project_purpose.md         # 8단계 미션
└── README.md
```

## 사용 방법

1. `http://localhost:8080` 접속
2. 피드백 텍스트 입력 또는 CSV 업로드
3. 감정/키워드 필터로 「분석」 실행
4. 필요 시 「결과 다운로드」(필터 성공 후)

## CSV 파일 형식

- 필수 컬럼: `text` (문서 기준)
- 현재 구현: 첫 행 스킵 + **0번 컬럼**만 읽음 → Phase 2에서 `text` 헤더 파싱 예정

---

## To Do List

[project_purpose.md](project_purpose.md) 8단계 미션 + [CODE_SMELL.md](doc/CODE_SMELL.md) 스멜 ID를 매핑한 체크리스트입니다. **TDD: Red → Green → Refactor** 순서를 권장합니다.

### 진행 현황 (2026-05-22 · 브랜치 `red`)

| Phase | 상태 | 비고 |
|-------|------|------|
| Phase 0 | **대부분 완료** | 문서·버그 증거·스멜 분석 완료 |
| Phase 1 | **Red 완료** / Green 대기 | Domain 6테스트 · **4 failed, 2 passed** |
| Phase 2~6 | 미착수 | 다음: B-01/B-02 Green |

**TDD Red Gate 확인** (`src/python`):

```bash
pytest tests/domain/test_anchor_prd_example.py tests/domain/test_filters_regression.py -v
# 기대: 4 failed, 2 passed (의도적 실패)
```

---

### Phase 0 — 준비·스멜 인지 (약 1시간)

- [x] [doc/PRD.md](doc/PRD.md), [doc/MOM_TEST.md](doc/MOM_TEST.md), [doc/CODE_SMELL.md](doc/CODE_SMELL.md), [doc/test_plan.md](doc/test_plan.md) 읽기
- [x] 가상환경·`pip install -r requirements.txt` · `pip install -r requirements-dev.txt`
- [ ] `python app.py` → `http://localhost:8080` 확인
- [x] **버그 재현** (Mom Test §3) — 문서·테스트로 고정
  - [x] `"배송이 너무 늦어요. 화가 납니다."` → 분석 중립 vs 기대 부정 (S-T04) · `test_anchor_prd_example.py`
  - [x] `filter(부정, 배송)` → 0건 (S-F02, S-F03) · 동일 파일
  - [x] 중립 샘플 3건 → `sent` 중립 수 ≠ `filter(중립)` 건수 (S-F01) · `test_filters_regression.py`
- [x] 스멜 체크: `app.render_page` God Function (S-A01), `filters.S_KEYWORDS` 중복 (S-F01) — [CODE_SMELL.md](doc/CODE_SMELL.md)

### Phase 1 — 테스트 기반 구축 (약 2시간)

**목표**: 커버리지 **90%+**, 스멜 S-T02·S-F01~F03을 테스트로 고정

- [x] `tests/` + `pytest`, `pytest-cov` 설치 (`requirements-dev.txt`, `pytest.ini`, `conftest.py`)
- [x] **Red** — 실패해야 하는 케이스 먼저 작성 (**TDD Red 단계 완료**)
  - [x] PRD 예시 문장 → `sent` 부정, `filter(부정,배송)` ≥1 (Mom Test §8) — 현재 **FAIL**
  - [x] 중립 3건 → 분석·필터 건수 일치 — 현재 **FAIL**
  - [x] 카테고리 `main` only (`"품질"`) → `kw` vs `filter(품질)` 일치 (B-02; `"배송"` only는 sub에 `배송` 포함으로 제외) — 현재 **FAIL**
- [ ] 단위 테스트 (Green 이후 확장)
  - [ ] `Feedback`, `Session` (S-FB01, S-S01) — 스텁 `skip`
  - [x] `TextAnalyzer.sent()`, `kw()` — Anchor·회귀 Red에 포함
  - [x] `filter_feedbacks()` — Anchor·회귀 Red에 포함
- [ ] 통합 테스트: `/analyze`, `/filter`, `/upload`, `/download` (S-A03) — `tests/boundary/` 스텁
- [ ] `pytest --cov` → **90% 이상**

### Phase 2 — 버그 수정·UX (약 1.5시간)

**목표**: PRD B-01~B-06, Mom Test 실무 Go 재검증

| PRD | 스멜 | 작업 |
|-----|------|------|
| B-01 | S-F01, S-F02, S-T04 | `S_KEYWORDS` 제거, `classify_sentiment()` 단일화 |
| B-02 | S-F03, S-T05 | 카테고리 `main`+sub 규칙을 `kw()`·filter에 동일 적용 |
| B-03 | S-A03 | `fil_data` 제거, 다운로드 대상을 세션/필터 결과로 통일 |
| B-04 | S-A06 | CSV `text` 컬럼 헤더 파싱 |
| B-05 | S-A07 | 업로드 후 분석 표시 또는 UX 안내 |
| B-06 | S-L02 | Logger 메시지를 페이지에 level별 표시 |

- [ ] 위 표 전항목 완료 후 Phase 1 테스트 **Green** 확인
- [ ] 멀티라인 입력 UX (textarea 높이·개행)
- [ ] `filters.py` L69-70 `print` 제거 (S-F04)

### Phase 3 — 코드 품질·스멜 제거 (약 2.5시간)

- [ ] 네이밍: `sent`→`analyze_sentiment`, `kw`→`analyze_keywords` (S-T01)
- [ ] 전역 제거: `fil_data`, `global_sent`, `global_kw` (S-A03, S-T02)
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

| 증상 | 스멜 ID | 파일 |
|------|---------|------|
| 중립 필터 개수 불일치 | S-F01, S-F02 | filters, text_analyzer |
| 배송+부정 0건 | S-F03, S-T04 | filters, constants |
| 다운로드 빈 파일 | S-A03 | app |
| CSV text 무시 | S-A06 | app |
| 로그 UI 없음 | S-L02 | logger, app |
| 죽은 코드 | S-FH01 | file_handler |

상세: [doc/CODE_SMELL.md](doc/CODE_SMELL.md) · PRD 버그: [doc/PRD.md](doc/PRD.md) §4
