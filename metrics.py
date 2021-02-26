from data.metrics.bookvalue import BookValue
from data.metrics.earningspershare import EarningsPerShare
from data.metrics.tangiblebookvaluepershare import TangibleBookValuePerShare
from data.metrics.marketcapoverequity import MarketCapOverEquity
from data.metrics.currentassetsoverliabilities import CurrentAssetsOverLiabilities
from data.metrics.returnonequity import ReturnOnEquity
from data.metrics.intrinsicvalue import IntrinsicValue
from data.metrics.freecashflowratio import FreeCashFlowRatio
from data.metrics.income.interestcoverage import InterestCoverage
from data.metrics.growth.price import Price as PriceGrowth

class Metrics:

    def __init__(self, rawData):
        self.rawData = rawData
        self.priceGrowth = PriceGrowth()

    def intrinsicValue(self, baseCashFlow, longGrowthRate, growthRate, discountRate, n):
        return IntrinsicValue().calc(baseCashFlow, longGrowthRate, growthRate, discountRate, self.rawData.keyStats.output(), n)

    def freeCashFlowRatio(self):
        fcfr = FreeCashFlowRatio()
        fcfr.calc(self.rawData.income, self.rawData.cashflow)
        return fcfr

    def calcPriceGrowth(self):
        return self.priceGrowth.calc(self.rawData.enterpriseValues)

    def ttmDividend(self):
        rawData = self.rawData

        ttmDiv = rawData.dividend.ttm()
        price = rawData.price.output()["Price"]
        wc = rawData.keyMetrics.year(2018)["Working Capital"]
        shares = rawData.keyStats.output()["Shares Outstanding"]

        return {
            "TTM Dividend Yield": ttmDiv / price,
            "TTM Dividend": ttmDiv,
            "Price to Working Capital": price / (wc / shares),
        }
    
    def ttmEPS(self):
        ttmEPS = self.rawData.income.ttmEPS()
        return{
            "TTM EPS": ttmEPS,
        }

    # def __init__(self, price, advKeyStats, keyStats, income, balanceSheet):
    #     self.price = price
    #     self.advKeyStats = advKeyStats
    #     self.keyStats = keyStats
    #     self.income = income
    #     self.balanceSheet = balanceSheet

    # def priceOverBookValue(self):
    #     return BookValue().calc(self.price, self.advKeyStats, self.keyStats)

    # def eps(self):
    #     return EarningsPerShare().calc(self.income, self.keyStats)

    # def tangibleBookValuePerShare(self):
    #     return TangibleBookValuePerShare().calc(self.balanceSheet, self.keyStats)

    # def marketCapOverEquity(self):
    #     return MarketCapOverEquity().calc(self.balanceSheet, self.keyStats)

    # def currentAssetsOverLiabilities(self):
    #     return CurrentAssetsOverLiabilities().calc(self.balanceSheet)

    # def returnOnEquity(self):
    #     return ReturnOnEquity().calc(self.balanceSheet, self.income)

    # def intrinsicValue(self, baseCashFlow, longGrowthRate, growthRate, discountRate, n):
    #     return IntrinsicValue().calc(baseCashFlow, longGrowthRate, growthRate, discountRate, self.keyStats, n)

    # def interestCoverage(self):
    #     return InterestCoverage().calc(self.income)
