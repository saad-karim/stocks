import loader.date as loader

def genRespWithYear(balanceSheet, year):
    return {
        "Year": year,
        "Current Assets": balanceSheet["totalCurrentAssets"],
        "Current Liabilities": balanceSheet["totalCurrentLiabilities"],
        "Shareholder Equity": balanceSheet["totalStockholdersEquity"],
        "Cash": balanceSheet["cashAndCashEquivalents"],
    }

class Yearly:

    sheets = {}

    def __init__(self):
        return

    def load(self, sheets):
        for sheet in sheets:
            resp = self.data(sheet)
            self.sheets[resp["Year"]] = resp

    def data(self, sheet):
        recordDate = sheet["date"]
        year = loader.getDate(recordDate)
        return genRespWithYear(sheet, year)

    def year(self, year):
        return self.sheets[year]

class Quarterly:

    sheets = {}

    def __init__(self):
        return

    def load(self, sheets):
        for sheet in sheets:
            resp = self.data(sheet)
            if resp != None:
                self.sheets[resp["Year"]] = {
                    resp["Quarter"]: resp,
                }

    def data(self, sheet):
        # recordDate = sheet["fillingDate"]
        recordDate = sheet["date"]
        year = loader.getDate(recordDate)
        qtr = genRespWithYear(sheet, year)
        qtr["Quarter"] = sheet["period"]
        return qtr

    def quarter(self, year, qtr):
        if qtr in self.sheets[year]:
            return self.sheets[year][qtr]

        return {}

class BalanceSheet:

    yearly = Yearly()
    quarterly = Quarterly()

    def __init__(self):
        return

    def loadYearlyData(self, balanceSheet):
        self.yearly.load(balanceSheet)
        return self

    def loadQuarterlyData(self, balanceSheet):
        self.quarterly.load(balanceSheet)
        return self

    def quarter(self, year, qtr):
        return self.quarterly.quarter(year, qtr)

    def year(self, year):
        return self.yearly.year(year)
