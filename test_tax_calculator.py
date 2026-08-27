import pytest
from tax_calculator import calculate_tax, PositiveCurrency, NumberIsNegativeError, Percentage, InvalidPercentageError
from decimal import Decimal

NZ_TEST_CASES: list[tuple[PositiveCurrency, Decimal]] = [
    (PositiveCurrency.from_any(gross_income), Decimal(paye_tax))
    for (gross_income, paye_tax) in [
        (10000.00, 1050),
        (35000.00, 5033.00),
        (100000.00, 22877.50),
        (220000.00, 64877.50),
    ]
]

AU_TEST_CASES: list[tuple[PositiveCurrency, Decimal]] = [
    (PositiveCurrency.from_any(gross_income), Decimal(paye_tax))
    for (gross_income, paye_tax) in [
        (10000.00, 0),
        (35000.00, 2688.00),
        (100000.00, 20788.00),
        (220000.00, 65138.00),
    ]
]

@pytest.mark.parametrize("test_case", NZ_TEST_CASES)
def test_calculate_tax_nz(test_case: tuple[PositiveCurrency, Decimal]):
    gross_income, expected_tax = test_case
    assert calculate_tax(gross_income, tax_country="NZ") == expected_tax

@pytest.mark.parametrize("test_case", AU_TEST_CASES)
def test_calculate_tax_au(test_case: tuple[PositiveCurrency, Decimal]):
    gross_income, expected_tax = test_case
    print(f"Testing {gross_income} {expected_tax} in AU")
    assert calculate_tax(gross_income, tax_country="AU") == expected_tax


# def test_positive_currency():
#     with pytest.raises(NumberIsNegativeError):
#         PositiveCurrency.from_any("-1")


# def test_positive_percentage():
#     with pytest.raises(NumberIsNegativeError):
#         Percentage.from_ratio("-1")


# def test_percentage_under_one():
#     with pytest.raises(InvalidPercentageError):
#         Percentage.from_ratio(1000)


# def test_percentage_from_percent():
#     assert Percentage.from_percent(100).value == Decimal(1)
