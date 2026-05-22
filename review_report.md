# 코드 리뷰 및 개선 보고서

| 항목 | 내용 |
|------|------|
| 문서 ID | REVIEW-01 |
| 작성일 | 2026-05-22 |
| 분석 도구 | Cursor AI (`doc/`, `README.md`, `src/` 통합 분석) |
| Before | 브랜치 `red` |
| After | 브랜치 `new_feature` |
| 상세 근거 | [report/refactoring_before_after.md](report/refactoring_before_after.md), [doc/defect_list.md](doc/defect_list.md), [doc/CODE_SMELL.md](doc/CODE_SMELL.md) |

---

## 1. 분석 배경 (프로젝트·목적)

### 1.1 프로젝트 개요

**Feedback Analyzer**는 Flask 기반 고객 피드백 분석 웹 애플리케이션이다. 텍스트·CSV 입력을 받아 규칙 기반 키워드 매칭으로 감정(긍정/부정/중립)·카테고리를 분류하고, 건수 통계·필터·CSV 다운로드를 제공한다. Phase 5 이후 `date,text` CSV 업로드 시 월별 추이(Trend)와 SQLite 감정 키워드 CRUD가 추가되었다.

### 1.2 분석 목적

- 의도적으로 포함된 **코드 스멜·안티패턴**과 PRD 버그(B-01~B-06) 식별
- TDD(Red → Green → Refactor) 및 Phase 4~5 구조·기능 확장 결과 검증
- QA 결함 23건(DEF-001~023) 대비 **수정·잔여** 정리
- Phase 6(문서·발표) 전 **전후 비교·효과** 문서화

### 1.3 분석 범위

| 범위 | 경로 |
|------|------|
| 요구사항·정책 | `doc/PRD.md`, `doc/CSV_FORMAT.md`, `doc/ADR-001-category-main-only.md` |
| 스멜·결함 | `doc/CODE_SMELL.md`, `doc/defect_list.md` |
| 제품 검증 | `doc/MOM_TEST.md`, `doc/test_plan.md` |
| 소스 | `src/python/` (app, handlers, services, models, tests) |
| 진행 현황 | `README.md`, `report/02.green.md` ~ `report/05.new_feature.md` |

---

## 2. Cursor AI 분석 요약 (항목별 표)

### 2.1 Phase·마일스톤

| Phase | Cursor AI 판정 | 핵심 산출 |
|-------|------------------|-----------|
| Phase 0 | 대부분 완료 | 문서·Red 재현 ✅ · 수동 E2E 미완 |
| Phase 1~2 (Green) | 완료 | B-01~B-06, Domain 6 pass, 39 tests |
| Phase 3 (Refactor) | 완료 | 3-C-1~7, 50 passed, cov 97.78% |
| Phase 4 (구조) | 완료 | handlers/services/models, 55 passed |
| Phase 5 (확장) | 완료 | Trend·SQLite, **79 passed**, cov **94.15%** |
| Phase 6 | 미착수 | DEF-020~022, 팀 리뷰, 발표 |

### 2.2 품질 지표

| 지표 | Before (`red`) | After (`new_feature`) |
|------|----------------|------------------------|
| `app.py` 규모 | ~240줄 (God Module) | ~18줄 (부트스트랩) |
| Python 모듈 | 8 (+ Lava Flow) | 30+ (레이어 분리) |
| Domain 테스트 | 4 fail / 2 pass | 전항목 pass |
| pytest 전체 | 6 (+ skip) | **79 passed** |
| 커버리지 | ~39% | **94.15%** |
| Golden Master | 없음 | pass (`--check`) |
| QA 결함 | 기능·구조 다수 | 완료 21 · 부분 3 · 미완료 0 |

### 2.3 스멜·버그 핵심 원인

| 구분 | Cursor AI 진단 | 조치 Phase |
|------|----------------|------------|
| 감정 규칙 이중화 | `constants` / `filters.S_KEYWORDS` / analyzer 불일치 (S-F01, S-F02) | Green |
| 카테고리 불일치 | filter가 `main` skip (S-F03, B-02) | Green |
| 전역 상태 | `fil_data`, `global_sent`, `global_kw` (S-A03, S-T02) | Green·Refactor |
| God Function | `render_page()` in `app.py` (S-A01) | Refactor |
| Lava Flow | `file_handler.py` 미사용 (S-FH01) | Refactor |
| 레이어 혼재 | 단일 `app.py`에 HTTP·UI·도메인 | Phase 4 |
| 감정 하드코딩 | constants만 (S-C01, S-C02) | Phase 5 (SQLite) |

### 2.4 Mom Test·실무 판정

| 관점 | 판정 | 비고 |
|------|------|------|
| 교육 제품 (TDD·리팩토링) | Pass | Red→Green→Refactor·Gate 통과 |
| VOC 1차 스크리닝 | Partial Go | Anchor·IT Pass, substring 한계 잔존 |
| 실무 정식 배포 | No-Go | Phase 6·인터뷰·문서 종결 전 |
| 문서 정직성 | Partial | DEF-020~022 Phase 6 종결 예정 |

---

