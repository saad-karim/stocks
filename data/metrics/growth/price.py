import datetime

# def genRespWithYear(raw, year):
#     return {
#         "Year": year,
#         "Price Growth": raw["priceGrowth"],
#     }

# def getDate(dateStr):
#     date = datetime.datetime.strptime(dateStr, "%Y-%m-%d")
#     return date.year

# class Yearly:

#     values = {}

#     def __init__(self, enterpriseValues):
#         return

#     def load(self, values):
#         for value in values:
#             resp = self.data(value)
#             self.values[resp["Year"]] = resp

#     def data(self, value):
#         recordDate = value["date"]
#         year = getDate(recordDate)
#         return genRespWithYear(value, year)

#     def year(self, year):
#         return self.values[year]

# class Quarterly:

#     currentYear = datetime.datetime.now().year
#     values = {
#         currentYear: {},
#     }

#     def __init__(self, enterpricesValues):
#         return

#     def load(self, values):
#         for value in values:
#             resp = self.data(value)
#             if resp != None:
#                 self.values[self.currentYear][resp["Quarter"]] = resp

#     def data(self, value):
#         recordDate = value["date"]
#         year = getDate(recordDate)
#         if year == self.currentYear:
#             qtr = genRespWithYear(value, year)
#             qtr["Quarter"] = value["period"]
#             return qtr

#     def quarter(self, year, qtr):
#         if qtr in self.values[year]:
#             return self.values[year][qtr]

#         return {}

class Price:

    # yearly = Yearly()
    # quarterly = Quarterly()
    yearlyGrowth = {}

    def __init__(self):
        return

    def calc(self, ev):
        for year in ev.allYears():
            price = ev.year(year)["Stock Price"]
            # print("price: ", price)

            prevYear = year - 1
            if prevYear in ev.allYears().keys():
                prevYearPrice = ev.year(year-1)["Stock Price"]
                # print("prev year price: ", prevYearPrice)

                priceDiff = price - prevYearPrice
                # print("price diff: ", priceDiff)

                growth = priceDiff / prevYearPrice
                # print("growth: ", growth)

                self.yearlyGrowth[year] = {
                    "Year": year,
                    "Price Growth": growth
                }

    def year(self, year):
        return self.yearlyGrowth[year]

    # def loadYearlyData(self, values):
    #     self.yearly.load(values)
    #     return self

    # def loadQuarterlyData(self, values):
    #     self.quarterly.load(values)
    #     return self

    # def quarter(self, year, qtr):
    #     return self.quarterly.quarter(year, qtr)

    # def year(self, year):
    #     return self.yearly.year(year)

