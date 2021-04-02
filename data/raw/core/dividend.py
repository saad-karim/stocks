import datetime
import loader.date as loader
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
        1: 1,
        2: 1,
        3: 1,
        4: 2,
        5: 2,
        6: 2,
        7: 3,
        8: 3,
        9: 3,
        10: 4,
        11: 4,
        12: 4,
    }

    date = datetime.datetime.strptime(dateStr, "%Y-%m-%d")
    month = date.month
    return qtrs.get(month)

class Yearly:

    __savedDivs = {}

    def __init__(self):
        return

    def load(self, dividends):
        i = 0
        while i < len(dividends):
            div = dividends[i]
            year = getYear(div["date"])

            pos = i+1
            divAmount = Decimal(div["amount"])
            # Peek forward one element at a time until different year found
            for nextDiv in dividends[pos:]:
                nextDivYear = getYear(nextDiv["date"])

                if pos == len(dividends)-1: # If at the last dividend value
                    if year == nextDivYear: # If next dividend is from the same year, sum the values
                        divAmount = divAmount + Decimal(nextDiv["amount"])
                    else: # If next dividend is from different year, start fresh
                        divAmount = Decimal(nextDiv["amount"])

                    self.__savedDivs.update({
                        nextDivYear: {
                            "Amount": divAmount,
                        }
                    })

                if year == nextDivYear:
                    divAmount = divAmount + Decimal(nextDiv["amount"])
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
        if year in self.__savedDivs:
            return self.__savedDivs[year]
        return "n/a"

class Quarterly:

    __savedDivs = {}

    def __init__(self):
        return

    def load(self, dividends):
        i = 0
        while i < len(dividends):
            div = dividends[i]
            year = getYear(div["date"])
            qtr = getQuarter(div["date"])

            saved = self.__savedDivs.get(year)
            if saved == None:
                self.__savedDivs.update({
                    year: {
                        qtr: {
                            "Amount": div["amount"],
                        }
                    }
                })
            else:
                self.__savedDivs[year].update( {
                        qtr: {
                            "Amount": div["amount"],
                        }
                })
            i+=1
        
    def quarter(self, year, qtr):
        if year in self.__savedDivs:
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

    _yearly = Yearly()
    _quarterly = Quarterly()

    def __init__(self):
        return

    def yearly(self):
        return self._yearly

    def quarterly(self):
        return self._quarterly