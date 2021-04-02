from metrics import Metrics
from data.raw.core.income import Income
from data.raw.core.balancesheet import BalanceSheet
from data.raw.core.cashflow import CashFlow
from data.raw.core.dividend import Dividend
from data.raw.realtime.price import Price

class Stock:

    def __init__(self, symb, discountFactor, dataFetcher):
        self.symb = symb
        self.discountFactor = discountFactor
        self.dataFetcher = dataFetcher

        # Realtime data
        self._price = Price()

        # Core data
        self._income = Income()
        self._balanceSheet = BalanceSheet()
        self._cashFlow = CashFlow()
        self._dividend = Dividend()

        # self.rawData = RawData(symb, api)
        # self.metrics = Metrics(self.rawData)
    
    def loadData(self):
        self._price = self._price.parse(self.dataFetcher.price(self.symb))

        self._income.yearly().load(self.dataFetcher.yearlyIncome(self.symb))
        self._income.quarterly().load(self.dataFetcher.quarterlyIncome(self.symb))

        self._cashFlow.yearly().load(self.dataFetcher.yearlyCashFlow(self.symb))
        self._cashFlow.quarterly().load(self.dataFetcher.quarterlyCashFlow(self.symb))

        self._balanceSheet.yearly().load(self.dataFetcher.yearlyBalanceSheet(self.symb))
        self._balanceSheet.quarterly().load(self.dataFetcher.quarterlyBalanceSheet(self.symb))

        self._dividend.yearly().load(self.dataFetcher.yearlyDividend(self.symb))
        self._dividend.quarterly().load(self.dataFetcher.quarterlyDividend(self.symb))

    def income(self):
        return self._income

    def balanceSheet(self):
        return self._balanceSheet

    def cashFlow(self):
        return self._cashFlow

    def dividend(self):
        return self._dividend

    def realtimeMetrics(self):
        fcf = self.rawData.cashFlow.year(2019)["Free Cash Flow"]

        # trend = self.metrics.outstandingSharesTrend()
        iv = self.metrics.intrinsicValue(fcf, .03, .06, .10, 10)

        metrics = {
            # "Shares Outstanding Trend": [trend, "num"],
            "Intrinsic Value": [iv, "money"],
        }
        
        return metrics

    def realtimeData(self):
        return {}
        # price = self.rawData.price.output()["Price"]

        # ttmDiv = self.metrics.ttmDividend()
        # ttmEPS = self.metrics.ttmEPS()

        # data = {
        #     'Ticker': self.symb,
        #     'Realtime Price': '=GOOGLEFINANCE("{0}", "price")'.format(self.symb),
        #     'EPS': '=GOOGLEFINANCE("{0}", "eps")'.format(self.symb),
        #     'PE Ratio': '=GOOGLEFINANCE("{0}", "pe")'.format(self.symb),
        #     'Price Used for Calculations': [price, "money"],
        #     'Shares Outstanding': [self.rawData.keyStats.get()["Shares Outstanding"], "num"],
        #     'TTM Dividend Yield': [ttmDiv.get('TTM Dividend Yield'), "pct"],
        #     'TTM Dividend Rate': [ttmDiv.get('TTM Dividend'), "money"],
        #     'Price to Working Capital': [ttmDiv.get('Price to Working Capital'), "num"],
        #     'TTM EPS': [ttmEPS['TTM EPS'], "money"],
        #     # 'Market Cap / Total Equity',
        #     # 'Book Value',
        #     # 'Tangible Book Value / Share',
        #     # 'Market Capitalization',
        #     # 'Price/Sales Ratio',
        #     # 'Total Cash',
        #     # 'EBITDA',
        # }

        # return data