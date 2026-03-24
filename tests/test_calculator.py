import pytest

from myproject.calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


class TestAdd:
    def test_positive(self, calc):
        assert calc.add(2, 3) == 5

    def test_negative(self, calc):
        assert calc.add(-1, -2) == -3

    def test_float(self, calc):
        assert calc.add(0.1, 0.2) == pytest.approx(0.3)


class TestSubtract:
    def test_positive(self, calc):
        assert calc.subtract(10, 4) == 6

    def test_negative_result(self, calc):
        assert calc.subtract(3, 7) == -4

    def test_zero(self, calc):
        assert calc.subtract(5, 5) == 0

    def test_float(self, calc):
        assert calc.subtract(0.3, 0.1) == pytest.approx(0.2)


class TestMultiply:
    def test_positive(self, calc):
        assert calc.multiply(3, 4) == 12

    def test_by_zero(self, calc):
        assert calc.multiply(5, 0) == 0

    def test_negative(self, calc):
        assert calc.multiply(-2, 3) == -6

    def test_float(self, calc):
        assert calc.multiply(0.1, 0.3) == pytest.approx(0.03)


class TestDivide:
    def test_positive(self, calc):
        assert calc.divide(10, 2) == 5

    def test_float_result(self, calc):
        assert calc.divide(7, 2) == pytest.approx(3.5)

    def test_float_rounding(self, calc):
        assert calc.divide(1, 3) == pytest.approx(0.3333, rel=1e-4)

    def test_divide_by_zero(self, calc):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calc.divide(5, 0)

    def test_negative_divide_by_zero(self, calc):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calc.divide(-5, 0)
