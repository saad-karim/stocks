class Ratio: 

    def __init__(self):
        return
    
    def calc(self, upper, lower):
        ratios = [0, 0, 0, 0]

        if len(upper) != len(lower):
            raise Exception("number of elements in upper and lower must match")

        for i in upper.keys():
            ratios.append(round(upper[i]/lower[i], 2))

        return ratios