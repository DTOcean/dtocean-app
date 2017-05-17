
import pytest

import datetime

import numpy as np
import pandas as pd

from attrdict import AttrDict
from dtocean_app.data.definitions import TimeSeries, DateTimeDict

def test_TimeSeries_input(qtbot):
    
    test = TimeSeries()
    test.parent = None
    test.meta = AttrDict({'result': AttrDict({"labels": None, "units": None})})
    
    rng = pd.date_range('1/1/2011', periods=72, freq='H')
    ts = pd.Series(np.random.randn(len(rng)), index=rng)
    test.data = AttrDict({'result': ts})

    test.auto_input(test)
    widget = test.data.result
    qtbot.addWidget(widget)
    
    assert True
    
def test_DateTimeDict_output(qtbot):
    
    test = DateTimeDict()
    test.parent = None
    
    mydict = {"test": datetime.date(1943,3, 13)}
    test.data = AttrDict({'result': mydict})
    
    test.auto_output(test)
    widget = test.data.result
    qtbot.addWidget(widget)
    
    assert True
    
