# 결함 목록 (Defect List)

| 항목 | 내용 |
|------|------|
| 문서 ID | QA-DEF-01 |
| 작성 | QA 리드 |
| 일자 | 2026-05-22 |
| 대상 브랜치 | **`feature/phase-4-structure`** (Phase 3 `refactor` + Phase 4 구조) |
| 근거 | Red · Green · Refactor · QA 분석(`doc/`, `README.md`, `src/`) |
| 관련 | [PRD.md](PRD.md) §4, [CODE_SMELL.md](CODE_SMELL.md), [test_plan.md](test_plan.md), [MOM_TEST.md](MOM_TEST.md), [README.md](../README.md) |

---

## 1. 요약

| 구분 | 건수 |
|------|------|
| **전체** | 23 |
| **완료** | 21 |
| **부분완료** | 3 |
| **미완료** | 0 |

| Severity | 완료 | 부분완료 |
|----------|------|----------|
| Critical / High | 6 | 0 |
| Medium | 11 | 2 |
| Low | 4 | 1 |

| 마일스톤 | 상태 |
|----------|------|
| TDD Red (`red`) | ✅ Anchor 4 fail 고정 |
| TDD Green (`green`) | ✅ B-01~B-06, Step 0~7, Golden Master |
| Phase 3 Refactor (`refactor`) | ✅ 3-A~3-D (3-C-1~7, Gate **50 passed**) |
| Phase 4 구조 (`feature/phase-4-structure`) | ✅ 4-1~4-5 · Gate **55 passed** |
| Phase 5 (선택) | ⏳ Trend·DB |
| Phase 6 QA 종결 | ⏳ §6.6 Gate (DEF-020~022 문서·발표) |

> **최종 갱신 (2026-05-22 · `feature/phase-4-structure`):** pytest **55 passed** · cov **97.57%** · Golden Master **OK** · Phase 4 R-07/R-08 완료 · 문서 DEF **020~022 부분완료**

---

## 2. 결함 상세

