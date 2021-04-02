class Translator:

    def __init__(self):
        self.income = _Income()
        self.balanceSheet = _BalanceSheet()
        self.cashFlow = _CashFlow()
        self.dividend = _Dividend()

class _Income:

    def yearly(self, data):
        incomes = data["income"]
        for income in incomes:
            income["quarter"] = 0
            income["date"] = income.pop("fiscalDate")
            income["revenue"] = income.pop("totalRevenue")
        return incomes

    def quarterly(self, data):
        incomes = data["income"]
        for income in incomes:
            income["date"] = income.pop("fiscalDate")
            income["quarter"] = income.pop("fiscalQuarter")
            income["revenue"] = income.pop("totalRevenue")
        return incomes

class _BalanceSheet:

    def yearly(self, data):
        sheets = data["balancesheet"]
        return self._translate(sheets)

    def quarterly(self, data):
        sheets = data["balancesheet"]
        for sheet in sheets:
            sheet["quarter"] = sheet.pop("fiscalQuarter")
        return self._translate(sheets)

    def _translate(self, sheets):
        for sheet in sheets:
            sheet["date"] = sheet.pop("fiscalDate")
            sheet["totalCurrentAssets"] = sheet.pop("currentAssets")
            sheet["totalStockholdersEquity"] = sheet.pop("shareholderEquity")
            sheet["cashAndCashEquivalents"] = sheet.pop("currentCash")
        return sheets
        
class _CashFlow:

    def yearly(self, data):
        flows = data["cashflow"]
        return self._translate(flows)

    def quarterly(self, data):
        flows = data["cashflow"]
        for flow in flows:
            flow["quarter"] = flow.pop("fiscalQuarter")
        return self._translate(flows)

    def _translate(self, flows):
        for flow in flows:
            flow["date"] = flow.pop("fiscalDate")
            flow["investingCashFlow"] = flow.pop("totalInvestingCashFlows")
            flow["financingCashFlow"] = flow.pop("cashFlowFinancing")
        return flows
        
class _Dividend:

    def yearly(self, data):
        return self._translate(data)

    def quarterly(self, data):
        return self._translate(data)

    def _translate(self, data):
        for d in data:
            d["date"] = d.pop("recordDate")
        return data