class EarningsPerShare:

    def __init__(self):
        return

    def calc(self, income, keyStats):
        eps = float(income[0]["Net Income"]) / int(keyStats["Shares Outstanding"])
        return {
            "EPS": eps,
        }
