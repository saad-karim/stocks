# Does not contain any historical data
class KeyStats:

    resp = {}

    def __init__(self):
        return

    def parse(self, keystats):
        resp = self.genResp(keystats)
        self.resp = resp
        return self

    def genResp(self, keystats):
        return {
            "P/E Ratio": keystats["peRatio"],
            "Dividend Yield": keystats["dividendYield"],
            "Market Capitalization": keystats["marketcap"],
            "Shares Outstanding": keystats["sharesOutstanding"],
            "Company Name": keystats["companyName"],
            "TTM EPS": keystats["ttmEPS"],
            "TTM Dividend Rate": keystats["ttmDividendRate"],
        }

    def get(self):
        return self.resp
