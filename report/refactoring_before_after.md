# 리팩토링 전후 비교 보고서

| 항목 | 내용 |
|------|------|
| 문서 ID | REPORT-REF-01 |
| 작성일 | 2026-05-22 |
| Before 기준 | 브랜치 `red` (TDD Red · 의도적 스멜·버그) |
| After 기준 | 브랜치 `new_feature` (Green → Refactor → Phase 4~5) |
| 근거 | [doc/CODE_SMELL.md](../doc/CODE_SMELL.md), [doc/defect_list.md](../doc/defect_list.md), [report/02.green.md](02.green.md), [report/03.refactor.md](03.refactor.md), [report/05.new_feature.md](05.new_feature.md) |

---

## 1. 요약

| 지표 | Before (`red`) | After (`new_feature`) |
|------|----------------|------------------------|
| Python 모듈 수 | 8 (+ `file_handler.py`) | 30+ (`handlers/`, `services/`, `models/`, …) |
| `app.py` 줄 수 | **~240** (라우팅·HTML·I/O 혼재) | **~18** (부트스트랩만) |
| Domain 테스트 | 4 fail / 2 pass | Anchor·회귀 **pass** |
| 전체 pytest | 6 (+ skip) | **79 passed** |
| 커버리지 | ~39% (domain만) | **94.15%** |
| Golden Master | 없음 | `golden_master_expected.txt` + `--check` |
| QA 결함 | 8+ 기능·구조 이슈 | DEF-001~019 **완료**, 020~022 문서 잔여 |

**핵심 변화 한 줄:** 감정·카테고리 **규칙 이중화·전역 상태·God Module**을 제거하고, **SSOT 서비스 + 레이어 분리 + 테스트 회귀**로 교체했다.

---

## 2. 아키텍처 Before / After

### Before (`red`)

```text
app.py (240줄)
  ├── render_page()      ← HTML + 비즈니스 + fil_data
  ├── /analyze, /filter, /upload, /download
  └── csv 파싱 (0열만, 헤더 스킵 버그)

text_analyzer.py  ← sent(), kw(), global_sent/kw
filters.py        ← S_KEYWORDS (constants와 불일치)
constants.py
session.py        ← 클래스 변수만
file_handler.py   ← Lava Flow (미사용)
```

### After (`new_feature`)

```text
app.py                    ← Flask + Blueprint 등록만
handlers/                 ← HTTP (analyze, upload, filter, download, …)
services/                 ← csv_parser, sentiment, category, keyword_db, trend
models/                   ← Feedback (+ sentiment, category, recorded_at), Session
html_renderer.py          ← UI (Trend·키워드 CRUD 포함)
text_utils.py             ← contains_any SSOT
analysis_strategies.py    ← 셔임 (하위 호환)
tests/                    ← domain + boundary + Golden Master
```

---

## 3. 기능 버그 수정 (Green · B-01~B-06)

### 3.1 B-01 감정 분류 — 규칙 이중화 제거 (DEF-001~003)

**증상:** PRD 예시 `"배송이 너무 늦어요. 화가 납니다."` → 분석은 중립, 필터(부정+배송) 0건.

#### Before — `filters.py` (`red`)

`constants.SENTIMENT_KEYWORDS`와 **별도** `S_KEYWORDS`를 사용하고, analyzer와 순서·키워드가 다름.

```python
S_KEYWORDS = {
    "긍정": ["좋아요", "만족", ...],
    "부정": ["나쁘", "불만", ...],  # "화가" 없음
    "중립": ["괜찮", "보통", ...],
}

def filter_feedbacks(data_list, sentiment_filter, keyword_filter):
    if sentiment_filter != "전체":
        tmp_filtered = []
        for item in data_list:
            txt = item.text
            if _contains_any(txt, S_KEYWORDS["긍정"]):
                current_sentiment = "긍정"
            elif _contains_any(txt, S_KEYWORDS["부정"]):
                current_sentiment = "부정"
            elif _contains_any(txt, S_KEYWORDS["중립"]):
                current_sentiment = "중립"
            else:
                current_sentiment = "중립"
            if current_sentiment == sentiment_filter:
                tmp_filtered.append(item)
    # ...
    for fb in final_filtered:
        print(fb.text)  # 디버그 잔류
    return final_filtered
```

#### Before — `text_analyzer.py` (`red`)

