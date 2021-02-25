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
        for income in raw["income"]:
            simple = {
                "reportDate": income["reportDate"],
                "totalRevenue": income["totalRevenue"],
                "netIncome": income["netIncome"],
                "grossProfit": income["grossProfit"],
            }
            resp.append(simple)

        return resp

    def balanceSheet(self, raw):
        log.info("Translating balance sheet...")
        resp = []
        for balanceSheet in raw["balancesheet"]:
            simple = {
                "reportDate": balanceSheet["reportDate"],
                "currentAssets": balanceSheet["currentAssets"],
                "totalCurrentLiabilities": balanceSheet["totalCurrentLiabilities"],
                "shareholderEquity": balanceSheet["shareholderEquity"],
                "netTangibleAssets": balanceSheet["netTangibleAssets"],
                "currentCash": balanceSheet["currentCash"],
            }
            resp.append(simple)

        return resp

    def keyStats(self, raw):
        log.info("Translating key stats...")
        simple = {
            "peRatio": raw["peRatio"],
            "dividendYield": raw["dividendYield"],
            "marketcap": raw["marketcap"],
            "sharesOutstanding": raw["sharesOutstanding"],
            "companyName": raw["companyName"],
            "ttmEPS": raw["ttmEPS"],
            "ttmDividendRate": raw["ttmDividendRate"],
        }

        return simple

    def advancedKeyStats(self, raw):
        log.info("Translating advanced key stats...")
        simple = {
            "grossProfit": raw["grossProfit"],
            "profitMargin": raw["profitMargin"],
            "priceToSales": raw["priceToSales"],
            "priceToBook": raw["priceToBook"],
            "debtToEquity": raw["debtToEquity"],
            "totalCash": raw["totalCash"],
            "EBITDA": raw["EBITDA"],
        }

        return simple

    def price(self, price):
        log.info("Translating price...")
        simple = {
            "price": price,
        }

        return simple
