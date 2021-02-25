import loader.date as loader

def genRespWithYear(raw, year):
    return {
        "Year": year,
        "EPS Growth": raw["epsgrowth"],
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
    numOfQtrs = 0

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
        qtr["Quarter"] = "Q"+str(self.numOfQtrs)
        self.numOfQtrs+=1
        return qtr

    def quarter(self, year, qtr):
        if qtr in self.incomes[year]:
            return self.incomes[year][qtr]

        return {}

class FinancialGrowth:

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
            'EPS Growth': [[
                self.quarter(2020, "Q2").get("EPS Growth"),
                self.quarter(2020, "Q1").get("EPS Growth"),
                self.year(2019).get("EPS Growth"),
                self.year(2018).get("EPS Growth"),
                self.year(2017).get("EPS Growth"),
                self.year(2016).get("EPS Growth"),
            ], "money"],
            'Price Growth': [[
                0,
                0,
                self.year(2019).get("Price Growth"),
                self.year(2018).get("Price Growth"),
                self.year(2017).get("Price Growth"),
                # stock.priceGrowth.year(2016).get("Price Growth"),
            ], "pct"],
        }

