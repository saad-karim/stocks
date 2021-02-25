import loader.date as loader

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

    incomes = {}

    def __init__(self):
        return

    def load(self, incomes):
        for income in incomes:
            resp = self.data(income)
            if resp != None:
                self.incomes[resp["Year"]] = {
                    resp["Quarter"]: resp,
                }

    def data(self, income):
        recordDate = income["date"]
        year = loader.getDate(recordDate)
        qtr = genRespWithYear(income, year)
        qtr["Quarter"] = income["period"]
        return qtr

    def quarter(self, year, qtr):
        if qtr in self.incomes[year]:
            return self.incomes[year][qtr]

        return {}

    def ttmEPS(self):
        addedQtrs = 0
        total = 0
        for year in self.incomes:
            qtrs = self.incomes.get(year)
            for qtr in qtrs:
                total = total + qtrs[qtr]["EPS"]
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
            'Interest Expense': [[
                self.quarter(2020, "Q2").get("Interest Expense"),
                self.quarter(2020, "Q1").get("Interest Expense"),
                self.year(2019).get("Interest Expense"),
                self.year(2018).get("Interest Expense"),
                self.year(2017).get("Interest Expense"),
                self.year(2016).get("Interest Expense"),
            ], "ratio"],
            'Total Revenue': [[
                self.quarter(2020, "Q2").get("Total Revenue"),
                self.quarter(2020, "Q1").get("Total Revenue"),
                self.year(2019).get("Total Revenue"),
                self.year(2018).get("Total Revenue"),
                self.year(2017).get("Total Revenue"),
                self.year(2016).get("Total Revenue"),
            ], "money"],
            'EBITDA': [[
                self.quarter(2020, "Q2").get("EBITDA"),
                self.quarter(2020, "Q1").get("EBITDA"),
                self.year(2019).get("EBITDA"),
                self.year(2018).get("EBITDA"),
                self.year(2017).get("EBITDA"),
                self.year(2016).get("EBITDA"),
            ], "money"],
            'Net Income': [[
                self.quarter(2020, "Q2").get("Net Income"),
                self.quarter(2020, "Q1").get("Net Income"),
                self.year(2019).get("Net Income"),
                self.year(2018).get("Net Income"),
                self.year(2017).get("Net Income"),
                self.year(2016).get("Net Income"),
            ], "money"],
            'Net Income Ratio': [[
                self.quarter(2020, "Q2").get("Net Income Ratio"),
                self.quarter(2020, "Q1").get("Net Income Ratio"),
                self.year(2019).get("Net Income Ratio"),
                self.year(2018).get("Net Income Ratio"),
                self.year(2017).get("Net Income Ratio"),
                self.year(2016).get("Net Income Ratio"),
            ], "ratio"],
            'Gross Profit': [[
                self.quarter(2020, "Q2").get("Gross Profit"),
                self.quarter(2020, "Q1").get("Gross Profit"),
                self.year(2019).get("Gross Profit"),
                self.year(2018).get("Gross Profit"),
                self.year(2017).get("Gross Profit"),
                self.year(2016).get("Gross Profit"),
            ], "money"],
            'Gross Profit Ratio': [[
                self.quarter(2020, "Q2").get("Gross Profit Ratio"),
                self.quarter(2020, "Q1").get("Gross Profit Ratio"),
                self.year(2019).get("Gross Profit Ratio"),
                self.year(2018).get("Gross Profit Ratio"),
                self.year(2017).get("Gross Profit Ratio"),
                self.year(2016).get("Gross Profit Ratio"),
            ], "ratio"],
            'Operating Income': [[
                self.quarter(2020, "Q2").get("Operating Income"),
                self.quarter(2020, "Q1").get("Operating Income"),
                self.year(2019).get("Operating Income"),
                self.year(2018).get("Operating Income"),
                self.year(2017).get("Operating Income"),
                self.year(2016).get("Operating Income"),
            ], "money"],
            'Operating Income Ratio': [[
                self.quarter(2020, "Q2").get("Operating Income Ratio"),
                self.quarter(2020, "Q1").get("Operating Income Ratio"),
                self.year(2019).get("Operating Income Ratio"),
                self.year(2018).get("Operating Income Ratio"),
                self.year(2017).get("Operating Income Ratio"),
                self.year(2016).get("Operating Income Ratio"),
            ], "ratio"],
                'EPS': [[
                self.quarter(2020, "Q2").get("EPS"),
                self.quarter(2020, "Q1").get("EPS"),
                self.year(2019).get("EPS"),
                self.year(2018).get("EPS"),
                self.year(2017).get("EPS"),
                self.year(2016).get("EPS"),
            ], "money"],
        }