import loader.date as loader
import data.raw.historical.format as formatter

def genRespWithYear(raw, year):
    return {
        "Year": year,
        "Number of Shares": raw["numberOfShares"],
        "Stock Price": raw["stockPrice"],
    }

class Yearly:

    __values = {}

    def __init__(self):
        return

    def load(self, values):
        for value in values:
            resp = self.data(value)
            self.__values[resp["Year"]] = resp

    def data(self, value):
        recordDate = value["date"]
        year = loader.getDate(recordDate)
        return genRespWithYear(value, year)

    def year(self, year):
        return self.__values[year]

    def allYears(self):
        return self.__values

class Quarterly:

    __values = {}

    def __init__(self):
        return

    def load(self, values):
        for value in values:
            resp = self.data(value)
            if resp != None:
                # print(resp)
                self.__values[resp["Year"]] = {
                    resp["Quarter"]: resp,
                }

    def data(self, value):
        recordDate = value["date"]
        year = loader.getDate(recordDate)
        qtr = genRespWithYear(value, year)
        qtr["Quarter"] = loader.getQuarter(recordDate)

        return qtr

    def quarter(self, year, qtr):
        if year in self.__values:
            if qtr in self.__values[year]:
                return self.__values[year][qtr]

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
    
    def allYears(self):
        return self.yearly.allYears()

    def output(self):
        return {
            'Price': [formatter.generate(self, "Stock Price"), "num"],
            'Number of Shares': [formatter.generate(self, "Number of Shares"), "num"],
        }
