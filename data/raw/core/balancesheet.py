import loader.date as loader

def genRespWithYear(balanceSheet, year):
    return {
        "Year": year,
        "Current Assets": balanceSheet["totalCurrentAssets"],
        "Current Liabilities": balanceSheet["totalCurrentLiabilities"],
        "Shareholder Equity": balanceSheet["totalStockholdersEquity"],
        "Cash": balanceSheet["cashAndCashEquivalents"],
        "Long-Term Debt": balanceSheet["longTermDebt"],
        "Common Stock": balanceSheet["commonStock"],
        "Retained Earnings": balanceSheet["retainedEarnings"],
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
        if year in self.__sheets:
            return self.__sheets[year]

        return {}

    def allYears(self):
        return self.__sheets

    def getKey(self, key): 
        resp = {}
        for year, sheet in self.__sheets.items():
            resp.update({year: sheet[key]})
        return resp

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
        qtr["Quarter"] = sheet["quarter"]
        return qtr

    def quarter(self, year, qtr):
        if year in self.__sheets:
            if qtr in self.__sheets[year]:
                return self.__sheets[year][qtr]

        return {}

    def allQtrs(self):
        return self.__sheets

class BalanceSheet:

    _yearly = Yearly()
    _quarterly = Quarterly()

    def __init__(self):
        return

    def yearly(self):
        return self._yearly

    def quarterly(self):
        return self._quarterly