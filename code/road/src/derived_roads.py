"""
衍生路 - 大眼仔路、小路、曱甴路

計算規則基於大路的結構來判斷紅藍:
- 紅 (red): 齊整/有路
- 藍 (blue): 不齊整/無路

換列判斷（新開一列時）:
- 比較前一列與參照列的長度是否相同
- 相同 = 紅，不同 = 藍

直落判斷（同列繼續時）:
- 檢查參照列在對應位置是否有結果
- 有 = 紅，無 = 藍
"""

from typing import Optional
from .big_road import BigRoad


class DerivedRoad:
    """衍生路基礎類別"""

    def __init__(self, start_col: int, compare_distance: int):
        """
        start_col: 從大路第幾列開始計算（0-indexed）
        compare_distance: 比較的距離（大眼仔=1, 小路=2, 曱甴路=3）
        """
        self.start_col = start_col
        self.compare_distance = compare_distance
        self.results: list[str] = []  # 'red' or 'blue'

    def calculate(self, big_road: BigRoad) -> list[str]:
        """根據大路計算衍生路結果"""
        self.results = []
        col_lengths = big_road.get_column_lengths()
        num_cols = len(col_lengths)

        if num_cols < self.start_col + 1:
            return self.results

        # Iterate through each position in the big road starting from start_col
        for col_idx in range(self.start_col, num_cols):
            col_len = col_lengths[col_idx]

            for row_idx in range(col_len):
                # Skip positions before the starting point
                if col_idx == self.start_col and row_idx == 0:
                    continue

                result = self._calculate_point(col_idx, row_idx, col_lengths)
                if result:
                    self.results.append(result)

        return self.results

    def _calculate_point(
        self, col_idx: int, row_idx: int, col_lengths: list[int]
    ) -> Optional[str]:
        """計算單一點的顏色"""
        compare_col = col_idx - self.compare_distance

        if compare_col < 0:
            return None

        if row_idx == 0:
            # 換列判斷：比較前一列與參照列的長度
            prev_col = col_idx - 1
            prev_prev_col = prev_col - self.compare_distance

            if prev_prev_col < 0:
                return None

            prev_len = col_lengths[prev_col]
            prev_prev_len = col_lengths[prev_prev_col]

            return 'red' if prev_len == prev_prev_len else 'blue'
        else:
            # 直落判斷：檢查參照列在對應行是否有結果
            compare_len = col_lengths[compare_col]
            # 對應位置是 row_idx（當前行數）
            has_result = compare_len > row_idx

            return 'red' if has_result else 'blue'

    def get_grid(self, max_cols: int = 30, max_rows: int = 6) -> list[list[Optional[str]]]:
        """
        取得二維網格表示（衍生路的排列方式）
        衍生路採用先下後右的排列方式
        """
        grid = [[None for _ in range(max_cols)] for _ in range(max_rows)]

        col = 0
        row = 0

        for result in self.results:
            if row >= max_rows:
                col += 1
                row = 0

            if col >= max_cols:
                break

            grid[row][col] = result
            row += 1

        return grid


class BigEyeRoad(DerivedRoad):
    """大眼仔路 - 從大路第2列第2行開始，比較距離為1"""

    def __init__(self):
        super().__init__(start_col=1, compare_distance=1)


class SmallRoad(DerivedRoad):
    """小路 - 從大路第3列第2行開始，比較距離為2"""

    def __init__(self):
        super().__init__(start_col=2, compare_distance=2)


class CockroachRoad(DerivedRoad):
    """曱甴路 - 從大路第4列第2行開始，比較距離為3"""

    def __init__(self):
        super().__init__(start_col=3, compare_distance=3)
