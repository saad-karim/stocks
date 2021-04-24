class Trend:

    def __init__(self, inc, bs, cf):
        self._inc = inc
        self._bs = bs
        self._cf = cf
        # self._analytics = analytics

    def netIncome(self, data):
        trend = []
        point = []

        for d in data.values():
            point.append(d)

        for i in range(len(point)):
            if i == len(point)-1:
                break

            current = point[i]
            previous = point[i+1]

            trend.append(round((current-previous)/previous, 2))

        # overallTrend = (point[0] - point[len(point)-1])/point[len(point)-1]
        overallTrend = 0
        for i in trend:
            overallTrend += i

        overallTrend = overallTrend / len(trend)

        trending = [0, 0, 0, 0]
        trending.extend(trend)
        return {
            "yearlyTrend": trending,
            "overallTrend": round(overallTrend, 2),
        }

    # Earnings per share
    def epsGrowth(self, earningspershare):
        point = []
        trend = []

        for eps in earningspershare:
            if eps == 0:
                continue

            point.append(eps)

        for i in range(len(point)):
            if i == len(point)-1:
                break

            current = point[i]
            previous = point[i+1]

            if current == 0:
                continue

            trend.append(round((current-previous)/previous, 2))

        # overallTrend = (point[0] - point[len(point)-1])/point[len(point)-1]
        overallTrend = 0
        for i in trend:
            overallTrend += i

        overallTrend = overallTrend / len(trend)

        trending = [0, 0, 0, 0]
        trending.extend(trend)

        return {
            "yearlyTrend": trending,
            "overallTrend": round(overallTrend, 2),
        }

    def fcfGrowth(self, fcfs):
        point = []
        trend = []

        for fcf in fcfs:
            if fcf == 0:
                continue

            point.append(fcf)

        for i in range(len(point)):
            if i == len(point)-1:
                break

            current = point[i]
            previous = point[i+1]

            if current == 0:
                continue

            trend.append(round((current-previous)/previous, 2))

        overallTrend = 0
        for i in trend:
            overallTrend += i

        overallTrend = overallTrend / len(trend)

        trending = [0, 0, 0, 0]
        trending.extend(trend)

        return {
            "yearlyTrend": trending,
            "overallTrend": round(overallTrend, 2),
        }
