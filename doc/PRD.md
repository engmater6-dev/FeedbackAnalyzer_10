# PRD: Feedback Analyzer (리팩토링 챌린지)

| 항목 | 내용 |
|------|------|
| 문서 버전 | 1.2 |
| 최종 수정 | 2026-05-22 (Phase 5 `new_feature`) |
| 프로젝트명 | 리팩토링 챌린지: 고객 피드백 분석 시스템 |
| 관련 문서 | [README.md](../README.md), [project_purpose.md](../project_purpose.md), [MOM_TEST.md](MOM_TEST.md), [CODE_SMELL.md](CODE_SMELL.md), [test_plan.md](test_plan.md) |

---

## 1. 제품 개요

### 1.1 목적

자연어 기반 고객 피드백을 수집·분류·시각화하는 Flask 웹 애플리케이션이다. **운영 제품**이 아니라 **리팩토링·TDD·클린 코드 실습용** 코드베이스이며, 의도적으로 포함된 코드 스멜과 안티패턴을 학습자가 식별·개선하는 것이 핵심 가치이다.

### 1.2 대상 사용자

| 역할 | 설명 |
|------|------|
| 학습자 | 중급 이상 Python 개발자, TDD·리팩토링 실습 참여자 |
| 강사/리뷰어 | 8단계 미션 진행·코드 리뷰·발표 평가 |

### 1.3 성공 지표 (완료 정의)

- 단위·통합 테스트 커버리지 **90% 이상**
- 문서화된 버그(중립 필터, 카테고리 필터 불일치 등) 수정
- 비즈니스 로직과 UI(HTML) 분리
- 키워드·감정 규칙의 단일 진실 원천(Single Source of Truth) 확보
- Trend 시각화 및 감정 키워드 File DB 관리 기능 구현 (Phase 2)

---

## 2. 현재 제품 기능 (As-Is)

### 2.1 핵심 기능

| ID | 기능 | 설명 | 엔드포인트 |
|----|------|------|------------|
| F-01 | 대시보드 | 웹 UI 제공 | `GET /` |
| F-02 | 텍스트 입력 | 단건·다건 피드백 수동 입력 | `POST /analyze` |
| F-03 | CSV 업로드 | 파일로 피드백 일괄 등록 | `POST /upload` |
| F-04 | 감정 분석 | 긍정/부정/중립 키워드 매칭 집계 | `POST /analyze`, `POST /filter` |
| F-05 | 카테고리 분류 | 배송·품질·가격·서비스·사용성 | `POST /analyze`, `POST /filter` |
| F-06 | 필터링 | 감정·카테고리 조건 필터 | `POST /filter` |
| F-07 | 결과 시각화 | 감정·키워드 분포 숫자 표시 | HTML stats 영역 |
| F-09 | Trend 추이 | `date,text` CSV 월별 감정·키워드 막대 | `POST /upload` + HTML Trend 섹션 |
| F-10 | 감정 키워드 DB | SQLite CRUD·분류 SSOT | `POST /settings/keywords` · `keyword_db` |
| F-08 | CSV 다운로드 | 필터 결과보내기 | `GET /download` |

### 2.2 사용자 시나리오

1. `http://localhost:8080` 접속
2. 피드백 텍스트 입력 또는 CSV 업로드
3. (선택) 「분석」으로 감정·카테고리 필터 적용
4. 통계 확인 후 필요 시 CSV 다운로드

### 2.3 입출력 명세

| 기능 | 입력 | 출력 |
|------|------|------|
| 텍스트 입력 | `"배송이 너무 늦어요. 화가 납니다."` | 감정: 부정, 카테고리: 배송 (집계) |
| CSV 업로드 | `feedbacks.csv` (`text` 컬럼 권장) | 세션에 피드백 누적 |
| 감정 분석 | 피드백 목록 | `{긍정: n, 중립: n, 부정: n}` |
| 키워드 필터 | 감정=`중립`, 키워드=`배송` | 조건 일치 피드백 목록·집계 |
| 다운로드 | (필터 성공 후) | `filtered_feedback.csv` |

### 2.4 CSV 업로드 규격 (Phase 3-B)

상세: [CSV_FORMAT.md](CSV_FORMAT.md)

