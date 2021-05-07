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
import analytics.analytics as analysis
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
        operIncTrend = trend.overallFromDict(self._income.yearly().getKey("Operating Income"))

        self.overallAnalytics = {
            "Net Income": incomeTrend,
            "EPS Trend": epsTrend,
            "FCF Trend": fcfTrend,
            "ROE Trend": roeTrend,
            "BVPS Trend": bvpsTrend,
            "Operating Income Trend": operIncTrend,
        }

    def logisticIndVariables(self):
        deRatio = self._financialRatios.yearly().getKey("Debt Equity Ratio")[2020]
        currRatio = self._financialRatios.yearly().getKey("Current Ratio")[2020]
        roeTrend = trend.overallFromDict(self._financialRatios.yearly().getKey("Return on Equity"))
        roaTrend = trend.overallFromDict(self._financialRatios.yearly().getKey("Return on Assets"))

        dcf = self.dcf()[0].get("dcf")
        iv1 = self.metrics().intrinsicValue()
        iv2 = self.metrics().intrinsicValueDiscountedPerpetuity(self.metrics().fcf(), .10, self.quote().get()["sharesOutstanding"])

        averageIV = statistics.mean([dcf, iv1, iv2])

        price = self._price.price

        interestCoverage = self._financialRatios.yearly().getKey("Interest Coverage")[2020]

        currAssets = self._balanceSheet.yearly().getKey("Current Assets")[2020]
        currLiab = self._balanceSheet.yearly().getKey("Current Liabilities")[2020]
        inventory = self._balanceSheet.yearly().getKey("Inventory")[2020]

        acid = (currAssets - inventory) / currLiab
        payoutRatio = self._financialRatios.yearly().getKey("Payout Ratio")[2020]

        fcfToRevenue = self.metrics().fcf()[0]/self._income.yearly().getKey("Total Revenue")[2020]

        self.logistic = {
            "Debt to Equity Ratio <= 0.5": 1 if deRatio <= 0.5 else 0,
            "Debt to Equity Ratio <= 1.0": 1 if deRatio <= 1.0 else 0,
            "Debt to Equity Ratio <= 1.5": 1 if deRatio <= 1.5 else 0,
            "Debt to Equity Ratio <= 2.0": 1 if deRatio <= 2.0 else 0,
            "Current Ratio >= 1.5": 1 if currRatio >= 1.5 else 0,
            "ROE Trend > 8%": 1 if roeTrend >= 0.08 else 0,
            "ROA Trend > 6%": 1 if roaTrend >= 0.06 else 0,
            "EPS Growth > 2%": 1 if self.overallAnalytics["EPS Trend"] >= .02 else 0,
            "BVPS Growth > 2%": 1 if self.overallAnalytics["BVPS Trend"] >= .02 else 0,
            "PE < 15": 1 if self._quote.get()["pe"] < 15 else 0,
            "Meets Margin (30%)": 1 if averageIV <= (price*.7) else 0,
            "Meets Margin (20%)": 1 if averageIV <= (price*.8) else 0,
            "Meets Margin (10%)": 1 if averageIV <= (price*.9) else 0,
            "Operating Income Growth > 2%": 1 if self.overallAnalytics["Operating Income Trend"] >= .02 else 0,
            "Interest Coverage 5x": 1 if interestCoverage >= 5 else 0,
            "Acid >= 1": 1 if acid >= 1 else 0,
            "Payout Ratio <= 0.6": 1 if payoutRatio <= 0.6 else 0,
            "FCF To Revenue >= 0.05": 1 if fcfToRevenue >= 0.05 else 0,
        }