| ID | Severity | 변환 타입 | 예정 Phase | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 | 완료 여부 |
|----|----------|-----------|------------|-----------|--------|--------|-----------|-----------|-----------|
| DEF-001 | High | 기능결함 | Green Step 1 | `TextAnalyzer().sent([Feedback("배송이 너무 늦어요. 화가 납니다.")])` | `부정:1`, `중립:0` | `중립:1`, `부정:0` | `constants` 부정에 `화가` 없음·`filters.S_KEYWORDS`와 규칙 이중화 | `classify_sentiment()` SSOT, `화가` 추가, `S_KEYWORDS` 제거 | **완료** |
| DEF-002 | High | 기능결함 | Green Step 1 | `filter_feedbacks(..., "부정", "배송")` PRD 예시 | 반환 ≥1건 | 0건 | 필터 `S_KEYWORDS`·부정 미매칭 | `classify_sentiment` 공유 | **완료** |
| DEF-003 | High | 기능결함 | Green Step 1 | 중립 3건 `sent` vs `filter(중립)` | 건수 일치 | 불일치 | 감정 규칙 이중화 | `classify_sentiment()` 단일화 | **완료** |
| DEF-004 | High | 기능결함 | Green Step 2 | `kw("품질")` vs `filter(..., "품질")` | 일치 | 불일치 | filter가 `main` skip | `matches_category()` | **완료** |
| DEF-005 | Medium | 기능결함 | Green Step 5 | `/analyze` 후 `/download` | 입력 반영 CSV | 빈/구버전 | `fil_data` | `Session.download_feedbacks` | **완료** |
| DEF-006 | Medium | 기능결함 | Green Step 5 | CSV `text` 헤더 | `text` 열 파싱 | 0열만 | 미구현 | `_parse_csv_to_feedbacks` | **완료** |
| DEF-007 | Low | UX | Green Step 5 | 업로드 직후 | 집계 표시 | 없음 | upload 미분석 | upload `sent`/`kw` | **완료** |
| DEF-008 | Low | UX | Phase 3 | warning/error UI | level별 on/off | stdout만 | `/settings/logs`·`apply_display_settings`·INFO 선택 | **완료** |
| DEF-009 | Low | UX | Green Step 4 | `filter_feedbacks` | stdout 미출력 | `print` | 디버그 | print 제거 | **완료** |
| DEF-010 | Medium | 테스트결함 | **Green Step 6** | `pytest --cov` | ≥90% | ~39% | IT·app 미측정 | **39** tests, cov **97.42%** | **완료** |
| DEF-011 | Medium | 테스트결함 | **Green Step 6** | boundary IT | HTTP 검증 | skip | IT 미착수 | IT-01~04 구현 | **완료** |
| DEF-012 | Medium | 테스트결함 | **Green Step 6** | CSV `text` E2E | upload IT Pass | 없음 | IT 없음 | `test_post_upload_text_header_csv` | **완료** |
| DEF-013 | Low | UX | **Green Step 6** | 연속 요청 로그 | 요청별만 | 누적 | 버퍼 미클리어 | `_begin_page_request()` | **완료** |
| DEF-014 | Low | UX | **Green Step 6** | 빈 `/download` | 안내 | 빈 CSV | 빈 목록 허용 | warning + 버튼 조건 | **완료** |
| DEF-015 | Medium | 기능결함 | Phase 3/문서 | CSV 헤더 없음 0열 | 명시적 규칙 | 레거시 0열 | 휴리스틱 없음 | [CSV_FORMAT.md](CSV_FORMAT.md) §2 | **완료** |
| DEF-016 | Medium | 기능결함 | Phase 3/문서 | sub-only 본문 | main-only 정책 | 0건 가능 | By design | [ADR-001](ADR-001-category-main-only.md) Won't fix v1 | **완료** |
| DEF-017 | High | 구조/기술부채 | Phase 3 | `render_page` | 분리 | God Function | S-A01 | `html_renderer.HtmlRenderer` | **완료** |
| DEF-018 | High | 구조/기술부채 | Phase 3 | `global_sent/kw` | 인스턴스 상태 | 클래스 변수 | S-T02 | `sent`/`kw` 반환값만 사용, 클래스 변수 제거 | **완료** |
| DEF-019 | Medium | 구조/기술부채 | Phase 3 | `file_handler.py` | 사용/삭제 | Lava Flow | S-FH01 | 미사용 모듈 삭제, `/download`는 Session 유지 | **완료** |
| DEF-020 | Medium | 문서 | Phase 3/6 | MOM_TEST §7~8 | Partial Go | Fail | 미갱신 | §7.2 Partial Go, §8 자동 `[x]` (Phase 3-A) | **부분완료** — §8 인터뷰·Phase 6 최종 |
| DEF-021 | Low | 문서 | Phase 3/6 | test_plan 메타 | `green` | `red` | 미갱신 | v1.1·Gate 39/cov 97% (Phase 3-A) | **부분완료** — Phase 6 최종 스냅샷 |
| DEF-022 | Low | 문서 | Phase 3/6 | README 기능 문구 | 건수 요약 | 시각화 과장 | 가설 괴리 | README 문구 완화(2026-05-22) | **부분완료** |
| DEF-023 | Medium | 테스트결함 | Green Step 7 | Domain 출력 스냅샷 회귀 | `golden_master_expected.txt` 대비 일치 | 수동 only | Approval 미적용 | Golden Master + `generate_golden_master.py` | **완료** |

---

## 3. PRD 버그 ID 매핑

| PRD | Defect ID | 완료 여부 |
|-----|-----------|-----------|
| B-01 | DEF-001, DEF-002, DEF-003 | 완료 |
| B-02 | DEF-004 | 완료 |
| B-03 | DEF-005 | 완료 |
| B-04 | DEF-006, DEF-015 | 완료 |
| B-05 | DEF-007 | 완료 |
| B-06 | DEF-008 | 완료 (3-C-4 UI 토글) |

---

## 4. Mom Test §8 재검증 매핑

| §8 항목 | Defect ID | 자동 검증 | 완료 여부 |
|---------|-----------|-----------|-----------|
| PRD 예시 부정·배송 필터 | DEF-001, DEF-002 | pytest Domain | **완료** |
| 중립 3건 일치 | DEF-003 | pytest Domain | **완료** |
| main only 카테고리 (`품질`) | DEF-004 | pytest Domain | **완료** |
| CSV `text` 헤더 업로드 | DEF-006, DEF-012 | pytest IT | **완료** |
| 실사용자 인터뷰 | — | — | **미완료** (선택) |

