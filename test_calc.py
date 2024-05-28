import calc
import pytest


def test_parce_cli_input():
    with pytest.raises(SystemExit):
        calc.parce_cli_input()


def test_get_time_to_win():
    assert round(calc.get_time_to_win(10, 1000000), 2) == 584.74
    assert round(calc.get_time_to_win(50, 1000000), 2) == 126.95


def test_get_power_price():
    assert calc.get_power_price(500, 0.1, 1) == 50
    assert calc.get_power_price(200, 0.3, 2) == 120


def test_get_profitability():
    assert calc.get_profitability(100, 99, 1, 1) == 1
    assert calc.get_profitability(30, 30, 240, 24 * 30) == 0
    assert calc.get_profitability(30, 20, 240, 24 * 30) == 30
    assert calc.get_profitability(30, 40, 240, 24 * 30) == -30


def test_get_power_price_threshold():
    assert calc.get_power_price_threshold(100, 100, 1) == 1
    assert calc.get_power_price_threshold(1, 100, 1) == 0.01


def test_get_blockchain_size():
    assert calc.get_blockchain_size() > 0


def test_get_chia_price():
    assert calc.get_chia_price() > 0
