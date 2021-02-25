import loader.date as loader

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

class Yearly:

    __metrics = {}

    def __init__(self):
        return

    def load(self, metrics):
        for metric in metrics:
            resp = self.data(metric)
            self.__metrics[resp["Year"]] = resp

    def data(self, metric):
        recordDate = metric["date"]
        year = loader.getDate(recordDate)
        return genRespWithYear(metric, year)

    def year(self, year):
        return self.__metrics[year]

class Quarterly:

    __metrics = {}
    numOfQtrs = 0

    def __init__(self):
        return

    def load(self, metrics):
        for metric in metrics:
            resp = self.data(metric)
            if resp != None:
                self.__metrics[resp["Year"]] = {
                    resp["Quarter"]: resp,
                }

    def data(self, metric):
        recordDate = metric["date"]
        year = loader.getDate(recordDate)
        qtr = genRespWithYear(metric, year)
        qtr["Quarter"] = "Q"+str(self.numOfQtrs)
        self.numOfQtrs+=1
        return qtr

    def quarter(self, year, qtr):
        if qtr in self.__metrics[year]:
            return self.__metrics[year][qtr]

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
    
    def output(self):
        return {
            'Market Cap': [[
                self.quarter(2020, "Q2").get("Market Cap"),
                self.quarter(2020, "Q1").get("Market Cap"),
                self.year(2019).get("Market Cap"),
                self.year(2018).get("Market Cap"),
                self.year(2017).get("Market Cap"),
                self.year(2016).get("Market Cap"),
            ], "money"],
            'Shareholders Equity Per Share': [[
                self.quarter(2020, "Q2").get("Shareholders Equity Per Share"),
                self.quarter(2020, "Q1").get("Shareholders Equity Per Share"),
                self.year(2019).get("Shareholders Equity Per Share"),
                self.year(2018).get("Shareholders Equity Per Share"),
                self.year(2017).get("Shareholders Equity Per Share"),
                self.year(2016).get("Shareholders Equity Per Share"),
            ], "money"],
            'Book Value Per Share': [[
                self.quarter(2020, "Q2").get("Book Value Per Share"),
                self.quarter(2020, "Q1").get("Book Value Per Share"),
                self.year(2019).get("Book Value Per Share"),
                self.year(2018).get("Book Value Per Share"),
                self.year(2017).get("Book Value Per Share"),
                self.year(2016).get("Book Value Per Share"),
            ], "money"],
            'Tangible Book Value Per Share': [[
                self.quarter(2020, "Q2").get("Tangible Book Value Per Share"),
                self.quarter(2020, "Q1").get("Tangible Book Value Per Share"),
                self.year(2019).get("Tangible Book Value Per Share"),
                self.year(2018).get("Tangible Book Value Per Share"),
                self.year(2017).get("Tangible Book Value Per Share"),
                self.year(2016).get("Tangible Book Value Per Share"),
            ], "money"],
        }