---

## 5. 테스트·회귀 현황 (2026-05-22 · `refactor`)

| 구분 | 수치 | 명령 |
|------|------|------|
| 전체 | **50 passed** | `pytest tests/ -q` |
| 커버리지 | **97.78%** | `pytest tests/ --cov --cov-fail-under=90` |
| Domain Gate | 6+ | Anchor·회귀·`test_text_utils`·`test_analysis_strategies` |
| Boundary IT | 12+ | `test_routes_analyze_filter` (로그 설정 IT 포함) |
| Golden Master | 1 | `test_golden_master` · `generate_golden_master.py --check` |

**모듈 커버리지:** `analysis_strategies`, `text_utils`, `html_renderer`, `text_analyzer` 등 **100%** 또는 **≥96%**

---

## 6. Phase별 작업 순서 체크리스트

[project_purpose.md](../project_purpose.md) 8단계 · [README](../README.md) Phase 0~6와 정렬.  
**Phase 6 종료 시** 아래 「Phase 6 Gate」를 모두 충족하면 QA 미완료·부분완료 결함을 **실습 완료**로 볼 수 있습니다.

### 6.0 전체 로드맵

```text
Phase 0 [ ] 수동 E2E
    ↓
Phase 1~2 ✅ (`green` · B-01~06 · Golden Master)
    ↓
Phase 3 ✅ (`refactor` · 3-A~D · 50 passed)
    ↓
Phase 4 [ ] (선택) 구조·모델
    ↓
Phase 5 [ ] (선택) Trend·DB
    ↓
Phase 6 [ ] 리뷰·문서·발표  ← DEF-020~022 최종
```

| Phase | 예상 | DEF·산출물 | Gate 요약 |
|-------|------|------------|-----------|
| 0 | 0.5h | 수동 E2E | 브라우저 5시나리오 |
| 1~2 | ✅ | Green | 39→50 tests, cov ≥90% |
| **3** | **✅** | **008~019, 015~016 문서, 3-C-1~7** | **50 passed, cov 97.78%, GM OK** |
| 4 | 선택 | R-07 | handlers/services 분리 |
| 5 | 3h | Trend·DB | ADR-001 재검토 |
| **6** | **2h** | **020~022, report, 발표** | **실습 종결 Gate** |

---

### Phase 0 — 준비·수동 검증 (약 0.5시간)

**목표:** 자동 테스트 밖 **실사용 경로** 증거 확보 (README `[ ]` 해소)

| 순서 | 체크 | 작업 | DEF | 완료 기준 |
|------|------|------|-----|-----------|
| 0-1 | [ ] | `python app.py` → `http://localhost:8080` 기동 | — | 페이지 정상 로드 |
| 0-2 | [ ] | PRD 예시 문장 입력 → 분석 → 부정·배송 통계 확인 | 001,002 | 화면·집계 일치 |
| 0-3 | [ ] | `text` 헤더 CSV 업로드 → 집계·안내 문구 | 006,007,012 | 업로드 N건 메시지 |
| 0-4 | [ ] | 필터(부정+배송) → 다운로드 CSV 내용 | 005,014 | Anchor 문장 포함 |
| 0-5 | [ ] | 빈 다운로드·필터 0건 시 warning UI | 013,014 | warning 표시 스크린샷 |
| 0-6 | [ ] | `report/manual_e2e_phase0.md` 또는 README에 체크일·결과 1줄 기록 | — | Phase 6 발표 증거 |

**Phase 0 Gate:** 0-1~0-5 통과 기록 존재

---

### Phase 1 — 테스트 기반 (약 2시간) ✅ 완료

| 순서 | 체크 | 작업 | DEF |
|------|------|------|-----|
| 1-1 | [x] | Domain Anchor·회귀 6 tests | 001~004 |
| 1-2 | [x] | boundary IT·확장 unit | 010~012 |
| 1-3 | [x] | `pytest --cov-fail-under=90` | 010 |
| 1-4 | [x] | Golden Master baseline·approve | 023 |

