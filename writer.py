import xlsxwriter
import logging
import datetime
import formatter.format

log = logging.getLogger("writer")

class Writer:

    def __init__(self, stock):
        self.symb = stock.symb
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

    def writef(self):
        stock = self.stock

        worksheet = self.workbook.add_worksheet(self.symb)

        worksheet.set_column(0, 10, 20)
        worksheet.write('A1', self.symb, self.h1)
        worksheet.write('A3', 'Realtime Data', self.h2)

        row = 3
        col = 0

        rt = stock.realtimeData()
        for key, value in rt.items():
            worksheet.write(row, col, key, self.bold)

            if isinstance(value, list):
                worksheet.write(row, col + 1, value[0], self.entryType(value[1]))
            else:
                worksheet.write(row, col + 1, value)

            row += 1

        row += 2
        worksheet.write("A{0}".format(row), 'Historical Data', self.h2)

        currentYear = datetime.datetime.now().year
        currentYearStr = str(currentYear)

        qtrs = [currentYearStr+"-Q4", currentYearStr+"-Q3", currentYearStr+"-Q2", currentYearStr+"-Q1"]
        for col_num, qtr in enumerate(qtrs):
            worksheet.write(row-1, col_num+1, qtr, self.h2)

        for x in range(5):
            worksheet.write(row-1, x+len(qtrs)+1, int(currentYear) - x - 1, self.h2)

        row += 2
        worksheet.write("A{0}".format(row), 'General', self.h3)
        # row = self.writeData(worksheet, row, stock.rawData.enterpriseValues.output())
        # row = self.writeData(worksheet, row, stock.rawData.keyMetrics.output())
        row = self.writeData(worksheet, row, formatter.format.dividend(stock.dividend()))

        row += 2
        worksheet.write("A{0}".format(row), 'Income', self.h3)
        row = self.writeData(worksheet, row, formatter.format.income(stock.income()))

        row += 2
        worksheet.write("A{0}".format(row), 'Balance Sheet', self.h3)
        row = self.writeData(worksheet, row, formatter.format.balanceSheet(stock.balanceSheet()))

        row += 2
        worksheet.write("A{0}".format(row), 'Cash Flow', self.h3)
        row = self.writeData(worksheet, row, formatter.format.cashFlow(stock.cashFlow()))

        # row += 2
        # worksheet.write("A{0}".format(row), 'Ratios', self.h3)
        # row = self.writeData(worksheet, row, stock.rawData.ratios.output())

        # row += 2
        # worksheet.write("A{0}".format(row), 'Growth', self.h3)
        # row = self.writeData(worksheet, row, stock.rawData.financialGrowth.output())

        # row += 2
        # worksheet.write("A{0}".format(row), 'Metrics', self.h3)
        # row = self.writeData(worksheet, row, stock.realtimeMetrics())

        self.workbook.close()

    def write(self, rt, hd, symb):
        filename = "./output/" + symb + ".xls"
        log.info("Writing to file %s", filename)

        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet(symb)

        worksheet.set_column(0, 10, 20)

        bold = workbook.add_format({'bold': True})
        num = workbook.add_format({'num_format': '#,##0.00'})
        money = workbook.add_format({'num_format': '$#,##0.00'})
        ratio = workbook.add_format({'num_format': '#,##0.00'})
        pct = workbook.add_format({'num_format': '0.00%'})

        worksheet.write('A1', symb)
        worksheet.write('A3', 'Realtime Data', bold)

        row = 3
        col = 0

        def entryType(type):
            if type == "money":
                return money
            if type == "ratio":
                return ratio
            if type == "pct":
                return pct
            if type == "num":
                return num

        for key, value in rt.items():
            worksheet.write(row, col, key, bold)

            if isinstance(value, list):
                worksheet.write(row, col + 1, value[0], self.entryType(value[1]))
            else:
                worksheet.write(row, col + 1, value)

            row += 1

        row += 2
        worksheet.write("A{0}".format(row), 'Historical Data', bold)

        currentYear = datetime.datetime.now().year
        currentYearStr = str(currentYear)

        # qtrs = [currentYearStr+"-Q4", currentYearStr+"-Q3", currentYearStr+"-Q2", currentYearStr+"-Q1"]
        qtrs = [currentYearStr+"-Q2", currentYearStr+"-Q1"]
        for col_num, qtr in enumerate(qtrs):
            worksheet.write(row, col_num+1, qtr, bold)

        for x in range(5):
            worksheet.write(row, x+len(qtrs)+1, int(currentYear) - x - 1, bold)
        # years = [2019, 2018, 2017, 2016, 2015]
        # for col_num, year in enumerate(years):
        #     worksheet.write(row, col_num+5, year, bold)

        row += 1
        for key, values in hd.items():
            col = 0
            worksheet.write(row, col, key, bold)
            col = 1

            fmt = ""
            if len(values) == 2:
                fmt = values[1]
                values = values[0]

            for value in values:
                worksheet.write(row, col, value, entryType(fmt))
                col += 1

            row += 1

        workbook.close()
