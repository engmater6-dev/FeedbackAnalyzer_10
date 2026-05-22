# Golden Master (Approval) 전략

## 기준 파일

| 항목 | 경로 |
|------|------|
| **Baseline (버전 관리 필수)** | `tests/golden_master_expected.txt` |
| **스냅샷 생성 로직** | `tests/golden_master_capture.py` |
| **Approve 비교** | `tests/golden_master.py` → `approve_golden_master()` |
| **pytest** | `tests/domain/test_golden_master.py` |
| **CLI 생성/갱신** | `scripts/generate_golden_master.py` |

## Approve 패턴

1. **기준 파일 없음** → 현재 출력을 `golden_master_expected.txt`에 저장 후 테스트 **FAIL** (리뷰·`git add` 유도).
2. **기준 파일 있음** → `actual` vs `expected` **문자열 전체 비교**.
3. **불일치** → `unified_diff` 출력 후 테스트 **FAIL**.

## 워크플로

```bash
cd src/python

# 최초 생성 (또는 의도적 변경 후 갱신)
python scripts/generate_golden_master.py
# 또는 기존 덮어쓰기
python scripts/generate_golden_master.py --force

git add tests/golden_master_expected.txt

# 회귀 검증
pytest tests/domain/test_golden_master.py -v
python scripts/generate_golden_master.py --check
```

## 스냅샷 범위

- PRD Anchor 문장 (감정·키워드·필터)
- 중립 3건 회귀
- 카테고리 `품질` main-only

HTTP/타임스탬프는 제외 (Domain 결정론 출력만).
