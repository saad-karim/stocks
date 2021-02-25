import datetime

def genRespWithYear(raw, year):
    return {
        "Year": year,
        "Number of Shares": raw["numberOfShares"],
        "Stock Price": raw["stockPrice"],
    }

def getDate(dateStr):
    date = datetime.datetime.strptime(dateStr, "%Y-%m-%d")
    return date.year

def getQuarter(dateStr):
    date = datetime.datetime.strptime(dateStr, "%Y-%m-%d")
    month = date.month
    if month <= 3:
        return "Q1"
    elif month <= 6:
        return "Q2"
    elif month <= 9:
        return "Q3"
    else:
        return "Q4"

class Yearly:

    values = {}

    def __init__(self):
        return

    def load(self, values):
        for value in values:
            resp = self.data(value)
            self.values[resp["Year"]] = resp

    def data(self, value):
        recordDate = value["date"]
        year = getDate(recordDate)
        return genRespWithYear(value, year)

    def year(self, year):
        return self.values[year]

class Quarterly:

    currentYear = datetime.datetime.now().year
    values = {
        # 2019: {},
        # 2020: {},
    }

    def __init__(self):
        return

    def load(self, values):
        for value in values:
            resp = self.data(value)
            if resp != None:
                # print(resp)
                self.values[resp["Year"]] = {
                    resp["Quarter"]: resp,
                }

    def data(self, value):
        recordDate = value["date"]
        year = getDate(recordDate)
        # print("value: ", value)
        # if year == self.currentYear:
        qtr = genRespWithYear(value, year)
        qtr["Quarter"] = getQuarter(recordDate)

        return qtr

    def quarter(self, year, qtr):
        # print(self.values)
        if qtr in self.values[year]:
            return self.values[year][qtr]

        return {}

class EnterpriseValues:

    yearly = Yearly()
    quarterly = Quarterly()

    def __init__(self):
        return

    def loadYearlyData(self, values):
        self.yearly.load(values)
        return self

    def loadQuarterlyData(self, values):
        self.quarterly.load(values)
        return self

    def quarter(self, year, qtr):
        return self.quarterly.quarter(year, qtr)

    def year(self, year):
        return self.yearly.year(year)