**유지보수 (Phase 3~6 공통):**

```bash
cd src/python
pytest tests/ -q
pytest tests/ --cov --cov-fail-under=90 -q
python scripts/generate_golden_master.py --check
```

---

### Phase 2 — 버그·UX (약 1.5시간) ✅ 완료

| 순서 | 체크 | 작업 | DEF |
|------|------|------|-----|
| 2-1 | [x] | B-01~B-02 감정·카테고리 SSOT | 001~004 |
| 2-2 | [x] | B-03~B-06 Session·CSV·로그 UI | 005~008,013,014 |
| 2-3 | [x] | 멀티라인·print 제거 | 009 |

**Phase 2 Gate:** Green Step 0~7 (`green` 브랜치 · `a244a4a`)

---

### Phase 3 — 코드 품질·스멜 (약 2.5시간) ✅ 완료 (`refactor`)

**목표:** 구조 부채·스멜 제거 — **달성** (3-A~3-D). 문서 DEF-020~022는 Phase 6에서 최종 종결.

#### 3-A. 사전 (Phase 6 문서 초안, 20분)

| 순서 | 체크 | 작업 | DEF |
|------|------|------|-----|
| 3-A-1 | [x] | [MOM_TEST.md](MOM_TEST.md) §7: VOC **Partial Go** (Domain·IT 통과 근거) | 020 |
| 3-A-2 | [x] | [MOM_TEST.md](MOM_TEST.md) §8: 자동 4항목 `[x]`, 인터뷰 `[ ]` 유지 | 020 |
| 3-A-3 | [x] | [test_plan.md](test_plan.md): 대상 브랜치 `green`, Gate 39 passed·cov 97% | 021 |

#### 3-B. 설계·문서 (코드 변경 최소, 30분)

| 순서 | 체크 | 작업 | DEF | 완료 기준 |
|------|------|------|-----|-----------|
| 3-B-1 | [x] | PRD/README·[CSV_FORMAT.md](CSV_FORMAT.md): `text` 헤더 권장, 없으면 0열 전체 | 015 | SPEC-CSV-01 |
| 3-B-2 | [x] | [ADR-001](ADR-001-category-main-only.md) main-only **Accepted**, sub Won't fix v1 | 016 | Phase 5 재검토 |
| 3-B-3 | [x] | [CODE_SMELL.md](CODE_SMELL.md) §1.1 Green 해소 표 | 020 | Phase 3-C 잔여 명시 |

#### 3-C. 구현 — Refactor (약 1.5시간)

| 순서 | 체크 | 작업 | DEF | 완료 기준 |
|------|------|------|-----|-----------|
| 3-C-1 | [x] | `global_sent`, `global_kw` 제거 | 018 | grep 0건·테스트 pass |
| 3-C-2 | [x] | `render_page` → `html_renderer.HtmlRenderer` 분리 | 017 | `app.py` ~200줄 감소 |
| 3-C-3 | [x] | `file_handler.py` 삭제 (download는 `Session`/`app`) | 019 | Lava Flow 제거 |
| 3-C-4 | [x] | Logger **UI 토글** (warning/error/info, `/settings/logs`) | 008 | boundary IT |
| 3-C-5 | [x] | `analyze_sentiments` / `analyze_keywords` | S-T01 | Golden Master pass |
| 3-C-6 | [x] | `text_utils.contains_any` | S-T03 | 단일 모듈 |
| 3-C-7 | [x] | `analysis_strategies.py` 전략 패턴 | — | RuleBasedSentiment/Category |

#### 3-D. Phase 3 종료 검증 (15분)

| 순서 | 체크 | 작업 |
|------|------|------|
| 3-D-1 | [x] | `pytest tests/ --cov --cov-fail-under=90` — **50 passed**, cov **97.78%** |
| 3-D-2 | [x] | Golden Master `--check` OK |
| 3-D-3 | [x] | §2 구조·UX DEF 008~019 완료 |

**Phase 3 Gate:** 3-C-1~3-C-7 완료 + 3-D-1~3 pass ✅

---

### Phase 4 — 구조·모델 (선택, 약 2시간)

