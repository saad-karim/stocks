class Yearly:

    def __init__(self, respGen):
        self._data = {}
        self._respGen = respGen

    def load(self, yearlyData):
        result = {}
        respGen = self._respGen

        for data in yearlyData:
            resp = respGen(data)
            result[resp["Year"]] = resp

        self._data = result

    def year(self, year):
        if year in self._data:
            return self._data[year]
        return {}

    def getKey(self, key):
        resp = {}

        for year, data in self._data.items():
            resp.update({year: data[key]})

        return resp


class Quarterly:

    def __init__(self, respGen):
        self._data = {}
        self._respGen = respGen

    def load(self, qtrlyData):
        result = {}
        respGen = self._respGen

        for data in qtrlyData:
            resp = respGen(data)
            resp["Quarter"] = data["quarter"]
            if resp is not None:
                result[resp["Year"]] = {
                    resp["Quarter"]: resp,
                }

        self._data = result

    def quarter(self, year, qtr):
        if year in self._data:
            if qtr in self._data[year]:
                return self._data[year][qtr]

        return {}

    def getKey(self, key):
        resp = {}

        for year in self._data:
            for qtr in self._data[year]:
                print('qtr: ', qtr)
                print('data: ', self._data[year][qtr])
                resp.update({year: self._data[year][qtr][key]})

        return resp

    def allQtrs(self):
        return self._data
