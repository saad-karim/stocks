class MarketCapOverEquity:

    def __init__(self):
        return

    def calc(self, balanceSheet, keyStats):
        capEquity = float(keyStats["Market Capitalization"]) / float(balanceSheet[0]["Shareholder Equity"])
        return {
            "Market Cap / Total Equity": capEquity,
        }