| 모드 | 조건 | 파싱 |
|------|------|------|
| **표준 (권장)** | 1행 헤더에 `text` | 2행부터 `text` 열, 빈 셀 제외 |
| **레거시** | `text` 헤더 없음 | **0번 열**, **1행부터** 전부 데이터 (헤더 스킵 없음) |

- 인코딩: UTF-8 / BOM 허용  
- B-04 **Resolved** (`_parse_csv_to_feedbacks`)

### 2.5 카테고리 매칭 정책 (Phase 3-B)

상세: [ADR-001-category-main-only.md](ADR-001-category-main-only.md)

| 항목 | 정책 |
|------|------|
| 매칭 범위 | `CATEGORY_KEYWORDS[cat]["main"]` substring만 |
| `sub` 맵 | 분류 메타·향후 확장용, **런타임 미사용** |
| `kw()` vs `filter` | `matches_category()` 단일 SSOT (B-02) |
| sub 확장 | Phase 5 인터뷰 **Go** 전까지 **No-Go** (DEF-016 문서 완료) |

---

## 3. 기술 아키텍처 (As-Is)

### 3.1 스택

- Python 3.9+
- Flask 3.1.0
- 의존성: `requirements.txt` (flask 단일)

### 3.2 모듈 구조

```
src/python/
├── app.py           # Flask, 라우팅, render_page (God Function)
├── feedback.py      # Feedback 모델
├── text_analyzer.py # sent(), kw() — 감정·카테고리 집계
├── filters.py       # filter_feedbacks() — classify_sentiment / matches_category 공유
├── constants.py     # SENTIMENT_KEYWORDS, CATEGORY_KEYWORDS
├── session.py       # Session.current_feedbacks (클래스 변수)
├── logger.py        # print/stderr 로깅
└── html_renderer.py # UI (Phase 3-C-2)
```

### 3.3 데이터 흐름

```
Browser → app.py (라우트)
       → Session.current_feedbacks (피드백 저장)
       → TextAnalyzer.sent/kw (집계)
       → filter_feedbacks (필터) → Session.download_feedbacks
       → Logger (터미널만)
```

---

## 4. 알려진 문제 (버그·불일치)

### 4.1 Green에서 해결됨 (`green` · 2026-05-22)

| ID | 상태 | 수정 요약 |
|----|------|-----------|
| B-01 | **Resolved** | `classify_sentiment()` SSOT, `S_KEYWORDS` 제거 |
| B-02 | **Resolved** | `matches_category()` — main-only ([ADR-001](ADR-001-category-main-only.md)) |
| B-03 | **Resolved** | `Session.download_feedbacks`, `fil_data` 제거 |
| B-04 | **Resolved** | [CSV_FORMAT.md](CSV_FORMAT.md), `_parse_csv_to_feedbacks` |
| B-05 | **Resolved** | upload 직후 `sent`/`kw` |
| B-06 | **Resolved** (부분) | warning/error UI — level 토글은 Phase 3-C (DEF-008) |

### 4.2 잔여·정책 (문서화 완료)

| ID | 유형 | 내용 | 처리 |
|----|------|------|------|
| — | CSV 레거시 | 헤더 없을 때 1행=데이터 | [CSV_FORMAT.md](CSV_FORMAT.md) §2 — **By design** |
| — | 카테고리 | sub 키워드 미매칭 | [ADR-001](ADR-001-category-main-only.md) — **Won't fix (v1)** |

### 4.3 Red 기준선 (참고)

| ID | Red 시 문제 | Green |
|----|-------------|-------|
| B-01 | 중립 필터 불일치 | ✅ |
| B-02 | 카테고리 filter vs kw | ✅ |
| B-03 | 다운로드 `fil_data` | ✅ |
| B-04 | CSV `text` 무시 | ✅ |
| B-05 | 업로드 후 미분석 | ✅ |
| B-06 | 로그 UI 없음 | ✅ (토글 잔여) |

---

## 5. 의도적 기술 부채 (학습용) — 제거 현황

