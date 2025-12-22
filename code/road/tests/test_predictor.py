"""Tests for Predictor"""

import pytest
from src.predictor import Predictor


class TestPredictor:
    """問路預測器測試"""

    def test_empty_predictor(self):
        """測試空預測器"""
        predictor = Predictor()
        result = predictor.ask()

        assert result['if_banker']['big_eye'] is None
        assert result['if_banker']['small'] is None
        assert result['if_banker']['cockroach'] is None

    def test_add_single_result(self):
        """測試加入單一結果"""
        predictor = Predictor()
        predictor.add_result('B')

        assert predictor.get_big_road().get_column_count() == 1

    def test_add_multiple_results(self):
        """測試加入多個結果"""
        predictor = Predictor()
        predictor.add_results('BBPPP')

        assert predictor.get_big_road().get_column_count() == 2
        assert predictor.get_big_road().get_column_lengths() == [2, 3]

    def test_ask_with_enough_data(self):
        """測試有足夠資料時的問路"""
        predictor = Predictor()
        predictor.add_results('BPBP')  # 4 columns

        result = predictor.ask()

        # Should have predictions for at least big_eye
        # The actual values depend on the algorithm
        assert 'if_banker' in result
        assert 'if_player' in result

    def test_ask_returns_different_predictions(self):
        """測試莊問和閒問可能有不同結果"""
        predictor = Predictor()
        predictor.add_results('BBPP')

        result = predictor.ask()

        # Both should have predictions
        assert 'big_eye' in result['if_banker']
        assert 'big_eye' in result['if_player']

    def test_prediction_values(self):
        """測試預測值只能是 red, blue, 或 None"""
        predictor = Predictor()
        predictor.add_results('BPBPBPBP')

        result = predictor.ask()

        for scenario in ['if_banker', 'if_player']:
            for road in ['big_eye', 'small', 'cockroach']:
                value = result[scenario][road]
                assert value in ('red', 'blue', None)

    def test_get_roads(self):
        """測試取得各路紙"""
        predictor = Predictor()
        predictor.add_results('BBPP')

        assert predictor.get_big_road() is not None
        assert predictor.get_big_eye_road() is not None
        assert predictor.get_small_road() is not None
        assert predictor.get_cockroach_road() is not None
