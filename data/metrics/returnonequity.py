class ReturnOnEquity:

    def __init__(self):
        return

    def calc(self, balanceSheet, income):
        resp = {}

        for i in range(len(income)):
            bookValue = float(income[i]["Net Income"]) / float(balanceSheet[i]["Shareholder Equity"])
            key = "ROE - Year " + str(income[i]["Year"])
            resp.update(
                {
                    key: bookValue,
                })

        return resp
