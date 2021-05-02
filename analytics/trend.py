import pandas as pd


def extractOnKey(data):
    point = []
    for d in data.values():
        point.append(d)
    return point


def overallFromDict(data):
    points = extractOnKey(data)
    return overall(points)


def overall(data):
    data.reverse()

    series = pd.Series(data)
    chg = series.pct_change()

    return chg.mean()


def calcFromDict(data):
    points = extractOnKey(data)
    return calc(points)


def calc(data):
    data.reverse()

    series = pd.Series(data)
    chg = series.pct_change()

    t = chg.tolist()[1:]
    t.reverse()

    trending = [None, None, None, None]
    trending.extend(t)

    return trending
