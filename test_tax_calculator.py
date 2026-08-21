import pytest
from tax_calculator import calculate_tax
from decimal import Decimal

TEST_CASES: list[tuple[Decimal, Decimal]] = [
    (Decimal(10000.00), Decimal(1050)),
    (Decimal(35000.00), Decimal(5033.00)),
    (Decimal(100000.00), Decimal(22877.50)),
    (Decimal(220000.00), Decimal(64877.50)),
]


@pytest.mark.parametrize("test_case", TEST_CASES)
def test_calculate_tax(test_case: tuple[Decimal, Decimal]):
    gross_income, expected_tax = test_case
    assert calculate_tax(gross_income) == expected_tax
