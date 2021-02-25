class CurrentAssetsOverLiabilities:

    def __init__(self):
        return

    def calc(self, balanceSheet):
        ratio = float(balanceSheet[0]["Current Assets"]) / float(balanceSheet[0]["Current Liabilities"])
        return {
            "Current Assets / Current Liablities": ratio,
        }
