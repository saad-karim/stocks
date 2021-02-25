class FreeCashFlowRatio:

    yearly = {}
    quarterly = {}

    def __init__(self):
        return

    def calc(self, income, cashflow):
        self.calcYearly(income, cashflow)
        self.calcQuarterly(income, cashflow)

    def calcYearly(self, income, cashflow):
        yearlyIncomes = income.allYears()
        yearlyCF = cashflow.allYears()

        for year in yearlyIncomes:
            if year not in yearlyCF:
                continue
            income = yearlyIncomes[year]
            cashflow = yearlyCF[year]
            self.yearly[year] = cashflow["Free Cash Flow"] / income["Total Revenue"]

    def calcQuarterly(self, income, cashflow):
        qtrIncomes = income.allQtrs()
        qtrCF = cashflow.allQtrs()

        for year in qtrIncomes:
            qtrsIncome = qtrIncomes[year]
            qtrsCF = qtrCF[year]
            for qtr in qtrsIncome:
                income = qtrsIncome[qtr]
                cashflow = qtrsCF[qtr]
                self.quarterly[year] = {
                    qtr: cashflow["Free Cash Flow"] / income["Total Revenue"]
                }

    def year(self, year):
        return self.yearly.get(year)

    def quarter(self, year, qtr):
        return self.quarterly.get(year).get(qtr)