```python
class TextAnalyzer:
    global_sent: Dict[str, int] = {}
    global_kw: Dict[str, int] = {}

    def sent(self, feedbacks):
        res = {"긍정": 0, "중립": 0, "부정": 0}
        for f in feedbacks:
            txt = f.text
            if self._contains_any(txt, SENTIMENT_KEYWORDS["긍정"]):
                s = "긍정"
            elif self._contains_any(txt, SENTIMENT_KEYWORDS["부정"]):
                s = "부정"
            else:
                s = "중립"  # elif 중립 키워드 분기 없음
            res[s] += 1
        TextAnalyzer.global_sent = res
        return res
```

#### After — `services/sentiment.py` + `services/filter_service.py`

단일 함수 `classify_sentiment()` (Phase 5: SQLite DB SSOT). 필터·집계·모델 주석이 **동일 규칙** 사용.

```python
# services/sentiment.py
def classify_sentiment(text: str) -> str:
    keywords = _sentiment_keywords()  # keyword_db → constants 시드
    if contains_any(text, keywords["긍정"]):
        return "긍정"
    if contains_any(text, keywords["부정"]):
        return "부정"
    return "중립"


# services/filter_service.py
def filter_feedbacks(data_list, sentiment_filter, keyword_filter):
    if sentiment_filter != "전체":
        tmp_filtered = [
            item for item in data_list
            if classify_sentiment(item.text) == sentiment_filter
        ]
    # ...
    return final_filtered  # print 제거
```

| 입력 | Before `sent` | After `analyze_sentiments` |
|------|---------------|----------------------------|
| PRD Anchor 문장 | 중립 1 | **부정 1** |
| `filter(부정, 배송)` | 0건 | **≥1건** |

---

### 3.2 B-02 카테고리 — `main` 키워드 스킵 (DEF-004)

#### Before — `filters.py` (`red`)

`main` 서브맵을 **의도적으로 skip** → `"품질"` 본문은 `kw()`에서 1건, 필터에서는 0건.

```python
if keyword_filter in CATEGORY_KEYWORDS:
    cat_map = CATEGORY_KEYWORDS[keyword_filter]
    for item in tmp_filtered:
        txt = item.text
        for sub_key, sub_keywords in cat_map.items():
            if sub_key == "main":
                continue  # ← 버그: main 미매칭
            if _contains_any(txt, sub_keywords):
                final_filtered.append(item)
                break
```

#### After — `services/category.py` (ADR-001 main-only)

```python
def matches_category(text: str, category: str) -> bool:
    sub_map = CATEGORY_KEYWORDS.get(category)
    if not sub_map or "main" not in sub_map:
        return False
    return contains_any(text, sub_map["main"])
```

`analyze_keywords()` 집계와 `filter_feedbacks()`가 **동일** `matches_category()` 사용.

---

### 3.3 B-03 다운로드 — 전역 `fil_data` (DEF-005)

#### Before — `app.py` (`red`)

필터 결과를 전역 `fil_data`에만 저장. `/analyze` 직후 다운로드 시 빈 파일·구버전.

```python
fil_data: list = []

@app.route("/filter", methods=["POST"])
def filter_route():
    global fil_data
    filtered = filter_feedbacks(feedbacks, sentiment, keyword)
    if filtered:
        fil_data = filtered
        # ...

@app.route("/download", methods=["GET"])
def download():
    output = io.StringIO()
    output.write("\ufeff")
    for fb in fil_data:          # text 헤더 없음
        output.write(fb.text + "\n")
```

#### After — `models/session.py` + `handlers/download.py`

```python
# models/session.py
class Session:
    def set_download_feedbacks(self, feedbacks: List[Feedback]) -> None:
        self._download_feedbacks = list(feedbacks)

    def get_download_feedbacks(self) -> List[Feedback]:
        return self._download_feedbacks


# handlers/download.py
def download():
    rows = get_session().get_download_feedbacks()
    if not rows:
        return render_page(warning="다운로드할 피드백이 없습니다.")
    output.write("text\n")  # B-04 정렬: 헤더 + 본문
    for fb in rows:
        output.write(fb.text + "\n")
```

---

### 3.4 B-04 CSV — `text` 헤더 무시 (DEF-006)

#### Before — `app.py` upload (`red`)

첫 행 스킵, **0번 열만** 사용 → `text` 헤더 CSV 오동작.

```python
reader = csv.reader(io.StringIO(content))
first_line = True
for row in reader:
    if first_line:
        first_line = False
        continue
    if row and row[0].strip():
        feedbacks.append(Feedback(row[0].strip()))
```

#### After — `services/csv_parser.py`

```python
def parse_csv_to_feedbacks(content: str) -> List[Feedback]:
    # 헤더에 "text" → text 열만
    # "date,text" → Trend 모드 (recorded_at)
    # 헤더 없음 → 레거시 0열 전체 (CSV_FORMAT.md §2)
```

---

