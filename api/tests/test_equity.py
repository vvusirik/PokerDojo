import numpy as np
import pytest
from utils.equity import (
    hand_range_vs_random_equity,
    hand_vs_hand_equity,
    hand_vs_random_equity_heatmap,
    hand_vs_random_hand_equity,
    hand_vs_range_equity,
    hand_vs_range_equity_heatmap,
)


@pytest.mark.parametrize(
    "hand_str, expected_equity", [("AsAc", 0.85), ("KsKc", 0.82), ("QsQc", 0.80)]
)
def test_hand_vs_random_hand_equity(hand_str: str, expected_equity: float):
    equity = hand_vs_random_hand_equity(hand_str)
    assert equity == pytest.approx(expected_equity, abs=0.01)


@pytest.mark.parametrize(
    "hero_hand, villain_hand, expected_equity", [("AsAc", "AhAd", 0.5)]
)
def test_hand_vs_hand_equity(hero_hand: str, villain_hand: str, expected_equity: float):
    equity = hand_vs_hand_equity(hero_hand, villain_hand)
    assert equity == pytest.approx(expected_equity, abs=0.01)


@pytest.mark.parametrize(
    "hand_str, range_str, expected_equity",
    [("AsAc", "AA", 0.5), ("KsKc", "KK", 0.5), ("AsAc", "22+", 0.81)],
)
def test_hand_vs_range_equity(hand_str: str, range_str: str, expected_equity: float):
    equity = hand_vs_range_equity(hand_str, range_str)
    assert equity == pytest.approx(expected_equity, abs=0.01)


@pytest.mark.parametrize(
    "range_str, expected_equity", [("AA", 0.85), ("AKs", 0.67), ("22+", 0.69)]
)
def test_hand_range_vs_random_equity(range_str: str, expected_equity: float):
    equity = hand_range_vs_random_equity(range_str)
    assert equity == pytest.approx(expected_equity, abs=0.01)


@pytest.mark.slow
def test_generate_equity_heatmap():
    equity_heatmap = hand_vs_random_equity_heatmap()
    equity_heatmap = np.array(equity_heatmap.values())
    assert (equity_heatmap < 1).all()
    assert (equity_heatmap > 0).all()


@pytest.mark.slow
@pytest.mark.parametrize(
    "hand",
    ["AcAs", "KcTh", "2h7d"],
)
def test_generate_hand_vs_range_equity_heatmap(hand: str):
    equity_heatmap = hand_vs_range_equity_heatmap(hand)
    equity_heatmap = np.array(equity_heatmap.values())
    assert (equity_heatmap < 1).all()
    assert (equity_heatmap > 0).all()
