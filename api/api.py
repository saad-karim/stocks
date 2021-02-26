import api.iex.prod
import api.fmp.prod
from enum import Enum

Annual = "annual"
Quarter = "quarter"

class Prod:

    def __init__(self, fmpKey, iexKey, cache, refresh):
        self.fmp = api.fmp.prod.Prod(fmpKey, cache, refresh)
        self.iex = api.iex.prod.Prod(iexKey, cache, refresh)
        return

    def price(self, symbol):
        return self.iex.price(symbol)

    def dividend(self, symbol):
        return self.fmp.dividend(symbol)

    def keyStats(self, symbol):
        return self.iex.keyStats(symbol)

    def advancedKeyStats(self, symbol):
        return self.iex.advancedKeyStats(symbol)

    def income(self, symbol, period):
        return self.fmp.income(symbol, period)

    def balanceSheet(self, symbol, period):
        return self.fmp.balanceSheet(symbol, period)

    def financialRatios(self, symbol, period):
        return self.fmp.financialRatios(symbol, period)

    def keyMetrics(self, symbol, period):
        return self.fmp.keyMetrics(symbol, period)

    def cashFlow(self, symbol, period):
        return self.fmp.cashFlow(symbol, period)

    def enterpriseValues(self, symbol, period):
        return self.fmp.enterpriseValues(symbol, period)

    def financialGrowth(self, symbol, period):
        return self.fmp.financialGrowth(symbol, period)
