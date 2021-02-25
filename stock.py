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
from metrics import Metrics

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

    def pullData(self):
        api = self.api
        symb = self.symb

        self.keyStatsResp = api.keyStats(symb)
        self.advancedKeyStatsResp = api.advancedKeyStats(symb)
        self.priceResp = api.price(symb)

        self.dividendResp = api.dividend(symb)

        self.incomeResp = api.income(symb, "annual")
        self.incomeQtrResp = api.income(symb, "quarter")

        self.balanceSheetResp = api.balanceSheet(symb, "annual")
        self.balanceSheetQtrResp = api.balanceSheet(symb, "quarter")

        self.ratiosResp = api.financialRatios(symb, "annual")
        self.ratiosQtrResp = api.financialRatios(symb, "quarter")

        self.keyMetricsResp = api.keyMetrics(symb, "annual")
        self.keyMetricsQtrResp = api.keyMetrics(symb, "quarter")

        self.cashFlowResp = api.cashFlow(symb, "annual")
        self.cashFlowQtrResp = api.cashFlow(symb, "quarter")

        self.enterpriseValuesResp = api.enterpriseValues(symb, "annual")
        self.enterpriseValuesQtrResp = api.enterpriseValues(symb, "quarter")

        self.financialGrowthResp = api.financialGrowth(symb, "annual")
        self.financialGrowthQtrResp = api.financialGrowth(symb, "quarter")

    def parseMetrics(self):
        # self.metrics = Metrics(self.price.resp, self.advancedKeyStats.resp, self.keyStats.resp, self.income.resps, self.balanceSheet.resps)
        self.metrics = Metrics(self.keyStats.resp, self.income, self.cashFlow)
        metrics = {}
        fcf = self.cashFlow.year(2019)["Free Cash Flow"]
        metrics.update(self.metrics.intrinsicValue(fcf, .03, .06, .10, 10))


        return metrics

    def getData(self):
        data = {
            "Ticker": self.symb,
            "Realtime Price": '=GOOGLEFINANCE("{0}", "price")'.format(self.symb),
            "EPS": '=GOOGLEFINANCE("{0}", "eps")'.format(self.symb),
            "PE Ratio": '=GOOGLEFINANCE("{0}", "pe")'.format(self.symb),
        }

        self.income.loadYearlyData(self.incomeResp)
        self.income.loadQuarterlyData(self.incomeQtrResp)

        self.keyMetrics.loadYearlyData(self.keyMetricsResp)
        self.keyMetrics.loadQuarterlyData(self.keyMetricsQtrResp)

        self.balanceSheet.loadYearlyData(self.balanceSheetResp)
        self.balanceSheet.loadQuarterlyData(self.balanceSheetQtrResp)

        self.ratios.loadYearlyData(self.ratiosResp)
        self.ratios.loadQuarterlyData(self.ratiosQtrResp)

        self.dividend.loadYearlyData(self.dividendResp)
        self.dividend.loadQuarterlyData(self.dividendResp)

        self.cashFlow.loadYearlyData(self.cashFlowResp)
        self.cashFlow.loadQuarterlyData(self.cashFlowQtrResp)

        self.enterpriseValues.loadYearlyData(self.enterpriseValuesResp)
        self.enterpriseValues.loadQuarterlyData(self.enterpriseValuesQtrResp)

        self.financialGrowth.loadYearlyData(self.financialGrowthResp)
        self.financialGrowth.loadQuarterlyData(self.financialGrowthQtrResp)

        self.priceGrowth.calc(self.enterpriseValues)

        self.price.parse(self.priceResp)
        price = self.price.output()["Price"]

        self.keyStats.parse(self.keyStatsResp)

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

        # data.update(self.keyStats.parse(self.keyStatsResp).output())
        data.update(self.keyStats.output())
        data.update(self.advancedKeyStats.parse(self.advancedKeyStatsResp).output())
        data.update(self.parseMetrics())


        return data
