import loader.date as loader

def genRespWithYear(raw, year):
    return {
        "Year": year,
        "Operating Cash Flow": raw.get("cashFlowOperating"),
        "Investing Cash Flow": raw.get("cashFlowInvesting"),
        "Financing Cash Flow": raw.get("cashFlowFinancing"),
        "Share Repurchase Cash Flow": raw.get("cashFlowShareRepurchase"),
    }

class Yearly:

    _fundamentals = {}

    def __init__(self):
        return

    def load(self, fundamentals):
        for f in fundamentals:
            resp = self.data(f)
            self._fundamentals[resp["Year"]] = resp

    def data(self, fundamental):
        recordDate = fundamental["date"]
        year = loader.getDate(recordDate)
        resp = genRespWithYear(fundamental, year)
        return resp

    def year(self, year):
        if year in self._fundamentals:
            return self._fundamentals[year]

        return {}

    def allYears(self):
        return self._fundamentals

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

class Fundamentals:

    _yearly = Yearly()
    _quarterly = Quarterly()

    def __init__(self):
        return

    def yearly(self):
        return self._yearly

    def quarterly(self):
        return self._quarterly