## 3. 개선/처리 내역

| 피드백사항 | 수정 조치 | 결과 |
|------------|-----------|------|
| PRD 예시 문장 부정 미분류 (`화가`·규칙 이중화) — DEF-001, B-01 | `classify_sentiment()` SSOT, `S_KEYWORDS` 제거, 부정 키워드 보강 | Anchor `sent` 부정 1건 ✅ |
| 필터(부정+배송) 0건 — DEF-002 | 필터가 `classify_sentiment()` 공유 | filter ≥1건 ✅ |
| 중립 3건 sent vs filter 건수 불일치 — DEF-003 | 감정 단일 규칙 | 건수 일치 ✅ |
| `kw(품질)` vs `filter(품질)` 불일치 — DEF-004, B-02 | `matches_category()` main-only ([ADR-001](doc/ADR-001-category-main-only.md)) | 집계·필터 일치 ✅ |
| 다운로드 빈/구버전 (`fil_data`) — DEF-005, B-03 | `Session.set/get_download_feedbacks`, `text` 헤더 CSV | 다운로드 정합 ✅ |
| CSV `text` 헤더 무시 — DEF-006, B-04 | `services/csv_parser.parse_csv_to_feedbacks` | 헤더·Trend 모드 ✅ |
| 업로드 후 집계 없음 — DEF-007, B-05 | upload 후 분석·안내 문구 | UX 개선 ✅ |
| 로그 UI 없음 — DEF-008, B-06 | `POST /settings/logs`, level별 토글 | warning/error/info ✅ |
| `filter_feedbacks` debug print — DEF-009 | print 제거 | stdout 정리 ✅ |
| 커버리지 ~39% — DEF-010 | boundary IT·unit 확장 | cov **94.15%** ✅ |
| boundary IT 미착수 — DEF-011~012 | IT-01~04, CSV upload IT | HTTP 경로 검증 ✅ |
| 연속 요청 로그 누적 — DEF-013 | `_begin_page_request()` | 요청별 로그 ✅ |
| 빈 download — DEF-014 | warning + 버튼 조건 | 빈 CSV 방지 ✅ |
| CSV 레거시 0열 규칙 — DEF-015 | [CSV_FORMAT.md](doc/CSV_FORMAT.md) | 문서화 ✅ |
| sub-only 본문 0건 — DEF-016 | ADR-001 main-only Won't fix v1 | 정책 확정 ✅ |
| God Function `render_page` — DEF-017 | `html_renderer.HtmlRenderer` | `app.py` 축소 ✅ |
| `global_sent`/`global_kw` — DEF-018 | 클래스 변수 제거, `analyze_sentiments`/`keywords` | 부작용 제거 ✅ |
| `file_handler.py` Lava Flow — DEF-019 | 파일 삭제, Session/download 연동 | dead code 제거 ✅ |
| Golden Master 없음 — DEF-023 | `golden_master_expected.txt`, `--check` | 회귀 고정 ✅ |
| 단일 app God Module — R-07 | `handlers/`, `services/`, `models/` Blueprint 분리 | 관심사 분리 ✅ |
| Anemic `Feedback` — R-08 | sentiment/category/recorded_at, setter | 도메인 강화 ✅ |
| Trend 미지원 — R-09 | `trend_service`, `date,text` CSV, UI 막대 | 월별 추이 ✅ |
| 감정 키워드 하드코딩 — R-10 | SQLite `keyword_db`, CRUD UI | 런타임 SSOT ✅ |
| MOM_TEST §8 인터뷰·최종 — DEF-020 | §7 Partial Go, §8 자동 `[x]` | **부분완료** (Phase 6) |
| test_plan Gate 스냅샷 — DEF-021 | v1.1 Green Gate | **부분완료** (79건 반영 예정) |
| README 기능 문구 — DEF-022 | 건수 통계·규칙 기반 명시 | **부분완료** |
| Phase 0 수동 E2E | `manual_e2e_phase0.md` | **미착수** |

---

## 4. 전후 코드 비교

### 4.1 감정 분류 (B-01 · DEF-001~003)

**Before (`red` — `filters.py`)**

```python
S_KEYWORDS = {"긍정": [...], "부정": [...], "중립": [...]}  # constants와 불일치

def filter_feedbacks(data_list, sentiment_filter, keyword_filter):
    if sentiment_filter != "전체":
        for item in data_list:
            if _contains_any(txt, S_KEYWORDS["긍정"]):
                current_sentiment = "긍정"
            elif _contains_any(txt, S_KEYWORDS["부정"]):
                current_sentiment = "부정"
            # ...
```

**After (`new_feature` — `services/sentiment.py`, `services/filter_service.py`)**

```python
def classify_sentiment(text: str) -> str:
    keywords = _sentiment_keywords()  # SQLite → constants 시드
    if contains_any(text, keywords["긍정"]):
        return "긍정"
    if contains_any(text, keywords["부정"]):
        return "부정"
    return "중립"

def filter_feedbacks(data_list, sentiment_filter, keyword_filter):
    tmp_filtered = [
        item for item in data_list
        if classify_sentiment(item.text) == sentiment_filter
    ]
```