## 4. 구조 리팩토링 (Phase 3 Refactor)

### 4.1 God Function · God Module (S-A01, S-A02 · DEF-017)

#### Before — `app.py` 일부 (`red`)

`render_page()` 한 함수에 폼·통계·HTML·로그 토글까지 포함 (~200줄+).

```python
def render_page(success="", warning="", error="",
                sentiment_results=None, keyword_results=None, feedbacks=None):
    # 수백 줄 HTML 문자열 조립 ...
    return html

@app.route("/analyze", methods=["POST"])
def analyze():
    # Session, TextAnalyzer, render_page 직접 호출
    return render_page(success="...", sentiment_results=..., ...)
```

#### After — `app.py` + `html_renderer.py`

```python
# app.py (~18줄)
app = Flask(__name__)
register_blueprints(app)

# html_renderer.py
class HtmlRenderer:
    def render(self, success="", warning="", error="",
               sentiment_results=None, keyword_results=None,
               trend_sentiment=None, trend_keyword=None, ...):
        # 프레젠테이션만 담당
```

---

### 4.2 클래스 전역 부작용 (S-T02 · DEF-018)

#### Before (`red` / 초기 `green`)

```python
class TextAnalyzer:
    global_sent: Dict[str, int] = {}
    global_kw: Dict[str, int] = {}

    def sent(self, feedbacks):
        # ...
        TextAnalyzer.global_sent = res  # 요청 간 상태 누수 위험
        return res
```

#### After — `services/analysis_service.py`

```python
class TextAnalyzer:
    def analyze_sentiments(self, feedbacks: List[Feedback]) -> Dict[str, int]:
        annotate_feedbacks(feedbacks)
        res = {"긍정": 0, "중립": 0, "부정": 0}
        for f in feedbacks:
            res[f.sentiment] += 1
        return res  # 반환값만, 클래스 변수 없음
```

---

### 4.3 중복 `_contains_any` (S-T03 · 3-C-6)

#### Before

`text_analyzer.py`와 `filters.py`에 각각 동일 헬퍼.

#### After — `text_utils.py`

```python
def contains_any(text: str, keywords: List[str]) -> bool:
    return any(kw in text for kw in keywords)
```

`services/sentiment.py`, `services/category.py`에서 import.

---

### 4.4 Lava Flow — `file_handler.py` (S-FH01 · DEF-019)

#### Before (`red`)

```python
class FileHandler:
    """Dead code - kept for parity with original C++ project."""
    def save_result(self, data: List[Feedback]):
        print(f"saveResult{len(data)}")
```

#### After

파일 **삭제**. 다운로드는 `handlers/download.py` + `Session.get_download_feedbacks()`만 사용.

---

### 4.5 전략 패턴 · 네이밍 (3-C-5, 3-C-7)

#### Before

```python
analyzer.sent(feedbacks)
analyzer.kw(feedbacks)
```

#### After

```python
# services/analysis_service.py
analyzer.analyze_sentiments(feedbacks)
analyzer.analyze_keywords(feedbacks)

# services/sentiment.py · category.py
class RuleBasedSentimentStrategy:
    def classify(self, text: str) -> str: ...

class RuleBasedCategoryStrategy:
    def matches(self, text: str, category: str) -> bool: ...
```

---

## 5. 구조 분리 (Phase 4 · R-07, R-08)

### 5.1 레이어 분리

#### Before (`red`)

모든 HTTP가 `app.py` 단일 파일.

#### After — Blueprint 등록

```python
# handlers/__init__.py
def register_blueprints(app: Flask) -> None:
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(analyze_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(filter_bp)
    app.register_blueprint(download_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(keywords_bp)
```

| 책임 | Before | After |
|------|--------|-------|
| HTTP | `app.py` | `handlers/*.py` |
| 규칙·집계 | `text_analyzer`, `filters` | `services/*` |
| 상태 | `Session` 클래스 변수 + `fil_data` | `models/session.Session` 인스턴스 |
| UI | `render_page` in app | `html_renderer.HtmlRenderer` |

---

### 5.2 도메인 모델 강화 (S-FB01 · R-08)

#### Before — `feedback.py` (`red`)

```python
class Feedback:
    def __init__(self, text: str):
        self._text = text
    @property
    def text(self) -> str:
        return self._text
```

#### After — `models/feedback.py`

```python
class Feedback:
    def __init__(self, text: str, sentiment=None, category=None, recorded_at=None):
        self._text = text
        self._sentiment = sentiment
        self._category = category
        self._recorded_at = recorded_at

    @sentiment.setter
    def sentiment(self, value: str) -> None:
        self._sentiment = value
```

