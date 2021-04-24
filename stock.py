from metrics import Metrics
from data.raw.core.income import Income
from data.raw.core.balancesheet import BalanceSheet
from data.raw.core.cashflow import CashFlow
from data.raw.core.dividend import Dividend
from data.raw.realtime.price import Price
from data.raw.realtime.quote import Quote
from data.raw.advanced.fundamentals import Fundamentals
from data.analytics.trend import Trend
from data.analytics.ratio import Ratio
from data.analytics.analytics import Analytics


class Stock:

    def __init__(self, symb, discountFactor, dataFetcher):
        self.symb = symb
        self.discountFactor = discountFactor
        self.dataFetcher = dataFetcher

        # Realtime data
        self._price = Price()
        self._quote = Quote()

        # Core data
        self._income = Income()
        self._balanceSheet = BalanceSheet()
        self._cashFlow = CashFlow()
        self._dividend = Dividend()

        # Advanced
        self._fundamentals = Fundamentals()

        # Analysis
        self._ratios = Ratio()
        self._analytics = Analytics(self._price, self._quote, self._income,
                                    self._balanceSheet, self._cashFlow)

        self._trends = Trend(self._income, self._balanceSheet,
                             self._cashFlow)

        # self.rawData = RawData(symb, api)
        # self.metrics = Metrics(self.rawData)

    def loadData(self):
        self._price = self._price.parse(
            self.dataFetcher.price(self.symb))

        self._quote.load(
            self.dataFetcher.quote(self.symb))
        self._dcf = self.dataFetcher.dcf(self.symb)

        self._income.yearly().load(
            self.dataFetcher.yearlyIncome(self.symb))
        self._income.quarterly().load(
            self.dataFetcher.quarterlyIncome(self.symb))

        self._cashFlow.yearly().load(
            self.dataFetcher.yearlyCashFlow(self.symb))
        self._cashFlow.quarterly().load(
            self.dataFetcher.quarterlyCashFlow(self.symb))

        self._balanceSheet.yearly().load(
            self.dataFetcher.yearlyBalanceSheet(self.symb))
        self._balanceSheet.quarterly().load(
            self.dataFetcher.quarterlyBalanceSheet(self.symb))

        self._dividend.yearly().load(
            self.dataFetcher.yearlyDividend(self.symb))
        self._dividend.quarterly().load(
            self.dataFetcher.quarterlyDividend(self.symb))

        self._fundamentals.yearly().load(
            self.dataFetcher.yearlyAdvanceFundamentals(self.symb))

    def price(self):
        return self._price

    def income(self):
        return self._income

    def balanceSheet(self):
        return self._balanceSheet

    def cashFlow(self):
        return self._cashFlow

    def dividend(self):
        return self._dividend

    def advancedFundamentals(self):
        return self._fundamentals

    def quote(self):
        return self._quote

    def dcf(self):
        return self._dcf

    def trends(self):
        return self._trends

    def ratios(self):
        return self._ratios

    def analytics(self):
        return self._analytics
