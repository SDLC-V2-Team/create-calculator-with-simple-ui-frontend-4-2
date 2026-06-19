import pytest
from calculator_logic import CalculatorLogic


def test_perform_addition():
    result = CalculatorLogic.perform(3.0, 4.0, '+')
    assert result == 7.0


def test_perform_subtraction():
    result = CalculatorLogic.perform(10.0, 3.5, '-')
    assert result == pytest.approx(6.5)


def test_perform_multiplication():
    result = CalculatorLogic.perform(2.5, 4.0, '*')
    assert result == pytest.approx(10.0)


def test_perform_division():
    result = CalculatorLogic.perform(9.0, 3.0, '/')
    assert result == pytest.approx(3.0)


def test_perform_division_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        CalculatorLogic.perform(5.0, 0.0, '/')


def test_perform_unsupported_operator_raises():
    with pytest.raises(ValueError, match="Unsupported operator"):
        CalculatorLogic.perform(1.0, 2.0, '%')