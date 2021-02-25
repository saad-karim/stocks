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

    # def incomeData(self, stock):
    #     return income(stock)

    # def balanceSheetData(self, stock):
    #     return balanceSheet(stock)

    # def cashflowData(self, stock):
    #     return cashflow(stock)

    # def ratioData(self, stock):
    #     return ratios(stock)

    # def growthData(self, stock):
    #     return growth(stock)

    def output(self):
        for metric in self.metrics:
            print(metric)
