import logging
import api.iex.sandbox
import api.iex.prod
import api.iex.translator
import api.fmp.translator
import api.fmp.prod
import api.api
import os
import sys
import xlsxwriter
import argparse
from translator.iex import Translator
from stock import Stock
from writer import Writer
from rawdatafetcher import RawDataFetcher

logging.basicConfig(level="INFO")
log = logging.getLogger("main")

key = {}
stockapi = {}
translator = {}

parser = argparse.ArgumentParser()
parser.add_argument('--refresh', default='store_true')
parser.add_argument('--envir', default='prod')
parser.add_argument('--stock')
args = parser.parse_args()

symb = args.stock.upper()
envir = args.envir

refresh = args.refresh
if refresh == "true":
    log.info("Pulling new data for %s", symb)
    refresh = 1
else:
    log.info("Pulling cached data for %s", symb)
    refresh = 0

if envir == "prod":
    fmpKey = os.getenv("FMP_PRODUCTION_KEY")
    iexKey = os.getenv("IEX_PRODUCTION_KEY")
    if key is None:
        raise Exception("production api key not set")
    stockapi = api.api.Prod(fmpKey, iexKey, "./cache/prod", refresh)

if envir == "sandbox":
    fmpKey = os.getenv("FMP_PRODUCTION_KEY")
    iexKey = os.getenv("SANDBOX_KEY")
    if key is None:
        raise Exception("sandbox api key not set")
    stockapi = api.api.Sandbox(fmpKey, iexKey, "./cache", refresh)

# TODO:

# Quantative
# 2. Add historical total debt
# 3. Add chart of historical data
# 6. Debt acquired each year
# 8. Look out and investigate huge jumps in cash from investing activities
# 10. Look for negative operations cash flow and positive
# finance cash flow, bad sign
# - Stock splits
# - Operating Cash Flow per Share
# - Long term debt along side total debt
# - Growth
# - Investing cash flow to operating cash flow ratio (pg. 227)

# Qualatative
# - Management
# - Insurance/Provisions
# - Competitive Advantage
# - Invesment in innovation/research
# - Entering new/creating markets

dataFetcher = RawDataFetcher(stockapi, 5, Translator())
stock = Stock(symb, 10, dataFetcher)
stock.loadData()
stock.runSeriesAnalytics()
stock.runOverallAnalytics()
stock.logisticIndVariables()

# Write gathered data to a properly formatted xls type file
writer = Writer(stock)
writer.write()
