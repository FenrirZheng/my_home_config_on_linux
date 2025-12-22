"""Tests for BigRoad"""

import pytest
from src.big_road import BigRoad


class TestBigRoad:
    """大路測試"""

    def test_empty_road(self):
        """測試空路"""
        road = BigRoad()
        assert road.get_column_count() == 0
        assert road.get_last_result() is None

    def test_single_result(self):
        """測試單一結果"""
        road = BigRoad()
        road.add_result('B')
        assert road.get_column_count() == 1
        assert road.get_last_result() == 'B'
        assert road.get_column_lengths() == [1]

    def test_same_results_same_column(self):
        """測試相同結果在同一列"""
        road = BigRoad()
        road.add_results('BBB')
        assert road.get_column_count() == 1
        assert road.get_column_lengths() == [3]

    def test_different_results_new_column(self):
        """測試不同結果換新列"""
        road = BigRoad()
        road.add_results('BP')
        assert road.get_column_count() == 2
        assert road.get_column_lengths() == [1, 1]

    def test_alternating_results(self):
        """測試交替結果"""
        road = BigRoad()
        road.add_results('BPBPBP')
        assert road.get_column_count() == 6
        assert road.get_column_lengths() == [1, 1, 1, 1, 1, 1]

    def test_streaks(self):
        """測試連續相同結果"""
        road = BigRoad()
        road.add_results('BBBPPBB')
        assert road.get_column_count() == 3
        assert road.get_column_lengths() == [3, 2, 2]

    def test_ignore_tie(self):
        """測試忽略和局"""
        road = BigRoad()
        road.add_results('BTBTP')
        assert road.get_column_count() == 2
        assert road.get_column_lengths() == [2, 1]

    def test_dragon_tail(self):
        """測試龍尾（超過6行）"""
        road = BigRoad(max_rows=6)
        road.add_results('BBBBBBBB')  # 8 bankers
        assert road.get_column_count() == 1
        # First 6 go in column 0, rows 0-5
        # 7th goes to column 1, row 5 (dragon tail)
        # 8th goes to column 2, row 5 (dragon tail continues)
        positions = road.positions
        assert positions[0] == (0, 0)
        assert positions[5] == (0, 5)
        assert positions[6] == (1, 5)  # Dragon tail starts
        assert positions[7] == (2, 5)  # Dragon tail continues

    def test_get_grid(self):
        """測試網格輸出"""
        road = BigRoad()
        road.add_results('BBPP')
        grid = road.get_grid(max_cols=4)

        assert grid[0][0] == 'B'
        assert grid[1][0] == 'B'
        assert grid[0][1] == 'P'
        assert grid[1][1] == 'P'
        assert grid[2][0] is None

    def test_clone(self):
        """測試複製功能"""
        road = BigRoad()
        road.add_results('BBP')

        cloned = road.clone()
        cloned.add_result('P')

        assert road.get_column_lengths() == [2, 1]
        assert cloned.get_column_lengths() == [2, 2]

    def test_get_column_result(self):
        """測試取得列結果類型"""
        road = BigRoad()
        road.add_results('BBPPP')

        assert road.get_column_result(0) == 'B'
        assert road.get_column_result(1) == 'P'
        assert road.get_column_result(2) is None
