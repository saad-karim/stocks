import loader.date as loader
import data.raw.historical.format as formatter

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
        if year in self.ratios:
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

    def output(self):
        return {
            'Gross Profit Margin': [formatter.generate(self, "Gross Profit Margin"), "pct"],
            'Operating Profit Margin': [formatter.generate(self, "Operating Profit Margin"), "pct"],
            'Net Profit Margin': [formatter.generate(self, "Net Profit Margin"), "pct"],
            'Return on Assets': [formatter.generate(self, "Return on Assets"), "pct"],
            'Return on Equity': [formatter.generate(self, "Return on Equity"), "pct"],
            'Debt Equity Ratio': [formatter.generate(self, "Debt Equity Ratio"), "ratio"],
            'Interest Coverage': [formatter.generate(self, "Interest Coverage"), "ratio"],
            'Price To Book Ratio': [formatter.generate(self, "Price To Book Ratio"), "ratio"],
            'Current Ratio': [formatter.generate(self, "Current Ratio"), "ratio"], 
            # 'Free Cash Flow Ratio': [[
            #     stock.metrics.freeCashFlowRatio().quarter(currentYear, "Q2"),
            #     stock.metrics.freeCashFlowRatio().quarter(currentYear, "Q1"),
            #     stock.metrics.freeCashFlowRatio().year(currentYear-1),
            #     stock.metrics.freeCashFlowRatio().year(currentYear-2),
            #     stock.metrics.freeCashFlowRatio().year(currentYear-3),
            #     stock.metrics.freeCashFlowRatio().year(2016),
            # ], "ratio"],
        }