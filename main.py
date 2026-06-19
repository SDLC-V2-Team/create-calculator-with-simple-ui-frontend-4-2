import tkinter as tk
from tkinter import ttk, messagebox
from calculator_logic import CalculatorLogic

class CalculatorApp:
    """Simple Tkinter calculator with basic arithmetic operations."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.resizable(False, False)

        self.logic = CalculatorLogic()
        self.current_input = ""
        self.operation = None
        self.prev_value = None

        self._create_widgets()

    def _create_widgets(self):
        # Display entry
        self.display_var = tk.StringVar(value="0")
        display = ttk.Entry(self.root, textvariable=self.display_var, state="readonly", font=("Arial", 18), justify="right")
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        # Button layout (row, col, text)
        buttons = [
            (1, 0, "7"), (1, 1, "8"), (1, 2, "9"), (1, 3, "/"),
            (2, 0, "4"), (2, 1, "5"), (2, 2, "6"), (2, 3, "*"),
            (3, 0, "1"), (3, 1, "2"), (3, 2, "3"), (3, 3, "-"),
            (4, 0, "0"), (4, 1, "."), (4, 2, "="), (4, 3, "+"),
            (5, 0, "C"), (5, 1, "⌫")
        ]

        for row, col, text in buttons:
            cmd = self._button_action(text)
            btn = ttk.Button(self.root, text=text, command=cmd, width=5)
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

        # Make grid responsive
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def _button_action(self, text: str):
        if text.isdigit() or text == ".":
            return lambda: self._digit_or_decimal(text)
        elif text in ("+", "-", "*", "/"):
            return lambda: self._operator(text)
        elif text == "=":
            return lambda: self._evaluate()
        elif text == "C":
            return lambda: self._clear()
        elif text == "⌫":
            return lambda: self._backspace()
        else:
            return lambda: None

    def _digit_or_decimal(self, char: str):
        if char == "." and "." in self.current_input:
            return
        self.current_input += char
        self.display_var.set(self.current_input)

    def _operator(self, op: str):
        if self.current_input:
            if self.prev_value is not None and self.operation:
                # Chain operations without pressing '='
                self._evaluate()
            self.prev_value = float(self.current_input)
            self.operation = op
            self.current_input = ""
        else:
            # If no input, just change the operator
            self.operation = op

    def _evaluate(self):
        if self.prev_value is None or self.operation is None:
            return
        try:
            second = float(self.current_input) if self.current_input else self.prev_value
            result = self.logic.perform(self.prev_value, second, self.operation)
            self.display_var.set(str(result))
            self.prev_value = result
            self.current_input = ""
            self.operation = None
        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero")
            self._clear()
        except ValueError:
            messagebox.showerror("Error", "Invalid input")
            self._clear()

    def _clear(self):
        self.current_input = ""
        self.operation = None
        self.prev_value = None
        self.display_var.set("0")

    def _backspace(self):
        if len(self.current_input) > 0:
            self.current_input = self.current_input[:-1]
            self.display_var.set(self.current_input if self.current_input else "0")


def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
