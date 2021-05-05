import loader.date as loader


def generate(data, key):
    currentYear = loader.currentYear()
    return [
        data.quarterly().quarter(currentYear, 4).get(key),
        data.quarterly().quarter(currentYear, 3).get(key),
        data.quarterly().quarter(currentYear, 2).get(key),
        data.quarterly().quarter(currentYear, 1).get(key),
        data.yearly().year(currentYear-1).get(key),
        data.yearly().year(currentYear-2).get(key),
        data.yearly().year(currentYear-3).get(key),
        data.yearly().year(currentYear-4).get(key),
        data.yearly().year(currentYear-5).get(key),
    ]


def price(price):
    return {
        'Price Used for Calculations': [[price.resp.get("Price")], "money"],
    }


def quote(quote):
    return {
        'Price': [[quote['price']], 'money'],
        'Market Cap': [[quote['marketCap']], 'money'],
        'EPS': [[quote['eps']], 'num'],
        'PE': [[quote['pe']], 'num'],
        'Shares Outstanding': [[quote['sharesOutstanding']], 'num'],
    }


def dividend(dividend):
    return {
        'Dividend Amount': [generate(dividend, "Amount"), "money"],
    }


def income(income):
    return {
        'Total Revenue': [generate(income, "Total Revenue"), "money"],
        'EBIT': [generate(income, "EBIT"), "money"], 
        'Net Income': [generate(income, "Net Income"), "money"],
        'Gross Profit': [generate(income, "Gross Profit"), "money"],
        'Operating Income': [generate(income, "Operating Income"), "money"],
        'EPS': [generate(income, "EPS"), "money"],
    }


def balanceSheet(balancesheet):
    return {
        'Cash': [generate(balancesheet, "Cash"), "money"],
        'Current Assets': [generate(balancesheet, "Current Assets"), "money"],
        'Current Liabilities': [generate(balancesheet, "Current Liabilities"), "money"],
        'Long-Term Debt': [generate(balancesheet, "Long-Term Debt"), "money"],
        'Total Assets': [generate(balancesheet, "Total Assets"), "money"],
        'Total Liabilities': [generate(balancesheet, "Total Liabilities"), "money"],
        'Shareholder Equity': [generate(balancesheet, "Shareholder Equity"), "money"],
        'Retained Earnings': [generate(balancesheet, "Retained Earnings"), "money"],
        'Inventory': [generate(balancesheet, "Inventory"), "money"],
        'Common Stock': [generate(balancesheet, "Common Stock"), "num"],
    }


def cashFlow(cashFlow):
    return {
        'Capital Expenditures': [generate(cashFlow, "Capital Expenditures"), "money"],
        'Net Change in Cash': [generate(cashFlow, "Net Change in Cash"), "money"],
        'Operating Cash Flow': [generate(cashFlow, "Operating Cash Flow"), "money"],
        'Investing Cash Flow': [generate(cashFlow, "Investing Cash Flow"), "money"],
        'Financing Cash Flow': [generate(cashFlow, "Financing Cash Flow"), "money"],
        # 'Free Cash Flow': [generate(cashFlow, "Free Cash Flow"), "money"],
        # 'Stock BuyBack': [generate(cashFlow, "Stock Buyback"), "money"],
    }


def advanced(fundamentals):
    return {
        'Share Repurchase Cash Flow': [generate(fundamentals, "Share Repurchase Cash Flow"), "money"],
        'Operating Cash Flow': [generate(fundamentals, "Operating Cash Flow"), "money"],
        'Investing Cash Flow': [generate(fundamentals, "Investing Cash Flow"), "money"],
        'Financing Cash Flow': [generate(fundamentals, "Financing Cash Flow"), "money"],
    }


def financialRatios(ratios):
    return {
        'Current Ratio': [generate(ratios, "Current Ratio"), "num"],
        'Quick Ratio': [generate(ratios, "Quick Ratio"), "num"],
        'Gross Profit Margin': [generate(ratios, "Gross Profit Margin"), "num"],
        "Operating Profit Margin": [generate(ratios, "Operating Profit Margin"), "num"],
        "Return on Assets": [generate(ratios, "Return on Assets"), "num"],
        "Return on Equity": [generate(ratios, "Return on Equity"), "num"],
        "Debt Ratio": [generate(ratios, "Debt Ratio"), "num"],
        "Debt Equity Ratio": [generate(ratios, "Debt Equity Ratio"), "num"],
        "Cash Flow to Debt Ratio": [generate(ratios, "Cash Flow to Debt Ratio"), "num"],
        "Price to Book Ratio": [generate(ratios, "Price to Book Ratio"), "num"],
        "Interest Coverage": [generate(ratios, "Interest Coverage"), "num"],
        "Inventory Turnover": [generate(ratios, "Inventory Turnover"), "num"],
        "Receivable Turnover": [generate(ratios, "Receivable Turnover"), "num"],
        "Payables Turnover": [generate(ratios, "Payables Turnover"), "num"],
        "Dividend Payout Ratio": [generate(ratios, "Payout Ratio"), "num"],
    }


def trends(trends):
    return {
        'Net Income Trend': [trends["Net Income Trend"], "pct"],
        'EPS Trend': [trends["EPS Trend"], "pct"],
        'FCF Trend': [trends["FCF Trend"], "pct"],
        'ROE Trend': [trends["ROE Trend"], "pct"],
        'BVPS Trend': [trends["BVPS Trend"], "pct"],
    }


def overallTrends(trends):
    return {
        'Net Income Trend Overall': [trends["Net Income"], "pct"],
        'EPS Trend Overall': [trends["EPS Trend"], "pct"],
        'FCF Trend Overall': [trends["FCF Trend"], "pct"],
        'FCF Trend Overall': [trends["FCF Trend"], "pct"],
        'ROE Trend Overall': [trends["ROE Trend"], "pct"],
        'BVPS Trend Overall': [trends["BVPS Trend"], "pct"],
        'Operating Income Overall': [trends["Operating Income Trend"], "pct"],
    }
