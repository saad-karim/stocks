import loader.date as loader
from data.data import Yearly, Quarterly


def translate(raw):
    recordDate = raw["date"]
    year = loader.getDate(recordDate)
    return {
        "Year": year,
        "Current Assets": raw["totalCurrentAssets"],
        "Current Liabilities": raw["totalCurrentLiabilities"],
        "Shareholder Equity": raw["totalStockholdersEquity"],
        "Cash": raw["cashAndCashEquivalents"],
        "Long-Term Debt": raw["longTermDebt"],
        "Common Stock": raw["commonStock"],
        "Retained Earnings": raw["retainedEarnings"],
        "Total Assets": raw["totalAssets"],
        "Total Liabilities": raw["totalLiabilities"],
        "Inventory": raw["inventory"],
        "Treasury Stock": raw["treasuryStock"],
    }


class BalanceSheet:

    _yearly = Yearly(translate)
    _quarterly = Quarterly(translate)

    def __init__(self):
        return

    def yearly(self):
        return self._yearly

    def quarterly(self):
        return self._quarterly

    def allKeys(self, key):
        qtrlyValues = self._quarterly.getKey(key)
        print("q values: ", qtrlyValues)
        yearlyValues = self._yearly.getKey(key)
        print("y values: ", yearlyValues)

        return qtrlyValues.update(yearlyValues)
