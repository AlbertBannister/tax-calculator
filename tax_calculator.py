from dataclasses import dataclass


@dataclass
class PAYETaxBracket:
    "Class representing an income tax bracket"

    lower: float
    upper: float
    tax_rate: float


TAX_BRACKETS = [
    PAYETaxBracket(0.0, 15600.0, 10.5),
    PAYETaxBracket(15601.0, 53500.0, 17.5),
    PAYETaxBracket(53500.0, 78100, 30.0),
    PAYETaxBracket(78101.0, 180000.0, 33.0),
    PAYETaxBracket(180000.0, float("inf"), 39.0),
]


def calculate_tax(gross_income: float) -> float:
    return -1.0


def main():
    print("Hello from hnry-tax-calculator!")


if __name__ == "__main__":
    main()
