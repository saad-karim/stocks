import loader.date as loader
from data.data import Yearly, Quarterly


def translate(raw):
    recordDate = raw["date"]
    year = loader.getDate(recordDate)
    return {
        "Year": year,
        "Operating Cash Flow": raw.get("operatingCashFlow"),
        "Investing Cash Flow": raw.get("investingCashFlow"),
        "Financing Cash Flow": raw.get("financingCashFlow"),
        "Net Change in Cash": raw.get("netChangeInCash"),
        "Capital Expenditures": raw.get("capitalExpenditures"),
    }


class CashFlow():

    _yearly = Yearly(translate)
    _quarterly = Quarterly(translate)

    def __init__(self):
        return

    def yearly(self):
        return self._yearly

    def quarterly(self):
        return self._quarterly
