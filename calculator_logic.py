class CalculatorLogic:
    """Handles arithmetic operations for the calculator."""

    @staticmethod
    def perform(a: float, b: float, operator: str) -> float:
        """Perform a basic arithmetic operation.

        Args:
            a: First operand (float).
            b: Second operand (float).
            operator: One of '+', '-', '*', '/'.

        Returns:
            Result of the operation.

        Raises:
            ZeroDivisionError: If operator is '/' and b is 0.
        """
        ops = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y  # ZeroDivisionError will bubble up
        }
        if operator not in ops:
            raise ValueError(f"Unsupported operator: {operator}")
        return ops[operator](a, b)
