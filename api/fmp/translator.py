import json
import logging
from decimal import Decimal

log = logging.getLogger("iex_translator")

class Translator:

    def __init__(self):
        return

    def dividend(self, raw):
        log.info("Translating dividend...")
        resp = []
        for dividend in raw:
            simple = {
                "recordDate": dividend["recordDate"],
                "amount": Decimal(dividend["amount"]),
                "frequency": dividend["frequency"],
            }
            resp.append(simple)

        return resp

    def income(self, raw):
        log.info("Translating income...")
        resp = []
        for income in raw[:5]:
            simple = {
                "reportDate": income["date"],
                "totalRevenue": income["revenue"],
                "netIncome": income["netIncome"],
                "netIncomeRatio": income["netIncomeRatio"],
                "grossProfit": income["grossProfit"],
                "grossProfitRatio": income["grossProfitRatio"],
                "operatingIncome": income["operatingIncome"],
                "operatingIncomeRatio": income["operatingIncomeRatio"],
                "interestExpense": income["interestExpense"],
                "eps": income["eps"],
            }
            resp.append(simple)

        return resp

    def balanceSheet(self, raw):
        log.info("Translating balance sheet...")
        resp = []
        for balanceSheet in raw[:5]:
            simple = {
                "reportDate": balanceSheet["date"],
                "totalCurrentAssets": balanceSheet["totalCurrentAssets"],
                "totalCurrentLiabilities": balanceSheet["totalCurrentLiabilities"],
                "shareholderEquity": balanceSheet["totalStockholdersEquity"],
            }
            resp.append(simple)

        return resp

    def ratios(self, raw):
        log.info("Translating financial raios...")
        resp = []
        for ratio in raw[:5]:
            simple = {
                "date": ratio["date"],
                "currentRatio": ratio["currentRatio"],
                "grossProfitMargin": ratio["grossProfitMargin"],
                "operatingProfitMargin": ratio["operatingProfitMargin"],
                "netProfitMargin": ratio["netProfitMargin"],
                "returnOnAssets": ratio["returnOnAssets"],
                "returnOnEquity": ratio["returnOnEquity"],
                "debtEquityRatio": ratio["debtEquityRatio"],
                "interestCoverage": ratio["interestCoverage"],
                "priceToBookRatio": ratio["priceToBookRatio"],
                "priceBookValueRatio": ratio["priceBookValueRatio"],
            }
            resp.append(simple)

        return resp

    def keyMetrics(self, raw):
        log.info("Translating key metrics...")
        resp = []
        for stats in raw[:5]:
            simple = {
                "date": stats["date"],
                "tangibleBookValuePerShare": stats["tangibleBookValuePerShare"],
                "shareholdersEquityPerShare": stats["shareholdersEquityPerShare"],
                "marketCap": stats["marketCap"],
                "peRatio": stats["peRatio"],
            }
            resp.append(simple)

        return resp
