def calcRatio(self, upper, lower):
    ratios = []

    if len(upper) != len(lower):
        raise Exception("number of elements in upper and lower must match")

    for i in upper.keys():
        ratios.append(round(upper[i]/lower[i], 2))

    return ratios