import csv

class Formatter:

    stocks = []
    metrics = []
    transformed = []

    def __init__(self):
        return


    def realtimeData(self, stock):
        m = stock.getData()
        return {
            'Ticker': m['Ticker'],
            'Realtime Price': [m['Realtime Price'], "money"],
            'Price Used for Calculations': [m['Price Used for Calculations'], "money"],
            'Intrinsic Value': [m['Intrinsic Value'], "money"],
            'Shares Outstanding': [m['Shares Outstanding'], "num"],
            'PE Ratio': m['PE Ratio'],
            'EPS': m['EPS'],
            'TTM Dividend Yield': [m['TTM Dividend Yield'], "pct"],
            'TTM EPS': [m['TTM EPS'], "money"],
            'TTM Dividend Rate': [m['TTM Dividend'], "money"],
            'Price to Working Capital': [m['Price to Working Capital'], "num"],
            # 'Market Cap / Total Equity',
            # 'Book Value',
            # 'Tangible Book Value / Share',
            # 'Market Capitalization',
            # 'Price/Sales Ratio',
            # 'Total Cash',
            # 'EBITDA',
        }

    def incomeData(self, stock):
        return income(stock)

    def balanceSheetData(self, stock):
        return balanceSheet(stock)

    def cashflowData(self, stock):
        return cashflow(stock)

    def ratioData(self, stock):
        return ratios(stock)

    def growthData(self, stock):
        return growth(stock)

    def historicData(self, stock):
        return {
            'Price': [[
                stock.enterpriseValues.quarter(2020, "Q2").get("Stock Price"),
                stock.enterpriseValues.quarter(2020, "Q1").get("Stock Price"),
                stock.enterpriseValues.year(2019).get("Stock Price"),
                stock.enterpriseValues.year(2018).get("Stock Price"),
                stock.enterpriseValues.year(2017).get("Stock Price"),
                stock.enterpriseValues.year(2016).get("Stock Price"),
            ], "num"],
            'Number of Shares': [[
                stock.enterpriseValues.quarter(2020, "Q2").get("Number of Shares"),
                stock.enterpriseValues.quarter(2020, "Q1").get("Number of Shares"),
                stock.enterpriseValues.year(2019).get("Number of Shares"),
                stock.enterpriseValues.year(2018).get("Number of Shares"),
                stock.enterpriseValues.year(2017).get("Number of Shares"),
                stock.enterpriseValues.year(2016).get("Number of Shares"),
            ], "num"],
            'Market Cap': [[
                stock.keyMetrics.quarter(2020, "Q2").get("Market Cap"),
                stock.keyMetrics.quarter(2020, "Q1").get("Market Cap"),
                stock.keyMetrics.year(2019).get("Market Cap"),
                stock.keyMetrics.year(2018).get("Market Cap"),
                stock.keyMetrics.year(2017).get("Market Cap"),
                stock.keyMetrics.year(2016).get("Market Cap"),
            ], "money"],
            'Shareholders Equity Per Share': [[
                stock.keyMetrics.quarter(2020, "Q2").get("Shareholders Equity Per Share"),
                stock.keyMetrics.quarter(2020, "Q1").get("Shareholders Equity Per Share"),
                stock.keyMetrics.year(2019).get("Shareholders Equity Per Share"),
                stock.keyMetrics.year(2018).get("Shareholders Equity Per Share"),
                stock.keyMetrics.year(2017).get("Shareholders Equity Per Share"),
                stock.keyMetrics.year(2016).get("Shareholders Equity Per Share"),
            ], "money"],
            'Book Value Per Share': [[
                stock.keyMetrics.quarter(2020, "Q2").get("Book Value Per Share"),
                stock.keyMetrics.quarter(2020, "Q1").get("Book Value Per Share"),
                stock.keyMetrics.year(2019).get("Book Value Per Share"),
                stock.keyMetrics.year(2018).get("Book Value Per Share"),
                stock.keyMetrics.year(2017).get("Book Value Per Share"),
                stock.keyMetrics.year(2016).get("Book Value Per Share"),
            ], "money"],
            'Tangible Book Value Per Share': [[
                stock.keyMetrics.quarter(2020, "Q2").get("Tangible Book Value Per Share"),
                stock.keyMetrics.quarter(2020, "Q1").get("Tangible Book Value Per Share"),
                stock.keyMetrics.year(2019).get("Tangible Book Value Per Share"),
                stock.keyMetrics.year(2018).get("Tangible Book Value Per Share"),
                stock.keyMetrics.year(2017).get("Tangible Book Value Per Share"),
                stock.keyMetrics.year(2016).get("Tangible Book Value Per Share"),
            ], "money"],
            'Dividend': [[
                stock.dividend.quarter(2020, "Q2").get("Amount"),
                stock.dividend.quarter(2020, "Q1").get("Amount"),
                stock.dividend.year(2019).get("Amount"),
                stock.dividend.year(2018).get("Amount"),
                stock.dividend.year(2017).get("Amount"),
                stock.dividend.year(2016).get("Amount"),
            ], "money"],
        }

    def output(self):
        for metric in self.metrics:
            print(metric)
