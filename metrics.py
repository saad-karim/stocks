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
import numpy as np

def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]

class Metrics:

    def __init__(self, rawData):
        self.rawData = rawData
        self.priceGrowth = PriceGrowth()

    def intrinsicValue(self, baseCashFlow, longGrowthRate, growthRate, discountRate, n):
        return IntrinsicValue().calc(baseCashFlow, longGrowthRate, growthRate, discountRate, self.rawData.keyStats.get(), n)

    def freeCashFlowRatio(self):
        fcfr = FreeCashFlowRatio()
        fcfr.calc(self.rawData.income, self.rawData.cashflow)
        return fcfr

    def calcPriceGrowth(self):
        return self.priceGrowth.calc(self.rawData.enterpriseValues)

    def ttmDividend(self):
        ttm =  {
            "TTM Dividend Yield": 0,
            "TTM Dividend": 0,
            "Price to Working Capital": 0,
        }
        
        rawData = self.rawData
        ttmDiv = rawData.dividend.ttm()
        price = rawData.price.output()["Price"]

        if ttmDiv != None:
            ttm["TTM Dividend Yield"] = ttmDiv / price
            ttm["TTM Dividend"] = ttmDiv
            
        keyMetrics = rawData.keyMetrics.year(2018)

        wc = 0
        if keyMetrics != None:
            shares = rawData.keyStats.get()["Shares Outstanding"]
            wc = keyMetrics.get("Working Capital")
            ttm["Price to Working Capital"] = price / (wc / shares)

        return ttm
        # return {
        #     "TTM Dividend Yield": ttmDiv / price,
        #     "TTM Dividend": ttmDiv,
        #     # "Price to Working Capital": price / (wc / shares),
        #     "Price to Working Capital": 1,
        # }
    
    def ttmEPS(self):
        ttmEPS = self.rawData.income.ttmEPS()
        return{
            "TTM EPS": ttmEPS,
        }
    
    def outstandingSharesTrend(self): 
        shares = self.rawData.enterpriseValues.getAllValues("Number of Shares")
        shares = remove_values_from_list(shares, 0.0)
        shares = remove_values_from_list(shares, None)
        # list(filter((0.0).__ne__, shares))
        # list(filter((None).__ne__, shares))
        shares.reverse()
        # print("shares: ", shares)
        x = np.arange(0, len(shares))
        y = np.array(shares)
        z = np.polyfit(x, y, 1)
        # print("z:", z)
        # print("{0}x + {1}".format(*z))
        if z[0] < 0:
            return -1

        return 0


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
