import pytest
from unittest.mock import Mock

from analytics.metrics import Metrics

mock = Mock()


def test_netWorkingCapital():
    balanceSheet = [
        {
            2020: 100,
            2019: 90
        },
        {
            2020: 50,
            2019: 40
        }
    ]

    yearlyMock = Mock()
    yearlyMock.getKey.side_effect = balanceSheet

    bsMock = Mock()
    bsMock.yearly.return_value = yearlyMock
    metrics = Metrics(mock, mock, mock, bsMock, mock)

    nc = metrics.netWorkingCapital()
    assert nc == [50, 50]


def test_roic():
    yearlyBSMock = Mock()

    def bsfunc(key):
        bs = {
            'Current Liabilities': {
                2020: 100,
                2019: 90
            },
            'Long-Term Debt': {
                2020: 50,
                2019: 40
            },
            'Common Stock': {
                2020: 50,
                2019: 40
            },
            'Retained Earnings': {
                2020: 50,
                2019: 40
            }
        }
        return bs[key]

    yearlyBSMock.getKey.side_effect = bsfunc

    bsMock = Mock()
    bsMock.yearly.return_value = yearlyBSMock

    def cffunc(key):
        cf = {
            'Financing Cash Flow': {
                2020: 100,
                2019: 90
            },
            'Investing Cash Flow': {
                2020: 50,
                2019: 40
            },
        }
        return cf[key]

    yearlyCFMock = Mock()
    yearlyCFMock.getKey.side_effect = cffunc

    cfMock = Mock()
    cfMock.yearly.return_value = yearlyCFMock

    yearlyIncMock = Mock()
    yearlyIncMock.getKey.side_effect = [{
        2020: 100,
        2019: 90,
    }]

    incMock = Mock()
    incMock.yearly.return_value = yearlyIncMock

    metrics = Metrics(mock, mock, incMock, bsMock, cfMock)

    roic = metrics.roic()
    assert roic == [0.3, 0.32]


def test_fcf():
    def cffunc(key):
        cf = {
            'Capital Expenditures': {
                2020: -100,
                2019: -90
            },
            'Operating Cash Flow': {
                2020: 150,
                2019: 240
            },
        }
        return cf[key]

    yearlyCFMock = Mock()
    yearlyCFMock.getKey.side_effect = cffunc

    cfMock = Mock()
    cfMock.yearly.return_value = yearlyCFMock

    metrics = Metrics(mock, mock, mock, mock, cfMock)
    fcfs = metrics.fcf()
    assert fcfs == [50, 150]


def test_eps():
    def bsfunc(key):
        bs = {
            'Common Stock': {
                2020: 50,
                2019: 40
            }
        }
        return bs[key]

    yearlyBSMock = Mock()
    yearlyBSMock.getKey.side_effect = bsfunc

    bsMock = Mock()
    bsMock.yearly.return_value = yearlyBSMock

    def incfunc(key):
        inc = {
            'Net Income for EPS': {
                2020: 5000,
                2019: 4440
            }
        }
        return inc[key]

    yearlyIncMock = Mock()
    yearlyIncMock.getKey.side_effect = incfunc

    incMock = Mock()
    incMock.yearly.return_value = yearlyIncMock

    metrics = Metrics(mock, mock, incMock, bsMock, mock)
    eps = metrics.eps()
    assert eps == [100.0, 111.0]


def test_bvps():
    def bsfunc(key):
        bs = {
            'Common Stock': {
                2020: 50,
                2019: 40
            },
            'Shareholder Equity': {
                2020: 502342,
                2019: 434231
            }
        }
        return bs[key]

    yearlyBSMock = Mock()
    yearlyBSMock.getKey.side_effect = bsfunc

    bsMock = Mock()
    bsMock.yearly.return_value = yearlyBSMock

    metrics = Metrics(mock, mock, mock, bsMock, mock)
    bvps = metrics.bvps()
    assert bvps == [10046.84, 10855.77]


def test_pbvRatio():
    def bsfunc(key):
        bs = {
            'Common Stock': {
                2020: 50,
                2019: 40
            },
            'Shareholder Equity': {
                2020: 200,
                2019: 165
            }
        }
        return bs[key]

    yearlyBSMock = Mock()
    yearlyBSMock.getKey.side_effect = bsfunc

    bsMock = Mock()
    bsMock.yearly.return_value = yearlyBSMock

    mockPrice = Mock()
    mockPrice.price = 10

    metrics = Metrics(mockPrice, mock, mock, bsMock, mock)
    pbvRatio = metrics.pbvRatio()
    assert pbvRatio == [2.5, 2.43]


def test_peRatio():
    def bsfunc(key):
        bs = {
            'Common Stock': {
                2020: 50,
                2019: 40
            }
        }
        return bs[key]

    yearlyBSMock = Mock()
    yearlyBSMock.getKey.side_effect = bsfunc

    bsMock = Mock()
    bsMock.yearly.return_value = yearlyBSMock

    def incfunc(key):
        inc = {
            'Net Income for EPS': {
                2020: 500,
                2019: 440
            }
        }
        return inc[key]

    yearlyIncMock = Mock()
    yearlyIncMock.getKey.side_effect = incfunc

    incMock = Mock()
    incMock.yearly.return_value = yearlyIncMock

    mockPrice = Mock()
    mockPrice.price = 10

    metrics = Metrics(mockPrice, mock, incMock, bsMock, mock)
    peRatio = metrics.peRatio()
    assert peRatio == [1.0, 0.91]


def test_instrinicValue():
    def cffunc(key):
        cf = {
            'Capital Expenditures': {
                2020: -100,
                2019: -90,
                2018: -110,
                2017: -75,
                2016: -90,
            },
            'Operating Cash Flow': {
                2020: 150,
                2019: 300,
                2018: 201,
                2017: 243,
                2016: 234,
            },
        }
        return cf[key]

    yearlyCFMock = Mock()
    yearlyCFMock.getKey.side_effect = cffunc

    cfMock = Mock()
    cfMock.yearly.return_value = yearlyCFMock

    quoteMock = Mock()
    quoteMock.get.return_value = {
        'sharesOutstanding': 1000
    }

    metrics = Metrics(mock, quoteMock, mock, mock, cfMock)
    iv = metrics.intrinsicValue()
    assert iv == 1.03


def test_instrinicValuePureFCF():
    metrics = Metrics(mock, mock, mock, mock, mock)

    fcfs = [76165201897, 61811347617, 67253156353, 53312778451, 52207055865]
    iv = metrics.intrinsicValueDiscountedPerpetuity(fcfs, .10, 16986601373)
    assert iv == 118.59
