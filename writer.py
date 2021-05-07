import xlsxwriter
import logging
import datetime
import formatter.format
import statistics

log = logging.getLogger("writer")


def pad(output):
    padding = [None, None, None, None]
    padding.extend(output)

    return padding


class Writer:

    def __init__(self, stock):
        self.stock = stock

        filename = "./output/" + stock.symb + ".xls"
        log.info("Writing to file %s", filename)

        self.workbook = xlsxwriter.Workbook(filename)

        self.h1 = self.workbook.add_format({'bold': True, 'font_size': 16})
        self.h2 = self.workbook.add_format({'bold': True, 'font_size': 15})
        self.h3 = self.workbook.add_format({'bold': True, 'font_size': 14, 'bg_color': "#C8EEB5"})
        self.bold = self.workbook.add_format({'bold': True})
        self.num = self.workbook.add_format({'num_format': '#,##0.00'})
        self.money = self.workbook.add_format({'num_format': '$#,##0.00'})
        self.ratio = self.workbook.add_format({'num_format': '#,##0.00'})
        self.pct = self.workbook.add_format({'num_format': '0.00%'})

    def entryType(self, type):
        if type == "money":
            return self.money
        if type == "ratio":
            return self.ratio
        if type == "pct":
            return self.pct
        if type == "num":
            return self.num

    def writeBlock(self, title, worksheet, row, *data):
        row += 2
        worksheet.write("A{0}".format(row), title, self.h3)
        for d in data:
            row = self.writeData(worksheet, row, d)
        return row

    def writeData(self, worksheet, row, data):
        for key, values in data.items():
            col = 0
            worksheet.write(row, col, key, self.bold)

            fmt = ""
            col = 1
            if type(values) is list:
                if len(values) == 2:
                    fmt = values[1]
                    values = values[0]

            if isinstance(values, list):
                for value in values:
                    worksheet.write(row, col, value, self.entryType(fmt))
                    col += 1
            else:
                worksheet.write(row, col, values, self.entryType(fmt))

            row += 1
        return row

    def coreDataHeader(self, title, worksheet, row):
        row += 2
        worksheet.write("A{0}".format(row), title, self.h2)

        currentYear = datetime.datetime.now().year
        currentYearStr = str(currentYear)

        qtrs = [currentYearStr+"-Q4",
                currentYearStr+"-Q3",
                currentYearStr+"-Q2",
                currentYearStr+"-Q1"]
        for col_num, qtr in enumerate(qtrs):
            worksheet.write(row-1, col_num+1, qtr, self.h2)

        for x in range(5):
            worksheet.write(row-1, x+len(qtrs)+1, int(currentYear) - x - 1, self.h2)

        return row

    def analysisDataHeader(self, title, worksheet, row):
        row += 2
        worksheet.write("A{0}".format(row), title, self.h2)

        currentYear = datetime.datetime.now().year
        currentYearStr = str(currentYear)

        qtrs = ['Q2Q', 'Q2Q', 'Q2Q', 'Q2Q']
        for col_num, qtr in enumerate(qtrs):
            worksheet.write(row-1, col_num+1, qtr, self.h2)

        years = ['Y2Y', 'Y2Y', 'Y2Y', 'Y2Y']
        for col_num, year in enumerate(years):
            worksheet.write(row-1, col_num+len(qtrs)+1, year, self.h2)

        worksheet.write(row-1, 10, 'Y2Y Overall', self.h2)

        return row

    def write(self):
        stock = self.stock

        worksheet = self.workbook.add_worksheet(stock.symb)

        worksheet.set_column(0, 10, 20)
        worksheet.write('A1', stock.symb, self.h1)

        col = 0
        row = 1

        dcf = stock.dcf()[0].get("dcf")
        iv1 = stock.metrics().intrinsicValue()
        iv2 = stock.metrics().intrinsicValueDiscountedPerpetuity(stock.metrics().fcf(), .10, stock.quote().get()["sharesOutstanding"])

        averageIV = statistics.mean([dcf, iv1, iv2])

        # Write realtime data
        row = self.writeBlock('Realtime Data', worksheet, row, formatter.format.quote(stock.quote().get()))
        row = self.writeData(worksheet, row, {"DCF": [dcf, "num"]})
        row = self.writeData(worksheet, row, {"NPV Per Stock": [iv1, "num"]})
        row = self.writeData(worksheet, row, {"NPV Per Stock (FCF Only)": [iv2, "num"]})
        row = self.writeData(worksheet, row, {"Average Intrinsic Value": [averageIV, "num"]})

        # Write assumption data
        row = self.writeBlock('Assumptions', worksheet, row, formatter.format.price(stock.price()))

        # Write core data
        row = self.coreDataHeader('Core Data', worksheet, row)
        row = self.writeBlock('General', worksheet, row, formatter.format.dividend(stock.dividend()))
        row = self.writeBlock('Income', worksheet, row, formatter.format.income(stock.income()))
        row = self.writeBlock('Balance Sheet', worksheet, row, formatter.format.balanceSheet(stock.balanceSheet()))
        row = self.writeBlock('Cash Flow', worksheet, row, formatter.format.cashFlow(stock.cashFlow()))

        # Advanced Data
        row = self.coreDataHeader('Advanced Data', worksheet, row)

        # Metrics
        row = self.writeData(worksheet, row, {"Net Working Capital": [pad(stock.metrics().netWorkingCapital()), "num"]})
        row = self.writeData(worksheet, row, {"Free Cash Flow": [pad(stock.metrics().fcf()), "num"]})
        row = self.writeData(worksheet, row, {"Book Value per Share": [pad(stock.metrics().bvps()), "ratio"]})
        row = self.writeData(worksheet, row, {"PBV Ratio": [pad(stock.metrics().pbvRatio()), "ratio"]})
        row = self.writeData(worksheet, row, {"EPS": [pad(stock.metrics().eps()), "ratio"]})
        row = self.writeData(worksheet, row, {"PE Ratio": [pad(stock.metrics().peRatio()), "ratio"]})
        row = self.writeData(worksheet, row, {"ROIC": [pad(stock.metrics().roic()), "pct"]})

        # Ratios
        # currentRatio = stock.ratios().calc(stock.balanceSheet().yearly().getKey("Current Assets"),
        #                                    stock.balanceSheet().yearly().getKey("Current Liabilities"))
        # row = self.writeData(worksheet, row, {"Current Ratio": [currentRatio, "ratio"]})
        row = self.writeBlock('Ratios', worksheet, row, formatter.format.financialRatios(stock.financialRatios()))

        # Write analysis data
        row = self.analysisDataHeader('Analysis', worksheet, row)

        # Trends
        row = self.writeBlock('Trends', worksheet, row, formatter.format.trends(stock.seriesAnalytics))
        row = self.writeBlock('Overall Trends', worksheet, row, formatter.format.overallTrends(stock.overallAnalytics))

        row += 2
        worksheet.write("A{0}".format(row), "Logistic Regression", self.h3)
        row = self.writeBlock('Variables', worksheet, row, stock.logistic)

        # worksheet.write(row, 10, incomeTrend["overallTrend"], self.pct)
        # row = self.writeData(worksheet, row, {"Net Income Trend": [incomeTrend["yearlyTrend"], "pct"]})

        # worksheet.write(row, 10, epsTrend["overallTrend"], self.pct)
        # row = self.writeData(worksheet, row, {"EPS Growth": [epsTrend["yearlyTrend"], "pct"]})

        self.workbook.close()
