# -*- coding: utf-8 -*-
"""
Golden Master regression (Approval pattern).

Baseline: tests/golden_master_expected.txt (version controlled).
Regenerate: python scripts/generate_golden_master.py [--force]
"""
import pytest

from tests.golden_master import approve_golden_master
from tests.golden_master_capture import capture_golden_master_output


@pytest.mark.p0
@pytest.mark.domain
class TestGoldenMasterApproval:
    def test_domain_output_matches_golden_master(self):
        actual = capture_golden_master_output()
        approve_golden_master(actual)
