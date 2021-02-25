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

    def output(self):
        return {
            'Gross Profit Margin': [[
                self.quarter(2020, "Q2").get("Gross Profit Margin"),
                self.quarter(2020, "Q1").get("Gross Profit Margin"),
                self.year(2019).get("Gross Profit Margin"),
                self.year(2018).get("Gross Profit Margin"),
                self.year(2017).get("Gross Profit Margin"),
                self.year(2016).get("Gross Profit Margin"),
            ], "pct"],
            'Operating Profit Margin': [[
                self.quarter(2020, "Q2").get("Operating Profit Margin"),
                self.quarter(2020, "Q1").get("Operating Profit Margin"),
                self.year(2019).get("Operating Profit Margin"),
                self.year(2018).get("Operating Profit Margin"),
                self.year(2017).get("Operating Profit Margin"),
                self.year(2016).get("Operating Profit Margin"),
            ], "pct"],
            'Net Profit Margin': [[
                self.quarter(2020, "Q2").get("Net Profit Margin"),
                self.quarter(2020, "Q1").get("Net Profit Margin"),
                self.year(2019)["Net Profit Margin"],
                self.year(2018)["Net Profit Margin"],
                self.year(2017)["Net Profit Margin"],
                self.year(2016)["Net Profit Margin"],
            ], "pct"],
            'Return on Assets': [[
                self.quarter(2020, "Q2").get("Return on Assets"),
                self.quarter(2020, "Q1").get("Return on Assets"),
                self.year(2019).get("Return on Assets"),
                self.year(2018).get("Return on Assets"),
                self.year(2017).get("Return on Assets"),
                self.year(2016).get("Return on Assets"),
            ], "pct"],
            'Return on Equity': [[
                self.quarter(2020, "Q2").get("Return on Equity"),
                self.quarter(2020, "Q1").get("Return on Equity"),
                self.year(2019).get("Return on Equity"),
                self.year(2018).get("Return on Equity"),
                self.year(2017).get("Return on Equity"),
                self.year(2016).get("Return on Equity"),
            ], "pct"],
            'Debt Equity Ratio': [[
                self.quarter(2020, "Q2").get("Debt Equity Ratio"),
                self.quarter(2020, "Q1").get("Debt Equity Ratio"),
                self.year(2019).get("Debt Equity Ratio"),
                self.year(2018).get("Debt Equity Ratio"),
                self.year(2017).get("Debt Equity Ratio"),
                self.year(2016).get("Debt Equity Ratio"),
            ], "ratio"],
            'Interest Coverage': [[
                self.quarter(2020, "Q2").get("Interest Coverage"),
                self.quarter(2020, "Q1").get("Interest Coverage"),
                self.year(2019).get("Interest Coverage"),
                self.year(2018).get("Interest Coverage"),
                self.year(2017).get("Interest Coverage"),
                self.year(2016).get("Interest Coverage"),
            ], "ratio"],
            'Price To Book Ratio': [[
                self.quarter(2020, "Q2").get("Price To Book Ratio"),
                self.quarter(2020, "Q1").get("Price To Book Ratio"),
                self.year(2019).get("Price To Book Ratio"),
                self.year(2018).get("Price To Book Ratio"),
                self.year(2017).get("Price To Book Ratio"),
                self.year(2016).get("Price To Book Ratio"),
            ], "ratio"],
            'Current Ratio': [[
                self.quarter(2020, "Q2").get("Current Ratio"),
                self.quarter(2020, "Q1").get("Current Ratio"),
                self.year(2019).get("Current Ratio"),
                self.year(2018).get("Current Ratio"),
                self.year(2017).get("Current Ratio"),
                self.year(2016).get("Current Ratio"),
            ], "ratio"],
            # 'Free Cash Flow Ratio': [[
            #     stock.metrics.freeCashFlowRatio().quarter(2020, "Q2"),
            #     stock.metrics.freeCashFlowRatio().quarter(2020, "Q1"),
            #     stock.metrics.freeCashFlowRatio().year(2019),
            #     stock.metrics.freeCashFlowRatio().year(2018),
            #     stock.metrics.freeCashFlowRatio().year(2017),
            #     stock.metrics.freeCashFlowRatio().year(2016),
            # ], "ratio"],
        }