`annotate_feedbacks()`가 분석 시 `sentiment`·`category`를 피드백 객체에 기록.

---

## 6. 기능 확장 (Phase 5 · R-09, R-10)

### 6.1 Trend 시각화 (Before: 없음)

#### After — `services/trend_service.py` + `html_renderer`

`date,text` CSV 업로드 시 월별 감정·키워드 막대 차트. `text`만 CSV는 기존 건수 통계만 표시.

```python
# models/feedback.py — 필드 추가
recorded_at: Optional[str]  # "2026-01-15" 등
```

---

### 6.2 감정 키워드 SQLite DB (S-C01, S-C02)

#### Before

`constants.SENTIMENT_KEYWORDS` 하드코딩만. 런타임 변경 불가.

#### After

```python
# services/keyword_db.py — SQLite CRUD
# handlers/keywords.py — POST /settings/keywords
# services/sentiment.py — DB 캐시 + invalidate_sentiment_cache()
```

UI에서 키워드 추가/삭제 시 `classify_sentiment()`·필터가 **동일 DB**를 참조.

---

## 7. 테스트·회귀 Before / After

| 단계 | 명령 | Before | After |
|------|------|--------|-------|
| Domain Gate | `pytest tests/domain/test_anchor_prd_example.py …` | 4F 2P | **pass** |
| 전체 | `pytest tests/ --cov --cov-fail-under=90` | ~39% cov | **79 passed**, **94.15%** |
| Approval | `generate_golden_master.py --check` | — | **OK** |

**Golden Master 예시 (After):**

```text
[anchor_prd]
sent={'긍정': 0, '중립': 0, '부정': 1}
filter_negative_shipping_count>=1
```

---

## 8. 스멜·결함 매핑표

| 스멜 ID | Before 문제 | After 조치 | Phase |
|---------|-------------|------------|-------|
| S-F01, S-F02 | `S_KEYWORDS` 3중 정의 | `classify_sentiment()` SSOT | Green |
| S-F03, S-T05 | filter가 `main` skip | `matches_category()` | Green |
| S-A03 | `fil_data` | `Session._download_feedbacks` | Green |
| S-A06 | CSV 0열만 | `csv_parser` + SPEC | Green |
| S-T02 | `global_sent/kw` | 제거 | Refactor |
| S-A01, S-A02 | God Function/Module | `HtmlRenderer` | Refactor |
| S-FH01 | `file_handler.py` | 삭제 | Refactor |
| S-T03 | 중복 `_contains_any` | `text_utils` | Refactor |
| S-T01 | `sent`/`kw` | `analyze_sentiments`/`keywords` | Refactor |
| — | 단일 `app.py` | handlers/services/models | Phase 4 |
| S-C01, S-C02 | 하드코딩 감정 | SQLite `keyword_db` | Phase 5 |

---

## 9. 잔여·한계 (After에도 유지)

| 항목 | 설명 |
|------|------|
| 규칙 기반 substring | ML/NLP 아님 — 동의어·문맥 한계 |
| ADR-001 main-only | `sub` 키워드만 있는 본문은 0건 (정책) |
| 셔임 모듈 | `feedback.py`, `session.py`, `text_analyzer.py` re-export (하위 호환) |
| DEF-020~022 | MOM_TEST·test_plan·발표 문서 — Phase 6 종결 예정 |
| S-A05 / S-FB01 | Anemic Domain **부분 개선** (필수 과제 아님) |

---

## 10. 브랜치·커밋 타임라인

```text
red          → TDD Red (4 fail 고정)
green        → B-01~B-06, 39 passed
refactor     → 3-C-1~7, HtmlRenderer, 50 passed
feature/…    → handlers/services/models, 55 passed
new_feature  → Trend + SQLite, 79 passed
```

**로컬에서 Before 코드 확인:**

```bash
git show red:src/python/filters.py
git show red:src/python/app.py
```

**After 코드:** 현재 워킹 트리 `src/python/` (`new_feature`).

---

## 11. 참고 문서

- [doc/CODE_SMELL.md](../doc/CODE_SMELL.md) — 스멜 ID 상세
- [doc/defect_list.md](../doc/defect_list.md) — DEF-001~023
- [doc/ADR-001-category-main-only.md](../doc/ADR-001-category-main-only.md)
- [doc/CSV_FORMAT.md](../doc/CSV_FORMAT.md)
- [report/02.green.md](02.green.md) · [report/03.refactor.md](03.refactor.md) · [report/04.feature.md](04.feature.md) · [report/05.new_feature.md](05.new_feature.md)

---

*본 보고서는 Phase 6 `team_review.md` 초안으로도 활용할 수 있습니다.*
