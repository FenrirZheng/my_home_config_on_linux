"""Tests for Derived Roads"""

import pytest
from src.big_road import BigRoad
from src.derived_roads import BigEyeRoad, SmallRoad, CockroachRoad


class TestBigEyeRoad:
    """大眼仔路測試"""

    def test_empty_with_insufficient_data(self):
        """測試資料不足時為空"""
        big_road = BigRoad()
        big_road.add_results('B')

        eye_road = BigEyeRoad()
        results = eye_road.calculate(big_road)

        assert results == []

    def test_starts_from_col2_row2(self):
        """測試從第2列第2行開始"""
        big_road = BigRoad()
        # Column 0: B, Column 1: P (first entry in col 1 doesn't generate)
        big_road.add_results('BP')

        eye_road = BigEyeRoad()
        results = eye_road.calculate(big_road)

        # No result yet - need col 1, row 1 or col 2
        assert results == []

    def test_column_change_equal_length(self):
        """測試換列時長度相同 = 紅"""
        big_road = BigRoad()
        # Col 0: B, Col 1: P, Col 2: B
        # When entering col 2, compare col 1 (len=1) with col 0 (len=1) -> equal -> red
        big_road.add_results('BPB')

        eye_road = BigEyeRoad()
        results = eye_road.calculate(big_road)

        assert 'red' in results

    def test_column_change_different_length(self):
        """測試換列時長度不同 = 藍"""
        big_road = BigRoad()
        # Col 0: BB, Col 1: P, Col 2: B
        # When entering col 2, compare col 1 (len=1) with col 0 (len=2) -> not equal -> blue
        big_road.add_results('BBPB')

        eye_road = BigEyeRoad()
        results = eye_road.calculate(big_road)

        assert 'blue' in results

    def test_same_column_with_result(self):
        """測試直落時有對應結果 = 紅"""
        big_road = BigRoad()
        # Col 0: BB, Col 1: PP
        # At col 1 row 1, check if col 0 has row 1 -> yes -> red
        big_road.add_results('BBPP')

        eye_road = BigEyeRoad()
        results = eye_road.calculate(big_road)

        assert 'red' in results

    def test_same_column_without_result(self):
        """測試直落時無對應結果 = 藍"""
        big_road = BigRoad()
        # Col 0: B, Col 1: PP
        # At col 1 row 1, check if col 0 has row 1 -> no -> blue
        big_road.add_results('BPP')

        eye_road = BigEyeRoad()
        results = eye_road.calculate(big_road)

        assert 'blue' in results


class TestSmallRoad:
    """小路測試"""

    def test_empty_with_insufficient_data(self):
        """測試資料不足時為空"""
        big_road = BigRoad()
        big_road.add_results('BP')

        small_road = SmallRoad()
        results = small_road.calculate(big_road)

        assert results == []

    def test_starts_from_col3_row2(self):
        """測試從第3列第2行開始（需要至少3列）"""
        big_road = BigRoad()
        # Need at least 3 columns
        big_road.add_results('BPB')

        small_road = SmallRoad()
        results = small_road.calculate(big_road)

        # Still not enough - need entry in col 2, row 1 or col 3
        assert results == []

    def test_compares_with_col_minus_2(self):
        """測試與前2列比較"""
        big_road = BigRoad()
        # Col 0: B, Col 1: P, Col 2: B, Col 3: P
        # When entering col 3, compare col 2 (len=1) with col 0 (len=1) -> equal -> red
        big_road.add_results('BPBP')

        small_road = SmallRoad()
        results = small_road.calculate(big_road)

        assert 'red' in results


class TestCockroachRoad:
    """曱甴路測試"""

    def test_empty_with_insufficient_data(self):
        """測試資料不足時為空"""
        big_road = BigRoad()
        big_road.add_results('BPB')

        cockroach_road = CockroachRoad()
        results = cockroach_road.calculate(big_road)

        assert results == []

    def test_starts_from_col4_row2(self):
        """測試從第4列第2行開始（需要至少4列）"""
        big_road = BigRoad()
        big_road.add_results('BPBP')

        cockroach_road = CockroachRoad()
        results = cockroach_road.calculate(big_road)

        # Still not enough - need entry in col 3, row 1 or col 4
        assert results == []

    def test_compares_with_col_minus_3(self):
        """測試與前3列比較"""
        big_road = BigRoad()
        # Col 0: B, Col 1: P, Col 2: B, Col 3: P, Col 4: B
        # When entering col 4, compare col 3 (len=1) with col 0 (len=1) -> equal -> red
        big_road.add_results('BPBPB')

        cockroach_road = CockroachRoad()
        results = cockroach_road.calculate(big_road)

        assert 'red' in results
