import xlsxwriter
import logging
import datetime
import formatter.format

log = logging.getLogger("writer")

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

        qtrs = [currentYearStr+"-Q4", currentYearStr+"-Q3", currentYearStr+"-Q2", currentYearStr+"-Q1"]
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
        # worksheet.write(row, 0, qtrs, self.h2)
        for col_num, qtr in enumerate(qtrs):
            worksheet.write(row-1, col_num+1, qtr, self.h2)

        years = ['Y2Y', 'Y2Y', 'Y2Y', 'Y2Y']
        # worksheet.write(row, 4, years, self.h2)
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

        # Write realtime data
        row = self.writeBlock('Realtime Data', worksheet, row, stock.realtimeData())

        # Write assumption data
        row = self.writeBlock('Assumptions', worksheet, row, formatter.format.price(stock.price()))
 
        # Write core data
        row = self.coreDataHeader('Core Data', worksheet, row)
        row = self.writeBlock('General', worksheet, row, formatter.format.dividend(stock.dividend()))
        row = self.writeBlock('Income', worksheet, row, formatter.format.income(stock.income()))
        row = self.writeBlock('Balance Sheet', worksheet, row, formatter.format.balanceSheet(stock.balanceSheet()))
        row = self.writeBlock('Cash Flow', worksheet, row, formatter.format.cashFlow(stock.cashFlow()), formatter.format.advanced(stock.advancedFundamentals()), stock.calcFCF())

        # Write analysis data
        row = self.analysisDataHeader('Analysis', worksheet, row)
        incomeTrend = stock.trends().netIncome(stock.income().yearly().getKey("Net Income"))
        worksheet.write(row, 10, incomeTrend["overallTrend"], self.pct)
        row = self.writeData(worksheet, row, {"Net Income Trend": [incomeTrend["yearlyTrend"], "pct"]})

        currentRatio = stock.ratios().calc(stock.balanceSheet().yearly().getKey("Current Assets"), stock.balanceSheet().yearly().getKey("Current Liabilities"))
        row = self.writeData(worksheet, row, {"Current Ratio": [currentRatio, "ratio"]})
        row = self.writeData(worksheet, row, {"Net Working Capital": [stock.analytics().netWorkingCapital(), "num"]})
        row = self.writeData(worksheet, row, {"ROIC": [stock.analytics().roic(), "pct"]})
        # row = self.writeData(worksheet, row, {"Net Working Capital": [stock.calNetWorkingCap(), "num"]})
        # row = self.writeData(worksheet, row, {"ROIC": [stock.calcROIC(), "pct"]})

        # row += 2
        # worksheet.write("A{0}".format(row), 'Ratios', self.h3)
        # row = self.writeData(worksheet, row, stock.rawData.ratios.output())
        # row = self.writeData(worksheet, row, stock.rawData.enterpriseValues.output())
        # row = self.writeData(worksheet, row, stock.rawData.keyMetrics.output())

        # row += 2
        # worksheet.write("A{0}".format(row), 'Growth', self.h3)
        # row = self.writeData(worksheet, row, stock.rawData.financialGrowth.output())

        # row += 2
        # worksheet.write("A{0}".format(row), 'Metrics', self.h3)
        # row = self.writeData(worksheet, row, stock.realtimeMetrics())

        self.workbook.close()