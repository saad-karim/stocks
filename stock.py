from metrics import Metrics
from rawdata import RawData

class Stock:

    def __init__(self, symb, api, discountFactor):
        self.api = api
        self.symb = symb
        self.discountFactor = discountFactor

        self.rawData = RawData(symb, api)
        self.metrics = Metrics(self.rawData)

    def pullData(self, timeout):
        self.rawData.pullData(timeout)

    def realtimeMetrics(self):
        fcf = self.rawData.cashFlow.year(2019)["Free Cash Flow"]

        trend = self.metrics.outstandingSharesTrend()
        iv = self.metrics.intrinsicValue(fcf, .03, .06, .10, 10)

        metrics = {
            "Shares Outstanding Trend": [trend, "num"],
            "Intrinsic Value": [iv, "money"],
        }
        
        return metrics

    def realtimeData(self):
        price = self.rawData.price.output()["Price"]

        ttmDiv = self.metrics.ttmDividend()
        ttmEPS = self.metrics.ttmEPS()

        data = {
            'Ticker': self.symb,
            'Realtime Price': '=GOOGLEFINANCE("{0}", "price")'.format(self.symb),
            'EPS': '=GOOGLEFINANCE("{0}", "eps")'.format(self.symb),
            'PE Ratio': '=GOOGLEFINANCE("{0}", "pe")'.format(self.symb),
            'Price Used for Calculations': [price, "money"],
            'Shares Outstanding': [self.rawData.keyStats.output()["Shares Outstanding"], "num"],
            'TTM Dividend Yield': [ttmDiv['TTM Dividend Yield'], "pct"],
            'TTM Dividend Rate': [ttmDiv['TTM Dividend'], "money"],
            'Price to Working Capital': [ttmDiv['Price to Working Capital'], "num"],
            'TTM EPS': [ttmEPS['TTM EPS'], "money"],
            # 'Market Cap / Total Equity',
            # 'Book Value',
            # 'Tangible Book Value / Share',
            # 'Market Capitalization',
            # 'Price/Sales Ratio',
            # 'Total Cash',
            # 'EBITDA',
        }

        return data