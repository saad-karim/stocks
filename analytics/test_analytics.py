import pytest
from unittest.mock import Mock, MagicMock

from analytics.metrics import Metrics


def test_instrinciValuePureFCF():
    mock = Mock()
    metrics = Metrics(mock, mock, mock, mock, mock)

    fcfs = [76165201897, 61811347617, 67253156353, 53312778451, 52207055865]
    iv = metrics.intrinsicValueDiscountedPerpetuity(fcfs, .10, 16986601373)
    assert round(iv, 2) == 118.59
