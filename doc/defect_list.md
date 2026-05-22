# 결함 목록 (Defect List)

| 항목 | 내용 |
|------|------|
| 문서 ID | QA-DEF-01 |
| 작성 | QA 리드 |
| 일자 | 2026-05-22 |
| 대상 브랜치 | `green` |
| 근거 | Red 재현 · Green 수정 · QA 분석(`doc/`, `README.md`, `src/`) |
| 관련 | [PRD.md](PRD.md) §4, [CODE_SMELL.md](CODE_SMELL.md), [test_plan.md](test_plan.md), [MOM_TEST.md](MOM_TEST.md) |

---

## 1. 요약

| 구분 | 건수 |
|------|------|
| **전체** | 22 |
| **완료** | 14 |
| **부분완료** | 2 |
| **미완료** | 6 |

| Severity | 완료 | 미완료·부분 |
|----------|------|-------------|
| Critical / High | 4 | 2 |
| Medium | 7 | 2 |
| Low | 3 | 2 |

> **Step 6 (2026-05-22):** DEF-010~014 완료 · cov **97.42%** · IT 8건 추가

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
| DEF-008 | Low | UX | Phase 3 | warning/error UI | level별 on/off | stdout만 | Logger UI 없음 | `get_page_logs`, flags | **부분완료** — UI 토글·INFO 없음 |
| DEF-009 | Low | UX | Green Step 4 | `filter_feedbacks` | stdout 미출력 | `print` | 디버그 | print 제거 | **완료** |
| DEF-010 | Medium | 테스트결함 | **Green Step 6** | `pytest --cov` | ≥90% | ~39% | IT·app 미측정 | 38 tests, cov **97.42%** | **완료** |
| DEF-011 | Medium | 테스트결함 | **Green Step 6** | boundary IT | HTTP 검증 | skip | IT 미착수 | IT-01~04 구현 | **완료** |
| DEF-012 | Medium | 테스트결함 | **Green Step 6** | CSV `text` E2E | upload IT Pass | 없음 | IT 없음 | `test_post_upload_text_header_csv` | **완료** |
| DEF-013 | Low | UX | **Green Step 6** | 연속 요청 로그 | 요청별만 | 누적 | 버퍼 미클리어 | `_begin_page_request()` | **완료** |
| DEF-014 | Low | UX | **Green Step 6** | 빈 `/download` | 안내 | 빈 CSV | 빈 목록 허용 | warning + 버튼 조건 | **완료** |
| DEF-015 | Medium | 기능결함 | Phase 3/문서 | CSV 헤더 없음 0열 | 명시적 규칙 | 레거시 0열 | 휴리스틱 없음 | `test_csv_parse`·문서 명시 | **부분완료** |
| DEF-016 | Medium | 기능결함 | Phase 3/문서 | `"택배만"` 본문 | 배송 1건? | 0건 | main-only 설계 | 문서화 또는 sub 확장 | **미완료** |
| DEF-017 | High | 구조/기술부채 | Phase 3 | `render_page` | 분리 | God Function | S-A01 | 템플릿 분리 | **미완료** |
| DEF-018 | High | 구조/기술부채 | Phase 3 | `global_sent/kw` | 인스턴스 상태 | 클래스 변수 | S-T02 | DTO·전역 제거 | **미완료** |
| DEF-019 | Medium | 구조/기술부채 | Phase 3 | `file_handler.py` | 사용/삭제 | Lava Flow | S-FH01 | 삭제 또는 연동 | **미완료** |
| DEF-020 | Medium | 문서 | Phase 3/6 | MOM_TEST §7~8 | Partial Go | Fail | 미갱신 | §8·§7 갱신 | **미완료** |
| DEF-021 | Low | 문서 | Phase 3/6 | test_plan 메타 | `green` | `red` | 미갱신 | 표지·Gate 갱신 | **미완료** |
| DEF-022 | Low | 문서 | Phase 3/6 | README 기능 문구 | 건수 요약 | 시각화 과장 | 가설 괴리 | 문구 완화 | **미완료** |

---

## 3. PRD 버그 ID 매핑

| PRD | Defect ID | 완료 여부 |
|-----|-----------|-----------|
| B-01 | DEF-001, DEF-002, DEF-003 | 완료 |
| B-02 | DEF-004 | 완료 |
| B-03 | DEF-005 | 완료 |
| B-04 | DEF-006, DEF-015(잔여 엣지) | 완료 / DEF-015 미완료 |
| B-05 | DEF-007 | 완료 |
| B-06 | DEF-008 | 부분완료 |

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

## 5. 권장 처리 순서 (미완료)

| 순위 | ID | 예정 Phase | 작업 |
|------|-----|------------|------|
| 1 | DEF-020, DEF-021, DEF-022 | Phase 3/6 | doc 동기화 |
| 2 | DEF-015, DEF-016 | Phase 3/문서 | CSV·main-only 설계 문서화 |
| 3 | DEF-008 | Phase 3 | 로그 level UI 토글 |
| 4 | DEF-017~DEF-019 | Phase 3 | Refactor·Lava Flow |
| — | Phase 0 | — | `python app.py` 수동 E2E (README `[ ]`) |

---

## 6. 변경 이력

| 일자 | 변경 |
|------|------|
| 2026-05-22 | 초안 — Red 발견 8건(Green 완료 7·부분 1), QA 잔여 14건 등록 |
| 2026-05-22 | Step 6 — DEF-010~014 완료, cov 97.42%, **예정 Phase** 컬럼 추가 |