**DEF 직접 매핑 없음** — README Phase 4·PRD R-07. Phase 3 완료 후 착수 권장.

| 순서 | 체크 | 작업 | 연관 |
|------|------|------|------|
| 4-1 | [x] | `handlers/`, `services/`, `models/` 분리 | R-07 |
| 4-2 | [x] | `services/sentiment.py`, `services/category.py` | 017 연계 |
| 4-3 | [x] | `Feedback` setter·분석 결과 필드 | S-FB01, R-08 |
| 4-4 | [x] | `Session` 인스턴스 + `get_session()` | S-S01 |
| 4-5 | [x] | 회귀 Gate (55 passed, GM `--check`) | 010,023 |

**Phase 4 Gate:** ✅ **55 passed** · cov **97.57%** · Golden Master **OK** (diff 없음, `--force` 불필요)

---

### Phase 5 — 확장 (선택, 약 3시간)

**목표:** Trend·File DB — **DEF-016 구현 여부를 여기서 확정**

| 순서 | 체크 | 작업 | DEF | 비고 |
|------|------|------|-----|------|
| 5-1 | [ ] | Mom Test 인터뷰 3명(선택) → Trend Go/No-Go | §8-5 | No-Go면 5-2~5-4 skip 가능 |
| 5-2 | [ ] | `sample/test_feedback_trend.csv` 추가 | — | |
| 5-3 | [ ] | Trend 시각화 UI | — | |
| 5-4 | [ ] | SQLite 감정 키워드 DB | — | constants 대체 |
| 5-5 | [ ] | **DEF-016:** sub 키워드 매칭 확장 시 analyzer·filter·**Golden Master `--force`** | 016 | 정책이 main-only 유지면 5-5 = 문서만 완료 |

**Phase 5 Gate:** 5-1 결정서 + (Go 시) 5-2~5-4 또는 (No-Go 시) DEF-016 문서 **완료** 처리

---

### Phase 6 — 리뷰·발표·QA 종결 (약 2시간) ★ 최종

**목표:** [project_purpose.md](../project_purpose.md) 8단계 · QA 결함표 **미완료 0건**(또는 의도적 defer 명시)

#### 6-A. 증거 수집·문서 동기화 (40분)

| 순서 | 체크 | 작업 | DEF | 산출물 |
|------|------|------|-----|--------|
| 6-A-1 | [ ] | Phase 0 수동 E2E 결과 `report/` 반영 | — | `manual_e2e_phase0.md` |
| 6-A-2 | [ ] | MOM_TEST §7·§8 최종 판정·체크박스 | 020 | §8 전항목 상태 확정 |
| 6-A-3 | [ ] | test_plan 표지·Gate·브랜치 `green` | 021 | v1.1 등 버전 기록 |
| 6-A-4 | [ ] | README Phase 3~6 체크리스트 ↔ 본 문서 §6 동기화 | 022 | README `[x]` 반영 |
| 6-A-5 | [ ] | PRD §4 알려진 문제 → **해결/잔여** 표 갱신 | 020 | B-01~06 Resolved |

#### 6-B. 팀 리뷰·비교 (50분)

| 순서 | 체크 | 작업 | 산출물 |
|------|------|------|--------|
| 6-B-1 | [ ] | Red vs Green **전/후** 비교 (버그·스멜·테스트 수) | |
| 6-B-2 | [ ] | `report/team_review.md` — 장점 3·단점 3·개선 제안 2 | README Phase 6 |
| 6-B-3 | [ ] | 타 팀 프로젝트 1건 리뷰 (Mom Test 관점) | 동일 파일 § |
| 6-B-4 | [ ] | `defect_list.md` §1 요약: 완료/미완료 건수 **최종 스냅샷** | |

#### 6-C. 자동 검증 최종 런 (15분)

| 순서 | 체크 | 명령 | 기대 |
|------|------|------|------|
| 6-C-1 | [ ] | `pytest tests/ -v` | 39+ passed |
| 6-C-2 | [ ] | `pytest tests/ --cov --cov-fail-under=90` | ≥90% |
| 6-C-3 | [ ] | `python scripts/generate_golden_master.py --check` | OK |
| 6-C-4 | [ ] | (선택) `report/coverage_html` 아카이브 | CI/발표용 |

