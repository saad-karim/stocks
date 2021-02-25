import datetime
from decimal import Decimal

def genRespWithYear(year, date, div):
    return {
        "Year": year,
        "Amount": div,
    }

def getYear(dateStr):
    date = datetime.datetime.strptime(dateStr, "%Y-%m-%d")
    return date.year

def getQuarter(dateStr):
    qtrs = {
        1: "Q1",
        2: "Q1",
        3: "Q1",
        4: "Q2",
        5: "Q2",
        6: "Q2",
        7: "Q3",
        8: "Q3",
        9: "Q3",
        10: "Q4",
        11: "Q4",
        12: "Q4",
    }

    date = datetime.datetime.strptime(dateStr, "%Y-%m-%d")
    month = date.month
    return qtrs.get(month)

class Yearly:

    __savedDivs = {}

    def __init__(self):
        return

    def load(self, dividends):
        h = dividends["historical"]
        i = 0
        while i < len(h):
            div = h[i]
            year = getYear(div["date"])

            pos = i+1
            divAmount = Decimal(div["adjDividend"])
            # Peek forward one element at a time until different year found
            for nextDiv in h[pos:]:
                nextDivYear = getYear(nextDiv["date"])

                if pos == len(h)-1:
                    if year == nextDivYear:
                        divAmount = divAmount + Decimal(nextDiv["adjDividend"])
                    else:
                        divAmount = Decimal(nextDiv["adjDividend"])

                    self.__savedDivs.update({
                        nextDivYear: {
                            "Amount": divAmount,
                        }
                    })

                if year == nextDivYear:
                    divAmount = divAmount + Decimal(nextDiv["adjDividend"])
                    pos+= 1
                else:
                    self.__savedDivs.update({
                        year: {
                            "Amount": divAmount,
                        }
                    })
                    break

            i = pos-1
            i+= 1


    def data(self, income):
        date = income["date"]
        year = getYear(date)
        return genRespWithYear(income, year)

    def year(self, year):
        return self.__savedDivs[year]

class Quarterly:

    __savedDivs = {}

    def __init__(self):
        return

    def load(self, dividends):
        h = dividends["historical"]
        i = 0
        while i < len(h):
            div = h[i]
            year = getYear(div["date"])
            qtr = getQuarter(div["date"])

            saved = self.__savedDivs.get(year)
            if saved == None:
                self.__savedDivs.update({
                    year: {
                        qtr: {
                            "Amount": div["adjDividend"],
                        }
                    }
                })
            else:
                self.__savedDivs[year].update( {
                        qtr: {
                            "Amount": div["adjDividend"],
                        }
                })
            i+=1

    def quarter(self, year, qtr):
        if qtr in self.__savedDivs[year]:
            return self.__savedDivs[year][qtr]

        return {}

    def ttm(self):
        addedQtrs = 0
        total = 0
        for year in self.__savedDivs:
            qtrs = self.__savedDivs.get(year)
            for qtr in qtrs:
                total = total + qtrs[qtr]["Amount"]
                addedQtrs+=1

                if addedQtrs == 4:
                    return total

class Dividend:

    yearlyIncome = Yearly()
    quarterlyIncome = Quarterly()

    def __init__(self):
        return

    def loadYearlyData(self, incomes):
        self.yearlyIncome.load(incomes)
        return self

    def loadQuarterlyData(self, incomes):
        self.quarterlyIncome.load(incomes)
        return self

    def quarter(self, year, qtr):
        return self.quarterlyIncome.quarter(year, qtr)

    def year(self, year):
        return self.yearlyIncome.year(year)

    def ttm(self):
        return self.quarterlyIncome.ttm()

    def output(self):
        return {
            'Dividend': [[
                self.quarter(2020, "Q2").get("Amount"),
                self.quarter(2020, "Q1").get("Amount"),
                self.year(2019).get("Amount"),
                self.year(2018).get("Amount"),
                self.year(2017).get("Amount"),
                self.year(2016).get("Amount"),
            ], "money"],
        }
