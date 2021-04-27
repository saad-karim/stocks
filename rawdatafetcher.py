from api.api import Annual, Quarter
import time


class RawDataFetcher:

    def __init__(self, api, years, translator):
        self.api = api
        self.years = years
        self.translator = translator

    # Price
    def price(self, symb):
        return self.api.price(symb)

    # Balance Sheet
    def yearlyBalanceSheet(self, symb):
        resp = self.api.balanceSheet(symb, Annual, self.years)
        return self.translator.balanceSheet.yearly(resp)

    def quarterlyBalanceSheet(self, symb):
        resp = self.api.balanceSheet(symb, Quarter, self.years)
        return self.translator.balanceSheet.quarterly(resp)

    # Income
    def yearlyIncome(self, symb):
        resp = self.api.income(symb, Annual, self.years)
        return self.translator.income.yearly(resp)

    def quarterlyIncome(self, symb):
        resp = self.api.income(symb, Quarter, self.years)
        return self.translator.income.quarterly(resp)

    # Cash Flow
    def yearlyCashFlow(self, symb):
        resp = self.api.cashFlow(symb, Annual, self.years)
        return self.translator.cashFlow.yearly(resp)

    def quarterlyCashFlow(self, symb):
        resp = self.api.cashFlow(symb, Quarter, self.years)
        return self.translator.cashFlow.quarterly(resp)

    # Dividend
    def yearlyDividend(self, symb):
        resp = self.api.dividend(symb, str(self.years)+"y")
        return self.translator.dividend.yearly(resp)

    def quarterlyDividend(self, symb):
        resp = self.api.dividend(symb, str(self.years)+"y")
        return self.translator.dividend.quarterly(resp)

    # Advanced
    def yearlyAdvanceFundamentals(self, symb):
        resp = self.api.advanceFundamentals(symb, Annual, self.years)
        return self.translator.advancedFundamentals.yearly(resp)

    def yearlyFinancialRatios(self, symb):
        resp = self.api.financialRatios(symb, Annual, self.years)
        return resp

    # Realtime
    # Quote data
    def quote(self, symb):
        resp = self.api.quote(symb)
        return resp

    # dcf
    def dcf(self, symb):
        return self.api.dcf(symb)
