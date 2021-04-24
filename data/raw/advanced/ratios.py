import loader.date as loader


def buildRatio(raw):
    year = loader.getDate(raw["date"])
    return {
        "Year": year,
        "Current Ratio": raw.get("currentRatio"),
    }


class Yearly:

    _ratios = {}

    def __init__(self):
        return

    def load(self, data):
        for raw in data:
            ratio = buildRatio(raw)
            self._ratios[ratio["Year"]] = ratio

    def year(self, year):
        if year in self._ratios:
            return self._ratios[year]

        return {}

    def allYears(self):
        return self._ratios

    def getKey(self, key):
        resp = {}
        for year, r in self._ratios.items():
            resp.update({year: r[key]})
        return resp

class Quarterly:

    __sheets = {}

    def __init__(self):
        return

    def load(self, sheets):
        return

    def data(self, sheet):
        return

    def quarter(self, year, qtr):
        if year in self.__sheets:
            if qtr in self.__sheets[year]:
                return self.__sheets[year][qtr]

        return {}

    def allQtrs(self):
        return self.__sheets


class Ratios:

    _yearly = Yearly()
    _quarterly = Quarterly()

    def __init__(self):
        return

    def yearly(self):
        return self._yearly

    def quarterly(self):
        return self._quarterly
