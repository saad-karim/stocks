import loader.date as loader

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

    cashflows = {}

    def __init__(self):
        return

    def load(self, cashflows):
        for cashflow in cashflows:
            resp = self.data(cashflow)
            self.cashflows[resp["Year"]] = resp

    def data(self, cashflow):
        recordDate = cashflow["date"]
        year = loader.getDate(recordDate)
        return genRespWithYear(cashflow, year)

    def year(self, year):
        return self.cashflows[year]

class Quarterly:

    cashflows = {}

    def __init__(self):
        return

    def load(self, cashflows):
        for cashflow in cashflows:
            resp = self.data(cashflow)
            if resp != None:
                self.cashflows[resp["Year"]] = {
                    resp["Quarter"]: resp,
                }

    def data(self, cashflow):
        print(cashflow)
        recordDate = cashflow["date"]
        year = loader.getDate(recordDate)
        qtr = genRespWithYear(cashflow, year)
        qtr["Quarter"] = cashflow["period"]
        return qtr

    def quarter(self, year, qtr):
        if qtr in self.cashflows[year]:
            return self.cashflows[year][qtr]

        return {}

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
        return self.quarterly.cashflows

    def quarter(self, year, qtr):
        return self.quarterly.quarter(year, qtr)

    def allYears(self):
        return self.yearly.cashflows

    def year(self, year):
        return self.yearly.year(year)
