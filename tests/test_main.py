import tkinter as tk
import pytest
from unittest.mock import patch, MagicMock

# Ensure calculator_logic is importable (mock if not present)
import sys
import types

# Provide a minimal calculator_logic stub if the real module isn't available
if "calculator_logic" not in sys.modules:
    mock_module = types.ModuleType("calculator_logic")

    class CalculatorLogic:
        def perform(self, a, b, op):
            if op == "+":
                return a + b
            elif op == "-":
                return a - b
            elif op == "*":
                return a * b
            elif op == "/":
                if b == 0:
                    raise ZeroDivisionError("division by zero")
                return a / b
            raise ValueError(f"Unknown operator: {op}")

    mock_module.CalculatorLogic = CalculatorLogic
    sys.modules["calculator_logic"] = mock_module

from main import CalculatorApp


@pytest.fixture
def app(tmp_path):
    """Create a CalculatorApp instance with a Tk root for testing."""
    root = tk.Tk()
    root.withdraw()  # Don't show the window during tests
    calculator = CalculatorApp(root)
    yield calculator
    root.destroy()


class TestDigitInput:
    def test_single_digit_updates_display(self, app):
        """Happy path: pressing a digit updates current_input and display."""
        app._digit_or_decimal("5")
        assert app.current_input == "5"
        assert app.display_var.get() == "5"

    def test_multiple_digits_concatenate(self, app):
        """Happy path: pressing multiple digits concatenates them."""
        for ch in ["1", "2", "3"]:
            app._digit_or_decimal(ch)
        assert app.current_input == "123"
        assert app.display_var.get() == "123"


class TestDecimalInput:
    def test_decimal_allowed_once(self, app):
        """Edge case: a second decimal point is ignored."""
        app._digit_or_decimal("3")
        app._digit_or_decimal(".")
        app._digit_or_decimal("1")
        app._digit_or_decimal(".")  # should be ignored
        app._digit_or_decimal("4")
        assert app.current_input == "3.14"
        assert app.display_var.get() == "3.14"


class TestOperatorAndEvaluate:
    def test_addition_result(self, app):
        """Happy path: 3 + 4 = 7."""
        app._digit_or_decimal("3")
        app._operator("+")
        app._digit_or_decimal("4")
        app._evaluate()
        assert app.display_var.get() == "7.0"
        assert app.current_input == ""
        assert app.operation is None

    def test_clear_resets_state(self, app):
        """Happy path: clear resets all state and display."""
        app._digit_or_decimal("9")
        app._operator("*")
        app._digit_or_decimal("2")
        app._clear()
        assert app.current_input == ""
        assert app.operation is None
        assert app.prev_value is None
        assert app.display_var.get() == "0"


class TestBackspace:
    def test_backspace_removes_last_char(self, app):
        """Edge case: backspace removes the last character."""
        app._digit_or_decimal("4")
        app._digit_or_decimal("2")
        app._backspace()
        assert app.current_input == "4"
        assert app.display_var.get() == "4"

    def test_backspace_on_empty_shows_zero(self, app):
        """Edge case: backspace on empty input shows '0' on display."""
        app._digit_or_decimal("5")
        app._backspace()
        app._backspace()  # already empty
        assert app.current_input == ""
        assert app.display_var.get() == "0"


class TestDivideByZero:
    def test_divide_by_zero_shows_error_and_clears(self, app):
        """Error path: dividing by zero shows an error and clears state."""
        app._digit_or_decimal("8")
        app._operator("/")
        app._digit_or_decimal("0")
        with patch("tkinter.messagebox.showerror") as mock_error:
            app._evaluate()
            mock_error.assert_called_once()
            args = mock_error.call_args[0]
            assert args[0] == "Error"
            assert "zero" in args[1].lower()
        # State should be cleared after error
        assert app.current_input == ""
        assert app.operation is None
        assert app.prev_value is None
        assert app.display_var.get() == "0"