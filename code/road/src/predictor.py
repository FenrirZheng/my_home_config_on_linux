"""
問路預測器

問路邏輯:
- 假設下一局開莊，計算各衍生路會顯示什麼顏色
- 假設下一局開閒，計算各衍生路會顯示什麼顏色
"""

from typing import Optional
from .big_road import BigRoad
from .derived_roads import BigEyeRoad, SmallRoad, CockroachRoad, DerivedRoad


class Predictor:
    """問路預測器"""

    def __init__(self):
        self.big_road = BigRoad()
        self.big_eye_road = BigEyeRoad()
        self.small_road = SmallRoad()
        self.cockroach_road = CockroachRoad()

    def add_result(self, result: str) -> None:
        """加入一局結果"""
        self.big_road.add_result(result)
        self._recalculate_derived_roads()

    def add_results(self, results: str) -> None:
        """批量加入結果"""
        for r in results:
            if r in ('B', 'P'):
                self.big_road.add_result(r)
        self._recalculate_derived_roads()

    def _recalculate_derived_roads(self) -> None:
        """重新計算所有衍生路"""
        self.big_eye_road.calculate(self.big_road)
        self.small_road.calculate(self.big_road)
        self.cockroach_road.calculate(self.big_road)

    def _get_next_color(
        self, road: DerivedRoad, big_road: BigRoad, assume_result: str
    ) -> Optional[str]:
        """
        取得假設結果後，該衍生路會產生的下一個顏色
        """
        # Clone the big road and add assumed result
        test_road = big_road.clone()
        test_road.add_result(assume_result)

        # Calculate derived road for test scenario
        test_derived = type(road)()  # Create new instance of same type
        test_derived.calculate(test_road)

        # Get the original results count
        original_count = len(road.results)
        new_results = test_derived.results

        # If new results has more items, return the new one
        if len(new_results) > original_count:
            return new_results[-1]

        return None

    def ask(self) -> dict:
        """
        問路 - 預測下一局莊贏或閒贏時各路的顯示

        回傳:
        {
            'if_banker': {
                'big_eye': 'red' | 'blue' | None,
                'small': 'red' | 'blue' | None,
                'cockroach': 'red' | 'blue' | None
            },
            'if_player': {
                'big_eye': 'red' | 'blue' | None,
                'small': 'red' | 'blue' | None,
                'cockroach': 'red' | 'blue' | None
            }
        }
        """
        result = {
            'if_banker': {
                'big_eye': self._get_next_color(
                    self.big_eye_road, self.big_road, 'B'
                ),
                'small': self._get_next_color(
                    self.small_road, self.big_road, 'B'
                ),
                'cockroach': self._get_next_color(
                    self.cockroach_road, self.big_road, 'B'
                ),
            },
            'if_player': {
                'big_eye': self._get_next_color(
                    self.big_eye_road, self.big_road, 'P'
                ),
                'small': self._get_next_color(
                    self.small_road, self.big_road, 'P'
                ),
                'cockroach': self._get_next_color(
                    self.cockroach_road, self.big_road, 'P'
                ),
            },
        }
        return result

    def get_big_road(self) -> BigRoad:
        """取得大路"""
        return self.big_road

    def get_big_eye_road(self) -> BigEyeRoad:
        """取得大眼仔路"""
        return self.big_eye_road

    def get_small_road(self) -> SmallRoad:
        """取得小路"""
        return self.small_road

    def get_cockroach_road(self) -> CockroachRoad:
        """取得曱甴路"""
        return self.cockroach_road
