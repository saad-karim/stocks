import loader.date as loader
from data.data import Yearly, Quarterly


def translate(raw):
    recordDate = raw["date"]
    year = loader.getDate(recordDate)
    return {
        "Year": year,
        "Quarter": raw["quarter"],
        "Total Revenue": raw["revenue"],
        "EBIT": raw.get("ebit"),
        "Net Income": raw["netIncome"],
        "Gross Profit": raw["grossProfit"],
        "Operating Income": raw["operatingIncome"],
        "Net Income for EPS": raw["netIncomeBasic"],
        # "Interest Expense": raw["interestExpense"],
        # "EPS": raw["eps"],
    }


class Income:

    _yearly = Yearly(translate)
    _quarterly = Quarterly(translate)

    def __init__(self):
        return

    def yearly(self):
        return self._yearly

    def quarterly(self):
        return self._quarterly