#### 6-D. 발표 준비 (35분)

| 순서 | 체크 | 작업 |
|------|------|------|
| 6-D-1 | [ ] | 발표 슬라이드 5~7장: 목적·Red→Green·데모·테스트·회고 |
| 6-D-2 | [ ] | 라이브 데모 시나리오 = Phase 0-2 (3분) |
| 6-D-3 | [ ] | Q&A: DEF-016 정책, main-only, Golden Master 워크플로 |
| 6-D-4 | [ ] | `prompt/01.green.md`, `report/01.green.md` (최종 요청사항, 선택) |

#### 6-E. QA 결함 종결 판정

| ID | Phase 6에서 닫는 조건 |
|----|----------------------|
| DEF-008 | 3-C-4 완료 → **완료** |
| DEF-015 | 3-B-1 완료 → **완료** (코드 변경 없을 때) |
| DEF-016 | 3-B-2 + 5-5 또는 defer 문서화 → **완료** 또는 **Won't fix** 명시 |
| DEF-017~019 | 3-C-1~3-C-3 → **완료** |
| DEF-020~022 | 6-A-2~6-A-5 → **완료** / 022는 차트 없으면 부분→완료 승인 가능 |
| §8 인터뷰 | 6-B 또는 5-1 — **선택**, 미수행 시 「교육 범위 제외」기록 |

**Phase 6 Gate (실습 완료 정의):**

- [ ] 6-A-2, 6-A-3, 6-A-5 완료  
- [ ] 6-B-2 팀 리뷰 문서  
- [ ] 6-C-1~6-C-3 pass  
- [ ] 6-D-1 발표 자료  
- [ ] `defect_list.md` §1: **미완료 0** (또는 Won't fix 1表 with 사유)

---

### 6.1 잔여·부분완료 DEF → Phase 참조

| ID | 현재 | Phase 6 종결 조건 |
|----|------|-------------------|
| DEF-008~019 | **완료** | — |
| DEF-015, 016 | **완료** | CSV_FORMAT · ADR-001 |
| DEF-020 | **부분완료** | MOM_TEST §8 인터뷰 · §7 최종 (6-A-2) |
| DEF-021 | **부분완료** | test_plan `refactor` Gate 50 tests (6-A-3) |
| DEF-022 | **부분완료** | README Phase 4~6·차트 정책 (6-A-4) |

**`refactor` 주요 커밋:** `CSV 규칙·main-only 정책 문서` → `global_sent, global_kw 제거` → `render_page 분리` → `file_handler 제거` → `Logger UI 토글` → `contains_any 공통 유틸` → `분석 전략 패턴 적용` → `sent/kw 네이밍 개선`

---

## 7. 변경 이력

| 일자 | 변경 |
|------|------|
| 2026-05-22 | 초안 — Red 발견 8건(Green 완료 7·부분 1), QA 잔여 14건 등록 |
| 2026-05-22 | Step 6 — DEF-010~014 완료, cov 97.42%, **예정 Phase** 컬럼 추가 |
| 2026-05-22 | Golden Master DEF-023, README·defect_list 진행사항 동기화 (39 tests) |
| 2026-05-22 | §6 Phase 0~6 작업 순서 체크리스트 세분화 (Phase 6 Gate) |
| 2026-05-22 | Phase 3-A — MOM_TEST v1.1 Partial Go, test_plan v1.1 Green Gate, DEF-020/021 부분완료 |
| 2026-05-22 | Phase 3-B — CSV_FORMAT, ADR-001 main-only, PRD v1.1, DEF-015/016 완료 |
| 2026-05-22 | Phase 3-C-2 — `html_renderer.py`, DEF-017 완료 |
| 2026-05-22 | Phase 3-C-3 — `file_handler.py` 삭제, DEF-019 완료 |
| 2026-05-22 | Phase 3-C-4 — Logger UI 토글, DEF-008 완료 |
| 2026-05-22 | Phase 3-C-5~7 — 네이밍·text_utils·전략패턴, 3-D Gate |
| 2026-05-22 | §1·§5·§6·README 진행사항 동기화 — 50 passed, Phase 3 ✅ |
