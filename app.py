from decimal import Decimal

from flask import Flask, request, render_template
from tax_calculator import calculate_tax, PositiveCurrency

app = Flask(__name__)


@app.get("/calculate/paye")
def calculate_paye():
    raw_gross_income = request.args.get("gross_income", "")
    parsed_gross_income = PositiveCurrency(Decimal(raw_gross_income))
    calculated_paye = calculate_tax(parsed_gross_income)

    return {"paye_tax": calculated_paye}

@app.route("/")
def home():
    return render_template("home.html")
