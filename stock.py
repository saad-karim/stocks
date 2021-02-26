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
        # self.metrics = Metrics(self.price.resp, self.advancedKeyStats.resp, self.keyStats.resp, self.income.resps, self.balanceSheet.resps)
        fcf = self.rawData.cashFlow.year(2019)["Free Cash Flow"]

        metrics = {}
        metrics.update(self.metrics.intrinsicValue(fcf, .03, .06, .10, 10))

        return metrics

    def realtimeData(self):
        price = self.rawData.price.output()["Price"]

        ttmDiv = self.metrics.ttmDividend()
        ttmEPS = self.metrics.ttmEPS()

        rtMetrics = self.realtimeMetrics()

        data = {
            'Ticker': self.symb,
            'Realtime Price': '=GOOGLEFINANCE("{0}", "price")'.format(self.symb),
            'EPS': '=GOOGLEFINANCE("{0}", "eps")'.format(self.symb),
            'PE Ratio': '=GOOGLEFINANCE("{0}", "pe")'.format(self.symb),
            'Price Used for Calculations': [price, "money"],
            'Intrinsic Value': [rtMetrics['Intrinsic Value'], "money"],
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

    # def processData(self):
    #     rawData = self.rawData

    #     data = {}

    #     # rawData.price.parse(self.priceResp)

    #     # print("!!SK >>> price: ", price)
    #     # print("!!SK >>> wc: ", wc)
    #     # print("!!SK >>> wc/share: ", (wc / shares))
    #     # print("!!SK >>> p/wc: ", price / (wc / shares))



    #     data.update({
    #         "Price Used for Calculations": price,
    #     })

    #     data.update(rawData.keyStats.output()) # Shares outstanding
    #     # data.update(self.advancedKeyStats.parse(self.advancedKeyStatsResp).output())
    #     data.update(self.parseMetrics()) # Instrinsic value

    #     return data