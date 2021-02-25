import datetime

def genRespWithYear(raw, year):
    return {
        "Year": year,
        "Book Value Per Share": raw["bookValuePerShare"],
        "Tangible Book Value Per Share": raw["tangibleBookValuePerShare"],
        "Shareholders Equity Per Share": raw["shareholdersEquityPerShare"],
        "Market Cap": raw["marketCap"],
        "PE Ratio": raw["peRatio"],
        "Working Capital": raw["workingCapital"],
    }

def getDate(dateStr):
    date = datetime.datetime.strptime(dateStr, "%Y-%m-%d")
    return date.year

class Yearly:

    metrics = {}

    def __init__(self):
        return

    def load(self, metrics):
        for metric in metrics:
            resp = self.data(metric)
            self.metrics[resp["Year"]] = resp

    def data(self, metric):
        recordDate = metric["date"]
        year = getDate(recordDate)
        return genRespWithYear(metric, year)

    def year(self, year):
        return self.metrics[year]

class Quarterly:

    currentYear = datetime.datetime.now().year
    metrics = {}
    numOfQtrs = 0

    def __init__(self):
        return

    def load(self, metrics):
        for metric in metrics:
            resp = self.data(metric)
            if resp != None:
                self.metrics[resp["Year"]] = {
                    resp["Quarter"]: resp,
                }

    def data(self, metric):
        recordDate = metric["date"]
        year = getDate(recordDate)
        # if year == self.currentYear:
        qtr = genRespWithYear(metric, year)
        qtr["Quarter"] = "Q"+str(self.numOfQtrs)
        self.numOfQtrs+=1
        return qtr

    def quarter(self, year, qtr):
        if qtr in self.metrics[year]:
            return self.metrics[year][qtr]

        return {}

class KeyMetrics:

    yearly = Yearly()
    quarterly = Quarterly()

    def __init__(self):
        return

    def loadYearlyData(self, metrics):
        self.yearly.load(metrics)
        return self

    def loadQuarterlyData(self, metrics):
        self.quarterly.load(metrics)
        return self

    def quarter(self, year, qtr):
        return self.quarterly.quarter(year, qtr)

    def year(self, year):
        return self.yearly.year(year)
