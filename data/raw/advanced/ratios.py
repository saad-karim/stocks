import loader.date as loader
from data.data import Yearly, Quarterly


def translate(raw):
    year = loader.getDate(raw["date"])
    return {
        "Year": year,
        "Current Ratio": raw.get("currentRatio"),
        "Quick Ratio": raw.get("quickRatio"),
        "Gross Profit Margin": raw.get("grossProfitMargin"),
        "Operating Profit Margin": raw.get("operatingProfitMargin"),
        "Net Income Margin": raw.get("netProfitMargin"),
        "Return on Assets": raw.get("returnOnAssets"),
        "Return on Equity": raw.get("returnOnEquity"),
        "Debt Ratio": raw.get("debtRatio"), # Total Liabilities / Total Assets
        "Debt Equity Ratio": raw.get("debtEquityRatio"), # Total Debt / Total Equity
        "Cash Flow to Debt Ratio": raw.get("cashFlowToDebtRatio"),
        "Price to Book Ratio": raw.get("priceToBookRatio"),
        "Interest Coverage": raw.get("interestCoverage"),
        "Inventory Turnover": raw.get("inventoryTurnover"),
        "Receivables Turnover": raw.get("receivablesTurnover"),
        "Payables Turnover": raw.get("payablesTurnover"),
        "Payout Ratio": raw.get("payoutRatio"),
    }


class Ratios:

    _yearly = Yearly(translate)
    _quarterly = Quarterly(translate)

    def __init__(self):
        return

    def yearly(self):
        return self._yearly

    def quarterly(self):
        return self._quarterly
