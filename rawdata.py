from data.raw.historical.dividend import Dividend
from data.raw.historical.income import Income
from data.raw.historical.balancesheet import BalanceSheet
from data.raw.historical.financialratios import FinancialRatios
from data.raw.historical.keymetrics import KeyMetrics
from data.raw.historical.cashflow import CashFlow
from data.raw.historical.enterprisevalues import EnterpriseValues
from data.raw.historical.financialgrowth import FinancialGrowth
from data.raw.price import Price
from data.raw.keystats import KeyStats
from data.raw.advancedkeystats import AdvancedKeyStats
from api.api import Annual, Quarter
import time

class RawData:

    def __init__(self, symb, api):
        self.api = api
        self.symb = symb

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

    def pullData(self, timeout):
        api = self.api
        symb = self.symb

        # Non-historical data
        self.keyStats.parse(api.keyStats(symb))
        self.advancedKeyStatsResp = api.advancedKeyStats(symb)
        self.price.parse(api.price(symb))

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