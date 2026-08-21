import pytest
from tax_calculator import calculate_tax

TEST_CASES: list[tuple[float, float]] = [
    (10000.00, 1050),
    (35000.00, 5033.00),
    (100000.00, 22877.50),
    (220000.00, 64877.50),
]


@pytest.mark.parametrize("test_case", TEST_CASES)
def test_calculate_tax(test_case: tuple[float, float]):
    gross_income, expected_tax = test_case
    assert calculate_tax(gross_income) == expected_tax
