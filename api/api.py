import api.iex.prod
import api.iex.sandbox
import api.fmp.prod
import translator.iex
from enum import Enum

Annual = "annual"
Quarter = "quarter"


class Sandbox:

    def __init__(self, fmpKey, iexKey, cache, refresh):
        self.fmp = api.fmp.prod.Prod(fmpKey, cache, refresh)
        self.iex = api.iex.sandbox.Sandbox(iexKey, cache, refresh)
        return

    def price(self, symbol):
        return self.iex.price(symbol)

    def dividend(self, symbol, length):
        return self.iex.dividend(symbol, length)

    def income(self, symbol, period, length):
        return self.iex.income(symbol, period, length)

    def balanceSheet(self, symbol, period, length):
        return self.iex.balanceSheet(symbol, period, length)

    def cashFlow(self, symbol, period, length):
        return self.iex.cashFlow(symbol, period, length)

    def advanceFundamentals(self, symbol, period, length):
        return self.iex.advanceFundamentals(symbol, period, length)

    def quote(self, symbol):
        return self.fmp.quote(symbol)

    def dcf(self, symbol):
        return self.fmp.dcf(symbol)


class Prod:

    def __init__(self, fmpKey, iexKey, cache, refresh):
        self.fmp = api.fmp.prod.Prod(fmpKey, cache, refresh)
        # self.iex = api.iex.prod.Prod(iexKey, cache, refresh)
        self.iex = api.iex.sandbox.Sandbox(iexKey, cache, refresh)
        return

    def price(self, symbol):
        return self.iex.price(symbol)

    def dividend(self, symbol):
        return self.fmp.dividend(symbol)

    # def keyStats(self, symbol):
    #     return self.iex.keyStats(symbol)

    # def advancedKeyStats(self, symbol):
    #     return self.iex.advancedKeyStats(symbol)

    def income(self, symbol, period):
        return self.iex.income(symbol, period, 4)

    def balanceSheet(self, symbol, period):
        return self.iex.balanceSheet(symbol, period,
                                     translator.iex.yearlyIncome)

    # def financialRatios(self, symbol, period):
    #     return self.fmp.financialRatios(symbol, period)

    # def keyMetrics(self, symbol, period):
    #     return self.fmp.keyMetrics(symbol, period)

    def cashFlow(self, symbol, period):
        return self.iex.cashFlow(symbol, period)

    # def enterpriseValues(self, symbol, period):
    #     return self.fmp.enterpriseValues(symbol, period)

    # def financialGrowth(self, symbol, period):
    #     return self.fmp.financialGrowth(symbol, period)
