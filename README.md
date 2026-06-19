# Simple Calculator (Tkinter)

A minimal desktop calculator built with Python's standard library (Tkinter).

## Features

- Basic arithmetic: addition, subtraction, multiplication, division.
- Decimal point support.
- Backspace and clear (C).
- Error handling for division by zero.

## Requirements

- Python 3.6 or higher (Tkinter is included by default).

## How to Run

```bash
python main.py
```

## Running Tests

```bash
python -m unittest discover tests
```

## Project Structure

```
.
├── main.py                  # GUI entry point
├── calculator_logic.py      # Calculation logic (separate from UI)
├── tests/
│   └── test_calculator_logic.py  # Unit tests
├── requirements.txt         # (empty – no dependencies)
└── README.md
```

## Architecture Decision

This project follows **ADR-001**: Python with Tkinter for the Calculator UI. The logic is isolated from the UI to allow easy testing and future extension (e.g., adding advanced operations).
