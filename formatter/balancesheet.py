def balanceSheet(stock):
    return {
        'Cash': [[
            stock.balanceSheet.quarter(2020, "Q2").get("Cash"),
            stock.balanceSheet.quarter(2020, "Q1").get("Cash"),
            stock.balanceSheet.year(2019).get("Cash"),
            stock.balanceSheet.year(2018).get("Cash"),
            stock.balanceSheet.year(2017).get("Cash"),
            stock.balanceSheet.year(2016).get("Cash"),
        ], "money"],
        'Current Assets': [[
            stock.balanceSheet.quarter(2020, "Q2").get("Current Assets"),
            stock.balanceSheet.quarter(2020, "Q1").get("Current Assets"),
            stock.balanceSheet.year(2019).get("Current Assets"),
            stock.balanceSheet.year(2018).get("Current Assets"),
            stock.balanceSheet.year(2017).get("Current Assets"),
            stock.balanceSheet.year(2016).get("Current Assets"),
        ], "money"],
        'Current Liabilities': [[
            stock.balanceSheet.quarter(2020, "Q2").get("Current Liabilities"),
            stock.balanceSheet.quarter(2020, "Q1").get("Current Liabilities"),
            stock.balanceSheet.year(2019).get("Current Liabilities"),
            stock.balanceSheet.year(2018).get("Current Liabilities"),
            stock.balanceSheet.year(2017).get("Current Liabilities"),
            stock.balanceSheet.year(2016).get("Current Liabilities"),
        ], "money"],
        'Shareholder Equity': [[
            stock.balanceSheet.quarter(2020, "Q2").get("Shareholder Equity"),
            stock.balanceSheet.quarter(2020, "Q1").get("Shareholder Equity"),
            stock.balanceSheet.year(2019).get("Shareholder Equity"),
            stock.balanceSheet.year(2018).get("Shareholder Equity"),
            stock.balanceSheet.year(2017).get("Shareholder Equity"),
            stock.balanceSheet.year(2016).get("Shareholder Equity"),
        ], "money"],
    }
