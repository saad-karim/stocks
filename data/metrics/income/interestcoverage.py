class InterestCoverage:

    def __init__(self):
        return

    def calc(self, income):
        resp = {}
        for inc in income:
            cov = int(inc["Operating Income"]) / int(inc["Interest Expense"])
            key = "Interest Coverage - Year " + str(inc["Year"])
            resp.update({
                key: cov
            })

        return resp
        # eps = float(income[0]["Net Income"]) / int(keyStats["Shares Outstanding"])
        # return {
        #     "EP