| 유형 | Red 위치 | After (`new_feature`) | Phase |
|------|----------|------------------------|-------|
| God Function | `app.render_page()` | `html_renderer.HtmlRenderer` | 3-C-2 ✅ |
| 중복 코드 | `_contains_any` ×2 | `text_utils.contains_any` | 3-C-6 ✅ |
| 전역 상태 | `fil_data`, `global_sent`, `global_kw` | `Session` 인스턴스·반환값만 | Green·3-C-1 ✅ |
| 부적절한 네이밍 | `sent`, `kw` | `analyze_sentiments`, `analyze_keywords` | 3-C-5 ✅ |
| Lava Flow | `file_handler.py` | 삭제 | 3-C-3 ✅ |
| 테스트 부재 | 없음 | **79 tests**, cov **94.15%** | Green~5 ✅ |
| Shotgun Surgery | `S_KEYWORDS` + constants | `classify_sentiment()` + SQLite | Green·5 ✅ |
| 레이어 혼재 | 단일 `app.py` | handlers / services / models | Phase 4 ✅ |

---

## 6. 목표 제품 기능 (To-Be)

### 6.1 Phase 1 — 안정화·리팩토링 (미션 1~6)

| ID | 요구사항 | 우선순위 |
|----|----------|----------|
| R-01 | pytest 기반 테스트, coverage ≥ 90% | P0 |
| R-02 | 중립·카테고리 필터 버그 수정 (B-01, B-02) | P0 |
| R-03 | 로그 level별 UI 표시 (warning, error) | P1 |
| R-04 | 멀티라인 입력 UX 개선 (textarea·개행) | P1 |
| R-05 | 네이밍·전역·하드코딩 정리 | P1 |
| R-06 | `render_page` 분리, `_contains_any` 통합 | P1 |
| R-07 | `handlers/`, `services/`, `models/` 디렉터리 분리 | P2 |
| R-08 | Feedback 모델에 분석 결과·setter | P2 |

### 6.2 Phase 2 — 확장 (미션 7)

| ID | 요구사항 | 우선순위 |
|----|----------|----------|
| R-09 | Trend 시각화 (`sample/test_feedback_trend.csv`) | P1 |
| R-10 | 감정 키워드 File DB (SQLite 등) CRUD | P1 |
| R-11 | CSV 업로드 `text` 컬럼 표준 준수 (B-04) | P1 |

### 6.3 Phase 3 — 협업 (미션 8)

| ID | 요구사항 |
|----|----------|
| R-12 | 팀 코드 리뷰·`report/` 산출물 |
| R-13 | 발표용 장단점 정리 |

---

## 7. 비기능 요구사항

| 항목 | 요구 |
|------|------|
| 실행 환경 | 로컬, `0.0.0.0:8080` |
| 인코딩 | UTF-8, CSV BOM 지원 |
| 보안 | 실습 범위 — 인증·Rate limit 없음 |
| 테스트 | Red-Green-Refactor, 커버리지 90%+ |
| 문서 | README, PRD, project_purpose 동기화 |

---

## 8. TDD 기반 개발 단계 (권장)

| 단계 | Red (실패 테스트) | Green (구현) | Refactor |
|------|-------------------|--------------|----------|
| 1 | `Feedback`, `Session` 기본 | 모델·세션 | — |
| 2 | `classify_sentiment`, `classify_category` | `text_analyzer` | 키워드 단일 소스 |
| 3 | `filter_feedbacks` 중립·카테고리 | `filters` 수정 | `_contains_any` 통합 |
| 4 | Flask 라우트 integration | `app` 핸들러 | `render_page` 분리 |
| 5 | Logger UI, CSV parser | `logger`, upload | — |
| 6 | Trend, File DB | 신규 모듈 | 디렉터리 구조 |

---

## 9. 제약 및 가정

- 외부 ML/NLP API 미사용 — 규칙 기반 키워드 매칭만 사용
- 단일 프로세스·단일 사용자 세션 (클래스 변수 세션)
- `sample/test_feedback_trend.csv`는 학습자가 `sample/`에 추가
- `.venv`는 저장소에 포함하지 않는 것을 권장

---

## 10. 참고: HTTP API 요약

| Method | Path | Body/Query | Response |
|--------|------|------------|----------|
| GET | `/` | — | HTML 대시보드 |
| POST | `/analyze` | `text` | HTML + 집계 |
| POST | `/upload` | `file` (multipart) | HTML |
| POST | `/filter` | `sentiment`, `keyword` | HTML + 집계 |
| GET | `/download` | — | `filtered_feedback.csv` |

---

## 11. 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 1.0 | 2026-05-22 | 초기 PRD 작성 (코드·project_purpose 분석 기반) |
| 1.1 | 2026-05-22 | Phase 3-B — §2.4 CSV, §2.5 카테고리 ADR, §4 Green Resolved |
