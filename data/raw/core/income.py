import loader.date as loader
from collections import defaultdict

def genRespWithYear(income, year):
    return {
        "Year": year,
        "Quarter": income["quarter"],
        "Total Revenue": income["revenue"],
        "EBIT": income.get("ebit"),
        # "EBITDA": income["ebitda"],
        "Net Income": income["netIncome"],
        # "Net Income Ratio": income["netIncomeRatio"],
        "Gross Profit": income["grossProfit"],
        # "Gross Profit Ratio": income["grossProfitRatio"],
        "Operating Income": income["operatingIncome"],
        # "Operating Income Ratio": income["operatingIncomeRatio"],
        # "Interest Expense": income["interestExpense"],
        # "EPS": income["eps"],
    }

class Yearly:

    incomes = {}

    def __init__(self):
        return

    def load(self, incomes):
        for income in incomes:
            resp = self.data(income)
            self.incomes[resp["Year"]] = resp

    def data(self, income):
        recordDate = income["date"]
        year = loader.getDate(recordDate)
        return genRespWithYear(income, year)

    def year(self, year):
        if year in self.incomes:
            return self.incomes[year]
        return {}

class Quarterly:

    incomes = defaultdict(list)

    def __init__(self):
        return

    def load(self, incomes):
        for income in incomes:
            resp = self.data(income)
            if resp != None:
                self.incomes[resp["Year"]].append({
                    resp["Quarter"]: resp,
                })

    def data(self, income):
        recordDate = income["date"]
        year = loader.getDate(recordDate)
        qtr = genRespWithYear(income, year)
        qtr["Quarter"] = income["quarter"]
        return qtr

    def quarter(self, year, qtr):
        if year in self.incomes:
            if qtr in self.incomes[year]:
                return self.incomes[year][qtr]

        return {}

    def ttmEPS(self):
        addedQtrs = 0
        total = 0
        for year in self.incomes:
            qtrs = self.incomes.get(year)
            for qtr in qtrs:
                for q in qtr:
                    total = total + qtr[q]["EPS"]
                    addedQtrs+=1

                    if addedQtrs == 4:
                        return total

class Income:

    _yearly = Yearly()
    _quarterly = Quarterly()

    def __init__(self):
        return

    def yearly(self):
        return self._yearly

    def quarterly(self):
        return self._quarterly