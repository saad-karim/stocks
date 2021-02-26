import loader.date as loader
import data.raw.historical.format as formatter
from collections import defaultdict

def genRespWithYear(income, year):
    return {
        "Year": year,
        "Quarter": income["period"],
        "Total Revenue": income["revenue"],
        "EBIT": income.get("ebit"),
        "EBITDA": income["ebitda"],
        "Net Income": income["netIncome"],
        "Net Income Ratio": income["netIncomeRatio"],
        "Gross Profit": income["grossProfit"],
        "Gross Profit Ratio": income["grossProfitRatio"],
        "Operating Income": income["operatingIncome"],
        "Operating Income Ratio": income["operatingIncomeRatio"],
        "Interest Expense": income["interestExpense"],
        "EPS": income["eps"],
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
        return self.incomes[year]

class Quarterly:

    incomes = defaultdict(list)

    def __init__(self):
        return

    def load(self, incomes):
        for income in incomes:
            resp = self.data(income)
            if resp != None:
                print("resp: ", resp)
                self.incomes[resp["Year"]].append({
                    resp["Quarter"]: resp,
                })

    def data(self, income):
        recordDate = income["date"]
        year = loader.getDate(recordDate)
        qtr = genRespWithYear(income, year)
        qtr["Quarter"] = income["period"]
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

    yearly = Yearly()
    quarterly = Quarterly()

    def __init__(self):
        return

    def loadYearlyData(self, incomes):
        self.yearly.load(incomes)
        return self

    def loadQuarterlyData(self, incomes):
        self.quarterly.load(incomes)
        return self

    def allQtrs(self):
        return self.quarterly.incomes

    def quarter(self, year, qtr):
        return self.quarterly.quarter(year, qtr)

    def allYears(self):
        return self.yearly.incomes

    def year(self, year):
        return self.yearly.year(year)

    def ttmEPS(self):
        return self.quarterly.ttmEPS()

    def output(self):
        return {
            'Interest Expense': [formatter.generate(self, "Interest Expense"), "ratio"],
            'Total Revenue': [formatter.generate(self, "Total Revenue"), "money"],
            'EBITDA': [formatter.generate(self, "EBITDA"), "money"], 
            'Net Income': [formatter.generate(self, "Net Income"), "money"],
            'Net Income Ratio': [formatter.generate(self, "Net Income Ration"), "ratio"],
            'Gross Profit': [formatter.generate(self, "Gross Profit"), "money"],
            'Gross Profit Ratio': [formatter.generate(self, "Gross Profit Ration"), "ratio"],
            'Operating Income': [formatter.generate(self, "Operation Income"), "money"],
            'Operating Income Ratio': [formatter.generate(self, "Operating Income Ratio"), "ratio"],
            'EPS': [formatter.generate(self, "EPS"), "money"],
        }