from data.raw.dividend import Dividend
from data.raw.income import Income
from data.raw.balancesheet import BalanceSheet
from data.raw.keystats import KeyStats
from data.raw.advancedkeystats import AdvancedKeyStats
from data.raw.price import Price
from data.raw.financialratios import FinancialRatios
from data.raw.keymetrics import KeyMetrics
from data.raw.cashflow import CashFlow
from data.raw.enterprisevalues import EnterpriseValues
from data.raw.financialgrowth import FinancialGrowth
from data.metrics.growth.price import Price as PriceGrowth
from api.api import Annual, Quarter
from metrics import Metrics
import time

class Stock:

    def __init__(self, symb, api, discountFactor):
        self.api = api
        self.symb = symb
        self.discountFactor = discountFactor

        self.dividend = Dividend()
        self.income = Income()
        self.balanceSheet = BalanceSheet()
        self.keyStats = KeyStats()
        self.advancedKeyStats = AdvancedKeyStats()
        self.price = Price()
        self.ratios = FinancialRatios()
        self.keyMetrics = KeyMetrics()
        self.cashFlow = CashFlow()
        self.enterpriseValues = EnterpriseValues()
        self.financialGrowth = FinancialGrowth()
        self.priceGrowth = PriceGrowth()

    def pullData(self, timeout):
        api = self.api
        symb = self.symb

        # Non-historical data
        self.keyStats.parse(api.keyStats(symb))
        self.advancedKeyStatsResp = api.advancedKeyStats(symb)
        self.priceResp = api.price(symb)

        dividendResp = api.dividend(symb)
        self.dividend.loadYearlyData(dividendResp)
        self.dividend.loadQuarterlyData(dividendResp)

        # Historical data provided on annual and quarterly bases
        self.income.loadYearlyData(api.income(symb, Annual))
        self.income.loadQuarterlyData(api.income(symb, Quarter))

        time.sleep(timeout)

        self.keyMetrics.loadYearlyData(api.keyMetrics(symb, Annual))
        self.keyMetrics.loadQuarterlyData(api.keyMetrics(symb, Quarter))

        time.sleep(timeout)

        self.balanceSheet.loadYearlyData(api.balanceSheet(symb, Annual))
        self.balanceSheet.loadQuarterlyData(api.balanceSheet(symb, Quarter))

        time.sleep(timeout)

        self.ratios.loadYearlyData(api.financialRatios(symb, Annual))
        self.ratios.loadQuarterlyData(api.financialRatios(symb, Quarter))

        time.sleep(timeout)

        self.cashFlow.loadYearlyData(api.cashFlow(symb, Annual))
        self.cashFlow.loadQuarterlyData(api.cashFlow(symb, Quarter))

        time.sleep(timeout)

        self.enterpriseValues.loadYearlyData(api.enterpriseValues(symb, Annual))
        self.enterpriseValues.loadQuarterlyData(api.enterpriseValues(symb, Quarter))

        time.sleep(timeout)

        self.financialGrowth.loadYearlyData(api.financialGrowth(symb, Annual))
        self.financialGrowth.loadQuarterlyData(api.financialGrowth(symb, Quarter))

    def parseMetrics(self):
        # self.metrics = Metrics(self.price.resp, self.advancedKeyStats.resp, self.keyStats.resp, self.income.resps, self.balanceSheet.resps)
        self.metrics = Metrics(self.keyStats.resp, self.income, self.cashFlow)
        metrics = {}
        fcf = self.cashFlow.year(2019)["Free Cash Flow"]
        metrics.update(self.metrics.intrinsicValue(fcf, .03, .06, .10, 10))

        return metrics

    def realtimeData(self):
        m = self.processData()
        return {
            "Ticker": self.symb,
            "Realtime Price": '=GOOGLEFINANCE("{0}", "price")'.format(self.symb),
            "EPS": '=GOOGLEFINANCE("{0}", "eps")'.format(self.symb),
            "PE Ratio": '=GOOGLEFINANCE("{0}", "pe")'.format(self.symb),
            'Price Used for Calculations': [m['Price Used for Calculations'], "money"],
            'Intrinsic Value': [m['Intrinsic Value'], "money"],
            'Shares Outstanding': [m['Shares Outstanding'], "num"],
            'TTM Dividend Yield': [m['TTM Dividend Yield'], "pct"],
            'TTM EPS': [m['TTM EPS'], "money"],
            'TTM Dividend Rate': [m['TTM Dividend'], "money"],
            'Price to Working Capital': [m['Price to Working Capital'], "num"],
            # 'Market Cap / Total Equity',
            # 'Book Value',
            # 'Tangible Book Value / Share',
            # 'Market Capitalization',
            # 'Price/Sales Ratio',
            # 'Total Cash',
            # 'EBITDA',
        }


    def processData(self):
        data = {}

        self.priceGrowth.calc(self.enterpriseValues)

        self.price.parse(self.priceResp)
        price = self.price.output()["Price"]

        ttmDiv = self.dividend.ttm()
        wc = self.keyMetrics.year(2018)["Working Capital"]
        shares = self.keyStats.output()["Shares Outstanding"]

        # print("!!SK >>> price: ", price)
        # print("!!SK >>> wc: ", wc)
        # print("!!SK >>> wc/share: ", (wc / shares))
        # print("!!SK >>> p/wc: ", price / (wc / shares))

        data.update({
            "TTM Dividend Yield": ttmDiv / price,
            "TTM Dividend": ttmDiv,
            "Price to Working Capital": price / (wc / shares),
        })

        ttmEPS = self.income.ttmEPS()
        data.update({
            "TTM EPS": ttmEPS,
        })

        price = self.price.output()
        data.update({
            "Price Used for Calculations": price["Price"],
        })

        data.update(self.keyStats.output()) # Shares outstanding
        # data.update(self.advancedKeyStats.parse(self.advancedKeyStatsResp).output())
        data.update(self.parseMetrics()) # Instrinsic value

        return data