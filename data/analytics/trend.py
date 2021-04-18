class Trend: 

    def __init__(self):
        return
    
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


        overallTrend = (point[0] - point[len(point)-1])/point[len(point)-1]

        trending = [0,0,0,0]
        trending.extend(trend)
        return {
            "yearlyTrend": trending,
            "overallTrend": round(overallTrend, 2),
        }