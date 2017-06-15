
import pytest

import datetime

import numpy as np
import pandas as pd
from shapely.geometry import Point

from attrdict import AttrDict
from dtocean_app.data.definitions import (TimeSeries,
                                          NumpyLine,
                                          Histogram,
                                          SimpleDict,
                                          DateTimeDict,
                                          PointDict)


def test_TimeSeries_input(qtbot):
    
    test = TimeSeries()
    test.parent = None
    test.meta = AttrDict({'result': AttrDict({"labels": None, "units": None})})
    
    rng = pd.date_range('1/1/2011', periods=72, freq='H')
    ts = pd.Series(np.random.randn(len(rng)), index=rng)
    test.data = AttrDict({'result': ts})

    test.auto_input(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_NumpyLine_input(qtbot):
    
    test = NumpyLine()
    test.parent = None
    test.meta = AttrDict({'result': AttrDict({"labels": None,
                                              "units": [None, "m"]})})
    
    line = np.array([[0, 0],
                     [1, 2],
                     [2, 2],
                     [3, 3],
                     [4, 4]])
    test.data = AttrDict({'result': line})

    test.auto_input(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_Histogram_input(qtbot):
    
    test = Histogram()
    test.parent = None
    test.meta = AttrDict({'result': AttrDict({"labels": None,
                                              "units": [None, "kg"]})})
    
    hist = {}
    hist['bins'] = [0, 1, 2, 3, 4, 5]
    hist['values'] = [1, 1, 2, 1, 1]
    test.data = AttrDict({'result': hist})

    test.auto_input(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_SimpleDict_input(qtbot):
    
    test = SimpleDict()
    test.parent = None
    test.meta = AttrDict({'result': AttrDict({"labels": None,
                                              "types": [float],
                                              "units": ["kg"],
                                              "valid_values": ["a",
                                                               "b",
                                                               "c"]})})
    
    test_dict = {"a": 1,
                 "b": 2,
                 "c": 3}
    test.data = AttrDict({'result': test_dict})

    test.auto_input(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_SimpleDict_output(qtbot):
    
    test = SimpleDict()
    test.parent = None
    test.meta = AttrDict({'result': AttrDict({"labels": None,
                                              "types": [float],
                                              "units": ["kg"],
                                              "valid_values": ["a",
                                                               "b",
                                                               "c"]})})
    
    test_dict = {"a": 1,
                 "b": 2,
                 "c": 3}
    test.data = AttrDict({'result': test_dict})

    test.auto_output(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True


def test_DateTimeDict_output(qtbot):
    
    test = DateTimeDict()
    test.parent = None
    
    mydict = {"test": datetime.date(1943,3, 13)}
    test.data = AttrDict({'result': mydict})
    
    test.auto_output(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True


def test_PointDict_input(qtbot):
    
    test = PointDict()
    test.parent = None
    test.meta = AttrDict({'result': AttrDict({"valid_values": ["a",
                                                               "b",
                                                               "c"]})})
    
    test_dict = {"a": Point([0, 0]),
                 "b": Point([1, 1]),
                 "c": Point([2, 2])}
    test.data = AttrDict({'result': test_dict})

    test.auto_input(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_PointDict_output(qtbot):
    
    test = PointDict()
    test.parent = None
    test.meta = AttrDict({'result': AttrDict({"valid_values": ["a",
                                                               "b",
                                                               "c"]})})
    
    test_dict = {"a": Point([0, 0]),
                 "b": Point([1, 1]),
                 "c": Point([2, 2])}
    test.data = AttrDict({'result': test_dict})

    test.auto_output(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True


def test_PointDict3D_input(qtbot):
    
    test = PointDict()
    test.parent = None
    test.meta = AttrDict({'result': AttrDict({"valid_values": ["a",
                                                               "b",
                                                               "c"]})})
    
    test_dict = {"a": Point([0, 0, 0]),
                 "b": Point([1, 1, 1]),
                 "c": Point([2, 2, 2])}
    test.data = AttrDict({'result': test_dict})

    test.auto_input(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_PointDict3D_output(qtbot):
    
    test = PointDict()
    test.parent = None
    test.meta = AttrDict({'result': AttrDict({"valid_values": ["a",
                                                               "b",
                                                               "c"]})})
    
    test_dict = {"a": Point([0, 0, 0]),
                 "b": Point([1, 1, 1]),
                 "c": Point([2, 2, 2])}
    test.data = AttrDict({'result': test_dict})

    test.auto_output(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
