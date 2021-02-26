import loader.date as loader

def generate(data, key):
    currentYear = loader.currentYear()
    return [
        data.quarter(currentYear, "Q4").get(key),
        data.quarter(currentYear, "Q3").get(key),
        data.quarter(currentYear, "Q2").get(key),
        data.quarter(currentYear, "Q1").get(key),
        data.year(currentYear-1).get(key),
        data.year(currentYear-2).get(key),
        data.year(currentYear-3).get(key),
        data.year(currentYear-4).get(key),
        data.year(currentYear-5).get(key),
    ]