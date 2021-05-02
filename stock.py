import analytics.trend as trend
from data.raw.core.income import Income
from data.raw.core.balancesheet import BalanceSheet
from data.raw.core.cashflow import CashFlow
from data.raw.core.dividend import Dividend
from data.raw.realtime.price import Price
from data.raw.realtime.quote import Quote
from data.raw.advanced.fundamentals import Fundamentals
from data.raw.advanced.ratios import Ratios
from analytics.metrics import Metrics
from analytics.ratio import Ratio
import statistics


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
        self._financialRatios = Ratios()

        # Analysis
        self._ratios = Ratio()
        self._metrics = Metrics(self._price, self._quote, self._income,
                                    self._balanceSheet, self._cashFlow)

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
        self._financialRatios.yearly().load(
            self.dataFetcher.yearlyFinancialRatios(self.symb))

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

    def financialRatios(self):
        return self._financialRatios

    def quote(self):
        return self._quote

    def dcf(self):
        return self._dcf

    # def trends(self):
    #     return self._trends

    def ratios(self):
        return self._ratios

    def metrics(self):
        return self._metrics

    def runSeriesAnalytics(self):
        incomeTrend = trend.calcFromDict(self._income.yearly().getKey("Net Income"))
        epsTrend = trend.calc(self._metrics.eps())
        fcfTrend = trend.calc(self._metrics.fcf())
        roeTrend = trend.calcFromDict(self._financialRatios.yearly().getKey("Return on Equity"))
        bvpsTrend = trend.calc(self._metrics.bvps())

        print("bvps trend: ", bvpsTrend)

        self.seriesAnalytics = {
            "Net Income Trend": incomeTrend,
            "EPS Trend": epsTrend,
            "FCF Trend": fcfTrend,
            "ROE Trend": roeTrend,
            "BVPS Trend": bvpsTrend,
        }

    def runOverallAnalytics(self):
        incomeTrend = trend.overallFromDict(self._income.yearly().getKey("Net Income"))
        epsTrend = trend.overall(self._metrics.eps())
        fcfTrend = trend.overall(self._metrics.fcf())
        roeTrend = trend.overallFromDict(self._financialRatios.yearly().getKey("Return on Equity"))
        bvpsTrend = trend.overall(self._metrics.bvps())

        print("bvps trend: ", bvpsTrend)

        self.overallAnalytics = {
            "Net Income": incomeTrend,
            "EPS Trend": epsTrend,
            "FCF Trend": fcfTrend,
            "ROE Trend": roeTrend,
            "BVPS Trend": bvpsTrend,
        }

    def logisticIndVariables(self):
        deRatio = self._financialRatios.yearly().getKey("Debt Equity Ratio")[2020]
        currRatio = self._financialRatios.yearly().getKey("Current Ratio")[2020]
        roeTrend = trend.overallFromDict(self._financialRatios.yearly().getKey("Return on Equity"))

        dcf = self.dcf()[0].get("dcf")
        iv1 = self.metrics().intrinsicValue()
        iv2 = self.metrics().intrinsicValueDiscountedPerpetuity(self.metrics().fcf(), .10, self.quote().get()["sharesOutstanding"])

        averageIV = statistics.mean([dcf, iv1, iv2])

        margin = self._price.price * .7
        print("margin: ", margin)

        self.logistic = {
            "Debt to Equity Ratio <= 0.5": 1 if deRatio <= 0.5 else 0,
            "Current Ratio >= 1.5": 1 if currRatio >= 1.5 else 0,
            "ROE > 8": 1 if roeTrend >= 0.08 else 0,
            "EPS Growth > 2": 1 if self.overallAnalytics["EPS Trend"] >= 0 else 0,
            "BVPS Growth > 2": 1 if self.overallAnalytics["BVPS Trend"] >= 0 else 0,
            "PE < 15": 1 if self._quote.get()["pe"] < 15 else 0,
            "Meets Margin": 1 if averageIV <= margin else 0,
            # "ROE Trend": 1 if roeTrend > 0 else 0,
        }
