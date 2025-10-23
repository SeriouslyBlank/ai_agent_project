
from pkg.calculator import Calculator

def test_expression():
    calculator = Calculator()
    result = calculator.evaluate("3 + 7 * 2")
    assert result == 17

test_expression()
