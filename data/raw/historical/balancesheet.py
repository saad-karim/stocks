import loader.date as loader
import data.raw.historical.format as formatter

def genRespWithYear(balanceSheet, year):
    return {
        "Year": year,
        "Current Assets": balanceSheet["totalCurrentAssets"],
        "Current Liabilities": balanceSheet["totalCurrentLiabilities"],
        "Shareholder Equity": balanceSheet["totalStockholdersEquity"],
        "Cash": balanceSheet["cashAndCashEquivalents"],
    }

class Yearly:

    __sheets = {}

    def __init__(self):
        return

    def load(self, sheets):
        for sheet in sheets:
            resp = self.data(sheet)
            self.__sheets[resp["Year"]] = resp

    def data(self, sheet):
        recordDate = sheet["date"]
        year = loader.getDate(recordDate)
        return genRespWithYear(sheet, year)

    def year(self, year):
        return self.__sheets[year]

    def allYears(self):
        return self.__sheets

class Quarterly:

    __sheets = {}

    def __init__(self):
        return

    def load(self, sheets):
        for sheet in sheets:
            resp = self.data(sheet)
            if resp != None:
                self.__sheets[resp["Year"]] = {
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
        if year in self.__sheets:
            if qtr in self.__sheets[year]:
                return self.__sheets[year][qtr]

        return {}

    def allQtrs(self):
        return self.__sheets

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

    def output(self):
        return {
            'Cash': [formatter.generate(self, "Cash"), "money"],
            'Current Assets': [formatter.generate(self, "Current Assets"), "money"],
            'Current Liabilities': [formatter.generate(self, "Current Liabilities"), "money"],
            'Shareholder Equity': [formatter.generate(self, "Shareholder Equity"), "money"],
        }