---

### 4.2 카테고리 main 매칭 (B-02 · DEF-004)

**Before (`red`)**

```python
for sub_key, sub_keywords in cat_map.items():
    if sub_key == "main":
        continue  # main 키워드 미사용 → 버그
    if _contains_any(txt, sub_keywords):
        final_filtered.append(item)
```

**After (`new_feature` — `services/category.py`)**

```python
def matches_category(text: str, category: str) -> bool:
    sub_map = CATEGORY_KEYWORDS.get(category)
    if not sub_map or "main" not in sub_map:
        return False
    return contains_any(text, sub_map["main"])
```

---

### 4.3 다운로드·세션 (B-03 · DEF-005)

**Before (`red` — `app.py`)**

```python
fil_data: list = []

@app.route("/filter", methods=["POST"])
def filter_route():
    global fil_data
    fil_data = filtered

@app.route("/download", methods=["GET"])
def download():
    for fb in fil_data:
        output.write(fb.text + "\n")
```

**After (`new_feature`)**

```python
# models/session.py
def set_download_feedbacks(self, feedbacks): ...
def get_download_feedbacks(self): ...

# handlers/download.py
rows = get_session().get_download_feedbacks()
output.write("text\n")
for fb in rows:
    output.write(fb.text + "\n")
```

---

### 4.4 애플리케이션 구조 (Phase 3~4)

**Before (`red`)**

```python
# app.py (~240줄)
def render_page(...):  # HTML + 비즈니스 혼재
    ...

@app.route("/analyze", methods=["POST"])
def analyze(): ...

class TextAnalyzer:
    global_sent = {}
    global_kw = {}
    def sent(self, feedbacks): ...
    def kw(self, feedbacks): ...
```

**After (`new_feature`)**

```python
# app.py (~18줄)
app = Flask(__name__)
register_blueprints(app)

# services/analysis_service.py
class TextAnalyzer:
    def analyze_sentiments(self, feedbacks): ...
    def analyze_keywords(self, feedbacks): ...

# html_renderer.py
class HtmlRenderer:
    def render(self, ...): ...
```

---

### 4.5 아키텍처 다이어그램

```text
[Before]                          [After]
app.py (240줄)                    app.py (18줄)
 ├── render_page                   ├── register_blueprints
 ├── fil_data                      handlers/  → HTTP
 ├── routes...                     services/  → sentiment, category, csv, trend, keyword_db
text_analyzer (global_*)            models/    → Feedback, Session
filters (S_KEYWORDS)                html_renderer.py
file_handler (dead)                 tests/ (79)
```

---

## 5. 효과 및 향후 과제

### 5.1 정량 효과

| 항목 | 효과 |
|------|------|
| 기능 정합성 | PRD Anchor·중립 3건·`품질` main 회귀 **pass** |
| 테스트 | 6건 → **79 passed**, cov **94.15%**, Golden Master 회귀 |
| 구조 | God Module 해소, 레이어 분리로 변경 영향 국소화 |
| 확장성 | Trend·SQLite CRUD로 운영 키워드·시계열 분석 가능 |
| 결함 | DEF-001~019, 023 **완료** (21/23 완료, 3 부분) |

### 5.2 정성 효과

- 분석·필터·다운로드가 **동일 분류 규칙**을 사용해 사용자 신뢰도 향상
- UI(`html_renderer`)와 도메인(`services`) 분리로 유지보수·테스트 용이
- TDD Red 기준선 → Green 수정 → Refactor 스멜 제거 **교육 목표 달성**

### 5.3 잔여 한계

| 항목 | 설명 |
|------|------|
| 규칙 기반 substring | ML/NLP 미적용, 동의어·문맥 한계 |
| ADR-001 main-only | sub 키워드만 포함한 본문은 0건 (v1 정책) |
| Anemic Domain | S-A05/S-FB01 부분 개선, 추가 DDD는 선택 |
| 셔임 모듈 | `feedback.py`, `session.py` 등 re-export 잔존 |

### 5.4 향후 과제 (Phase 6)

| 순서 | 과제 | 산출물 |
|------|------|--------|
| 1 | Phase 0 브라우저 수동 E2E | `report/manual_e2e_phase0.md` |
| 2 | DEF-020~022 문서 종결 | MOM_TEST §8, test_plan Gate 79, PRD §4 |
| 3 | 팀 리뷰·발표 | `report/team_review.md`, 슬라이드·라이브 데모 |
| 4 | Gate 재실행 기록 | pytest · cov · Golden Master |
| 5 | (선택) `new_feature` → `main` merge | 팀 브랜치 정책 |

### 5.5 검증 명령

```bash
cd src/python
pytest tests/domain/test_anchor_prd_example.py tests/domain/test_filters_regression.py -v
pytest tests/ --cov --cov-fail-under=90 -q
python scripts/generate_golden_master.py --check
```

---

## 참고

- [report/refactoring_before_after.md](report/refactoring_before_after.md)
- [doc/defect_list.md](doc/defect_list.md)
- [doc/CODE_SMELL.md](doc/CODE_SMELL.md)
- [README.md](README.md)
