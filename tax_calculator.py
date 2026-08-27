from dataclasses import dataclass
from multiprocessing import Value
from numbers import Number
from loguru import logger
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Any, Literal


class NumberIsNegativeError(ValueError):
    pass


class InvalidPercentageError(ValueError):
    pass


@dataclass(frozen=True)
class PositiveCurrency:
    value: Decimal

    def __post_init__(self) -> None:
        if self.value < 0:
            raise NumberIsNegativeError("Currency quantity must be positive")

    @classmethod
    def from_any(cls, value: Any):
        return cls(Decimal(value))


@dataclass(frozen=True)
class Percentage:
    value: Decimal

    def __post_init__(self) -> None:
        if self.value < 0:
            raise NumberIsNegativeError("Percentage must be zero or positive")

        if self.value > 1:
            raise InvalidPercentageError("Percentage must be under 1")

    @classmethod
    def from_ratio(cls, ratio: Any):
        return cls(Decimal(ratio))

    @classmethod
    def from_percent(cls, percent: Any):
        ratio = Decimal(percent) / 100
        return cls(ratio)


@dataclass(frozen=True)
class PAYETaxBracket:
    "Class representing an income tax bracket"

    lower: PositiveCurrency
    upper: PositiveCurrency
    tax_rate: Percentage

    @classmethod
    def from_numeric(
        cls, lower: float | int, upper: float | int, tax_rate: float | int
    ):
        return cls(
            PositiveCurrency.from_any(lower),
            PositiveCurrency.from_any(upper),
            Percentage.from_percent(tax_rate),
        )


class TimePeriod(Enum):
    DAILY = Decimal(1)
    WEEKLY = Decimal(7)
    FORTNIGHTLY = Decimal(14)
    MONTHLY = Decimal(30)
    YEARLY = Decimal(365)


class TaxJurisdiction(Enum):
    NZ = "NZ"
    AU = "AU"


NZ_TAX_BRACKETS = [
    PAYETaxBracket.from_numeric(lower, upper, tax_rate)
    for (lower, upper, tax_rate) in [
        (0, 15600, 10.5),
        (15600.0, 53500.0, 17.5),
        (53500.0, 78100.0, 30),
        (78100.0, 180000.0, 33),
        (180000.0, float("inf"), 39),
    ]
]

AUS_TAX_BRACKETS = [
    PAYETaxBracket.from_numeric(lower, upper, tax_rate)
    for (lower, upper, tax_rate) in [
        (0, 18200, 0),
        (18200, 45000, 16),
        (45000, 135000, 30),
        (135000, 190000, 37),
        (190000.0, float("inf"), 45),
    ]
]

TAX_BRACKETS = {
    TaxJurisdiction.NZ: NZ_TAX_BRACKETS,
    TaxJurisdiction.AU: AUS_TAX_BRACKETS,
}


def calculate_yearly_income(
    gross_income: PositiveCurrency, time_period: TimePeriod
) -> Decimal:
    logger.info(f"Calculating gross yearly income with {time_period}")
    gross_yearly_income = (
        gross_income.value * time_period.value / TimePeriod.YEARLY.value
    )
    logger.info(f"Gross yearly income calculated: {gross_yearly_income}")
    return gross_yearly_income


def calculate_tax(
    gross_income: PositiveCurrency,
    time_period: TimePeriod = TimePeriod.YEARLY,
    tax_country: TaxJurisdiction = TaxJurisdiction.NZ,
) -> Decimal:
    logger.info(f"Calculating PAYE tax for {gross_income} in {tax_country}")
    total_paye_tax = Decimal(0)
    for tax_bracket in TAX_BRACKETS[tax_country]:
        if gross_income.value < tax_bracket.lower.value:
            break
        logger.debug(f"Tax bracket: {tax_bracket}")
        taxable_income_in_bracket = (
            min(tax_bracket.upper.value, gross_income.value) - tax_bracket.lower.value
        )
        logger.debug(f"Taxable income in bracket: {taxable_income_in_bracket}")
        calculated_paye_in_bracket = (
            taxable_income_in_bracket * tax_bracket.tax_rate.value
        )
        logger.debug(f"Calculated PAYE: {calculated_paye_in_bracket}")
        total_paye_tax += calculated_paye_in_bracket

    return total_paye_tax.quantize(Decimal(".01"))


def main():
    print("Welcome to Albert's tax calculator!")
    print("Type in your gross yearly income and we'll calculate your PAYE tax")
    print("Press q at any time to quit")
    valid_input = False
    parsed_gross_income: PositiveCurrency | None = None
    while not valid_input:
        raw_user_input = input("Enter your gross annual income:")
        if raw_user_input == "q":
            print("Seeya next time!")
            return

        try:
            parsed_gross_income = PositiveCurrency.from_any(raw_user_input)
            valid_input = True
        except NumberIsNegativeError:
            print("Gross income must be positive!")
            continue
        except InvalidOperation:
            print("Gross income must be a number")

    if parsed_gross_income is None:
        print("Something went wrong")
        return

    valid_country = False
    user_country: TaxJurisdiction | None = None

    while not valid_country:
        raw_user_country = input("Enter the tax jurisdiction, one of NZ or AU: ")

        try:
            user_country = TaxJurisdiction[raw_user_country]
            valid_country = True
        except KeyError:
            print("Must be NZ or AU")

    if not user_country:
        print("Something went wrong")
        return

    paye_tax = calculate_tax(parsed_gross_income, tax_country=user_country)
    print(f"PAYE tax owed: {paye_tax}")


if __name__ == "__main__":
    main()
