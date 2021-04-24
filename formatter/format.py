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
        'Current Liabilities': [generate(balancesheet, "Current Liabilities"),"money"],
        'Shareholder Equity': [generate(balancesheet, "Shareholder Equity"), "money"],
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
