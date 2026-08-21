from dataclasses import dataclass
from loguru import logger
from decimal import Decimal, InvalidOperation


@dataclass
class PAYETaxBracket:
    "Class representing an income tax bracket"

    lower: Decimal
    upper: Decimal
    tax_rate: Decimal


TAX_BRACKETS = [
    PAYETaxBracket(Decimal(0), Decimal(15600), Decimal(10.5)),
    PAYETaxBracket(Decimal(15600.0), Decimal(53500.0), Decimal(17.5)),
    PAYETaxBracket(Decimal(53500.0), Decimal(78100.0), Decimal(30.0)),
    PAYETaxBracket(Decimal(78100.0), Decimal(180000.0), Decimal(33.0)),
    PAYETaxBracket(Decimal(180000.0), Decimal("Infinity"), Decimal(39.0)),
]


def calculate_tax(gross_income: Decimal) -> Decimal:
    logger.info(f"Calculating PAYE tax for {gross_income}")
    total_paye_tax: Decimal = Decimal(0.0)
    for tax_bracket in TAX_BRACKETS:
        if gross_income < tax_bracket.lower:
            break
        logger.debug(f"Tax bracket: {tax_bracket}")
        taxable_income_in_bracket = (
            min(tax_bracket.upper, gross_income) - tax_bracket.lower
        )
        logger.debug(f"Taxable income in bracket: {taxable_income_in_bracket}")
        calculated_paye_in_bracket = (
            taxable_income_in_bracket * tax_bracket.tax_rate
        ) / Decimal(100.0)
        logger.debug(f"Calculated PAYE: {calculated_paye_in_bracket}")
        total_paye_tax += calculated_paye_in_bracket

    return total_paye_tax


def main():
    print("Welcome to Albert's tax calculator!")
    print("Type in your gross yearly income and we'll calculate your PAYE tax")
    print("Press q at any time to quit")
    valid_input = False
    parsed_gross_income: Decimal | None = None
    while not valid_input:
        raw_user_input = input("Enter your gross annual income:")
        if raw_user_input == "q":
            print("Seeya next time!")
            return

        try:
            parsed_gross_income = Decimal(raw_user_input)
            if parsed_gross_income < 0:
                print("Income cannot be negative")
                continue
            valid_input = True
        except InvalidOperation:
            print("Income must be a number")
            continue

    if parsed_gross_income is None:
        print("Something went wrong")
        return

    paye_tax = calculate_tax(parsed_gross_income)
    print(f"PAYE tax owed: {paye_tax}")


if __name__ == "__main__":
    main()
