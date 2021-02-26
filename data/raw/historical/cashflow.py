import loader.date as loader
import data.raw.historical.format as formatter

def genRespWithYear(raw, year):
    return {
        "Year": year,
        "Free Cash Flow": raw["freeCashFlow"],
        "Operating Cash Flow": raw.get("operatingCashFlow"),
        "Investing Cash Flow": raw.get("investingCashFlow"),
        "Financing Cash Flow": raw.get("financingCashFlow"),
        "Net Change in Cash": raw.get("netChangeInCash"),
        "Stock Buyback": raw.get("commonStockRepurchased"),
        "Acquisitions": raw.get("acquisitionsNet"),
    }

class Yearly:

    __cashflows = {} # Private attribute, load method should be use to fill this

    def __init__(self):
        return

    def load(self, cashflows):
        for cashflow in cashflows:
            resp = self.__data(cashflow)
            self.__cashflows[resp["Year"]] = resp

    def __data(self, cashflow):
        recordDate = cashflow["date"]
        year = loader.getDate(recordDate)
        return genRespWithYear(cashflow, year)

    def year(self, year):
        return self.__cashflows[year]

    def allYears(self):
        return self.__cashflows

class Quarterly:

    __cashflows = {} # Private attribute, load method should be use to fill this

    def __init__(self):
        return

    def load(self, cashflows):
        for cashflow in cashflows:
            resp = self.__data(cashflow)
            if resp != None:
                self.__cashflows[resp["Year"]] = {
                    resp["Quarter"]: resp,
                }

    def __data(self, cashflow):
        # print(cashflow)
        recordDate = cashflow["date"]
        year = loader.getDate(recordDate)
        qtr = genRespWithYear(cashflow, year)
        qtr["Quarter"] = cashflow["period"]
        return qtr

    def quarter(self, year, qtr):
        if year in self.__cashflows:
            if qtr in self.__cashflows[year]:
                return self.__cashflows[year][qtr]

        return {}

    def allQtrs(self):
        return self.__cashflows

class CashFlow:

    yearly = Yearly()
    quarterly = Quarterly()

    def __init__(self):
        return

    def loadYearlyData(self, cashflows):
        self.yearly.load(cashflows)
        return self

    def loadQuarterlyData(self, cashflows):
        self.quarterly.load(cashflows)
        return self

    def allQtrs(self):
        return self.quarterly.allQtrs()

    def quarter(self, year, qtr):
        return self.quarterly.quarter(year, qtr)

    def allYears(self):
        return self.yearly.allYears()

    def year(self, year):
        return self.yearly.year(year)
        
    def output(self):
        return {
            'Free Cash Flow': [formatter.generate(self, "Free Cash Flow"), "money"],
            'Acquisitions': [formatter.generate(self, "Acquisitions"), "money"],
            'Stock BuyBack': [formatter.generate(self, "Stock Buyback"), "money"],
            'Net Change in Cash': [formatter.generate(self, "Net Change in Cash"), "money"],
            'Operating Cash Flow': [formatter.generate(self, "Operating Cash Flow"), "money"],
            'Investing Cash Flow': [formatter.generate(self, "Investing Cash Flow"), "money"],
            'Financing Cash Flow': [formatter.generate(self, "Financing Cash Flow"), "money"],
        }