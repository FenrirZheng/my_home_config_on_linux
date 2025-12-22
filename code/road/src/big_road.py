"""
大路 (Big Road) - 百家樂主路紙

記錄規則:
- 同結果往下排（同一列）
- 不同結果換新列
- 超過6行則「龍尾」右移（保持在第6行往右延伸）
"""

from typing import Optional


class BigRoad:
    """大路類別 - 記錄百家樂開牌結果"""

    def __init__(self, max_rows: int = 6):
        self.max_rows = max_rows
        # columns: list of columns, each column is a list of results
        # e.g., [['B', 'B', 'B'], ['P', 'P'], ['B']]
        self.columns: list[list[str]] = []
        # For dragon tail tracking: (col_index, row_index) for each entry
        self.positions: list[tuple[int, int]] = []

    def add_result(self, result: str) -> None:
        """加入一局結果 (B=莊, P=閒)，T=和會被忽略"""
        if result not in ('B', 'P'):
            return

        if not self.columns:
            # First result
            self.columns.append([result])
            self.positions.append((0, 0))
            return

        last_col = self.columns[-1]
        last_result = last_col[0]  # All results in a column are the same

        if result == last_result:
            # Same result - continue in same logical column (streak)
            col_idx = len(self.columns) - 1
            row_idx = len(last_col)

            # Add to logical column (for derived road calculation)
            last_col.append(result)

            if row_idx < self.max_rows:
                # Normal case - visual position matches logical
                self.positions.append((col_idx, row_idx))
            else:
                # Dragon tail - visual position moves right, stays at bottom row
                # Find last position's column and move right
                last_pos = self.positions[-1]
                dragon_col = last_pos[0] + 1
                # Check if position is occupied
                while self._is_position_occupied(dragon_col, self.max_rows - 1):
                    dragon_col += 1
                self.positions.append((dragon_col, self.max_rows - 1))
        else:
            # Different result - start new column
            self.columns.append([result])
            self.positions.append((len(self.columns) - 1, 0))

    def _is_position_occupied(self, col: int, row: int) -> bool:
        """檢查指定位置是否已被佔用"""
        return (col, row) in self.positions

    def add_results(self, results: str) -> None:
        """批量加入結果字串"""
        for r in results:
            self.add_result(r)

    def get_grid(self, max_cols: int = 60) -> list[list[Optional[str]]]:
        """
        取得二維網格表示
        回傳: max_rows x max_cols 的網格，空位為 None
        """
        grid = [[None for _ in range(max_cols)] for _ in range(self.max_rows)]

        for pos, col_data in zip(self.positions, self._flatten_results()):
            col_idx, row_idx = pos
            if col_idx < max_cols and row_idx < self.max_rows:
                grid[row_idx][col_idx] = col_data

        return grid

    def _flatten_results(self) -> list[str]:
        """將所有結果展平成一維列表"""
        results = []
        for col in self.columns:
            results.extend(col)
        return results

    def get_column_lengths(self) -> list[int]:
        """
        取得每列的長度（用於衍生路計算）
        注意：這裡的長度是邏輯長度，不考慮龍尾
        """
        return [len(col) for col in self.columns]

    def get_column_count(self) -> int:
        """取得列數"""
        return len(self.columns)

    def get_last_result(self) -> Optional[str]:
        """取得最後一個結果"""
        if not self.columns:
            return None
        return self.columns[-1][0]

    def get_column_result(self, col_idx: int) -> Optional[str]:
        """取得指定列的結果類型（B 或 P）"""
        if 0 <= col_idx < len(self.columns) and self.columns[col_idx]:
            return self.columns[col_idx][0]
        return None

    def get_column_length(self, col_idx: int) -> int:
        """取得指定列的長度"""
        if 0 <= col_idx < len(self.columns):
            return len(self.columns[col_idx])
        return 0

    def clone(self) -> 'BigRoad':
        """複製當前大路狀態"""
        new_road = BigRoad(self.max_rows)
        new_road.columns = [col.copy() for col in self.columns]
        new_road.positions = self.positions.copy()
        return new_road
