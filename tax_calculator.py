from dataclasses import dataclass
from loguru import logger


@dataclass
class PAYETaxBracket:
    "Class representing an income tax bracket"

    lower: float
    upper: float
    tax_rate: float


TAX_BRACKETS = [
    PAYETaxBracket(0.0, 15600.0, 10.5),
    PAYETaxBracket(15601.0, 53500.0, 17.5),
    PAYETaxBracket(53500.0, 78100.0, 30.0),
    PAYETaxBracket(78101.0, 180000.0, 33.0),
    PAYETaxBracket(180000.0, float("inf"), 39.0),
]


def calculate_tax(gross_income: float) -> float:
    logger.info(f"Calculating PAYE tax for {gross_income}")
    total_paye_tax: float = 0.0
    for tax_bracket in TAX_BRACKETS:
        if gross_income < tax_bracket.lower:
            break
        logger.debug(f"Tax bracket: {tax_bracket}")
        taxable_income_in_bracket = (
            min(tax_bracket.upper, gross_income) - tax_bracket.lower
        )
        logger.debug(f"Taxable income in bracket: {taxable_income_in_bracket}")
        calculated_paye_in_bracket = (taxable_income_in_bracket * tax_bracket.tax_rate) / 100.0
        logger.debug(f"Calculated PAYE: {calculated_paye_in_bracket}")
        total_paye_tax += calculated_paye_in_bracket

    return total_paye_tax


def main():
    print("Hello from hnry-tax-calculator!")


if __name__ == "__main__":
    main()
