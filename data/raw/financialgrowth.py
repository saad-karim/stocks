import datetime

def genRespWithYear(raw, year):
    return {
        "Year": year,
        "EPS Growth": raw["epsgrowth"],
    }

def getDate(dateStr):
    date = datetime.datetime.strptime(dateStr, "%Y-%m-%d")
    return date.year

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
        year = getDate(recordDate)
        return genRespWithYear(income, year)

    def year(self, year):
        return self.incomes[year]

class Quarterly:

    currentYear = datetime.datetime.now().year
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
        year = getDate(recordDate)
        # if year == self.currentYear:
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

