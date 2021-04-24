import loader.date as loader

def genRespWithYear(raw, year):
    return {
        "Year": year,
        "Operating Cash Flow": raw.get("operatingCashFlow"),
        "Investing Cash Flow": raw.get("investingCashFlow"),
        "Financing Cash Flow": raw.get("financingCashFlow"),
        "Net Change in Cash": raw.get("netChangeInCash"),
        "Capital Expenditures": raw.get("capitalExpenditures"),
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
        if year in self.__cashflows:
            return self.__cashflows[year]
        
        return {}

    def allYears(self):
        return self.__cashflows

    def getKey(self, key): 
        resp = {}
        for year, cf in self.__cashflows.items():
            resp.update({year: cf[key]})
        return resp


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
        qtr["Quarter"] = cashflow["quarter"]
        return qtr

    def quarter(self, year, qtr):
        if year in self.__cashflows:
            if qtr in self.__cashflows[year]:
                return self.__cashflows[year][qtr]

        return {}

    def allQtrs(self):
        return self.__cashflows

class CashFlow:

    _yearly = Yearly()
    _quarterly = Quarterly()

    def __init__(self):
        return

    def yearly(self):
        return self._yearly

    def quarterly(self):
        return self._quarterly