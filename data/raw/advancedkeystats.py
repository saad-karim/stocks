import datetime

class AdvancedKeyStats:

    resp = {}

    def __init__(self):
        return

    def parse(self, keystats):
        resp = self.genResp(keystats)
        self.resp = resp
        return self

    def genResp(self, advKeyStats):
        return {
            "Gross Profit": advKeyStats["grossProfit"],
            "Profit Margin": advKeyStats["profitMargin"],
            "Price/Sales Ratio": advKeyStats["priceToSales"],
            "Price/BookValue Ratio": advKeyStats["priceToBook"],
            "Debt/Equity Ratio": advKeyStats["debtToEquity"],
            "Total Cash": advKeyStats["totalCash"],
            "EBITDA": advKeyStats["EBITDA"],
        }

    def output(self):
        return self.resp
