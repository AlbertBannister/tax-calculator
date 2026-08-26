document.addEventListener("DOMContentLoaded", () => {
  console.log("Houston we have Javascript");
  const calculateButton = document.getElementById("calculate-button");
  calculateButton.addEventListener("click", () => {
    const rawGrossIncomeInput = document.getElementById("gross-income-input").value;
    const parsedGrossIncome = parseFloat(rawGrossIncomeInput)
    
    fetch(`/calculate/paye?gross_income=${parsedGrossIncome}`)
    .then((response) => response.json(),)
    .then(data => alert(data["paye_tax"]));
  });
});
