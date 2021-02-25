def growth(stock):
    return {
        'EPS Growth': [[
            stock.financialGrowth.quarter(2020, "Q2").get("EPS Growth"),
            stock.financialGrowth.quarter(2020, "Q1").get("EPS Growth"),
            stock.financialGrowth.year(2019).get("EPS Growth"),
            stock.financialGrowth.year(2018).get("EPS Growth"),
            stock.financialGrowth.year(2017).get("EPS Growth"),
            stock.financialGrowth.year(2016).get("EPS Growth"),
        ], "money"],
        'Price Growth': [[
            0,
            0,
            stock.priceGrowth.year(2019).get("Price Growth"),
            stock.priceGrowth.year(2018).get("Price Growth"),
            stock.priceGrowth.year(2017).get("Price Growth"),
            # stock.priceGrowth.year(2016).get("Price Growth"),
        ], "pct"],
    }
