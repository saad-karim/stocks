class TangibleBookValuePerShare:

    def __init__(self):
        return

    def calc(self, balanceSheet, keyStats):
        tngBookValue = float(balanceSheet[0]["Net Tangible Assets"]) / float(keyStats["Shares Outstanding"])
        return {
            "Tangible Book Value / Share": tngBookValue,
        }
