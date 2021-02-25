import loader.date as loader

def genRespWithYear(raw, year):
    return {
        "Year": year,
        "Current Ratio": raw["currentRatio"],
        "Gross Profit Margin": raw["grossProfitMargin"],
        "Operating Profit Margin": raw["operatingProfitMargin"],
        "Net Profit Margin": raw["netProfitMargin"],
        "Return on Assets": raw["returnOnAssets"],
        "Return on Equity": raw["returnOnEquity"],
        "Debt Equity Ratio": raw["debtEquityRatio"],
        "Interest Coverage": raw["interestCoverage"],
        "Price To Book Ratio": raw["priceToBookRatio"],
        "Price Book Value Ratio": raw["priceBookValueRatio"],
    }

class Yearly:

    ratios = {}

    def __init__(self):
        return

    def load(self, raw):
        for r in raw:
            resp = self.genResp(r)
            self.ratios[resp["Year"]] = resp

        return self

    def genResp(self, raw):
        date = raw["date"]
        year = loader.getDate(date)
        return genRespWithYear(raw, year)

    def year(self, year):
        return self.ratios[year]

class Quarterly:

    ratios = {}
    numOfQtrs = 0

    def __init__(self):
        return

    def load(self, raw):
        qtrs = len(raw)
        for r in raw:
            resp = self.data(r)
            if resp != None:
                self.ratios[resp["Year"]] = {
                    resp["Quarter"]: resp,
                }

    def data(self, raw):
        recordDate = raw["date"]
        year = loader.getDate(recordDate)
        qtr = genRespWithYear(raw, year)
        qtr["Quarter"] = "Q"+str(self.numOfQtrs)
        self.numOfQtrs+=1
        return qtr

    def quarter(self, year, qtr):
        if qtr in self.ratios[year]:
            return self.ratios[year][qtr]

        return {}

class FinancialRatios:

    yearlyRatios = Yearly()
    quarterlyRatios = Quarterly()

    def __init__(self):
        return

    def loadYearlyData(self, raw):
        self.yearlyRatios.load(raw)
        return self

    def loadQuarterlyData(self, raw):
        self.quarterlyRatios.load(raw)
        return self

    def quarter(self, year, qtr):
        return self.quarterlyRatios.quarter(year, qtr)

    def year(self, year):
        return self.yearlyRatios.year(year)
