from api.api import Annual, Quarter
import time

class RawDataFetcher:

    def __init__(self, api, translator):
        self.api = api
        self.translator = translator


    ### Price ###
    def price(self, symb):
        return self.api.price(symb)

    ### Balance Sheet ###
    def yearlyBalanceSheet(self, symb):
        resp = self.api.balanceSheet(symb, Annual, 4)
        return self.translator.balanceSheet.yearly(resp)

    def quarterlyBalanceSheet(self, symb):
        resp = self.api.balanceSheet(symb, Quarter, 4)
        return self.translator.balanceSheet.quarterly(resp)

    ### Income ###
    def yearlyIncome(self, symb):
        resp = self.api.income(symb, Annual, 4)
        return self.translator.income.yearly(resp)

    def quarterlyIncome(self, symb):
        resp = self.api.income(symb, Quarter, 4)
        return self.translator.income.quarterly(resp)

    ### Cash Flow ###
    def yearlyCashFlow(self, symb):
        resp = self.api.cashFlow(symb, Annual, 4)
        return self.translator.cashFlow.yearly(resp)

    def quarterlyCashFlow(self, symb):
        resp = self.api.cashFlow(symb, Quarter, 4)
        return self.translator.cashFlow.quarterly(resp)

    ### Dividend ###
    def yearlyDividend(self, symb):
        resp = self.api.dividend(symb, "5y")
        return self.translator.dividend.yearly(resp)

    def quarterlyDividend(self, symb):
        resp = self.api.dividend(symb, "5y")
        return self.translator.dividend.quarterly(resp)