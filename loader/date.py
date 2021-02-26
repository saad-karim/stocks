import datetime

def currentYear():
    return datetime.datetime.now().year

def getDate(dateStr):
    date = datetime.datetime.strptime(dateStr, "%Y-%m-%d")
    return date.year

def getQuarter(dateStr):
    date = datetime.datetime.strptime(dateStr, "%Y-%m-%d")
    month = date.month
    if month <= 3:
        return "Q1"
    elif month <= 6:
        return "Q2"
    elif month <= 9:
        return "Q3"
    else:
        return "Q4"