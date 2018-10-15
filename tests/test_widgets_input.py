# -*- coding: utf-8 -*-

#    Copyright (C) 2016-2018 Mathew Topper
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import pandas as pd

from dtocean_app.widgets.input import (FloatSelect,
                                       StringSelect,
                                       DirectorySelect,
                                       CoordSelect,
                                       InputDataTable,
                                       InputLineTable,
                                       InputTriStateTable,
                                       InputDictTable,
                                       InputPointTable,
                                       InputPointDictTable,
                                       InputHistogram,
                                       InputTimeSeries)


def test_FloatSelect(qtbot):
        
    window = FloatSelect(units="Test")
    window.show()
    qtbot.addWidget(window)
    
    assert str(window.unitsLabel.text()) == "(Test)"


def test_FloatSelect_get_result(qtbot):
    
    window = FloatSelect()
    window._set_value(1.)
    window.show()
    qtbot.addWidget(window)
    
    test = window._get_result()
    
    assert test == 1.


def test_StringSelect(qtbot):

    window = StringSelect(units="Test")
    window.show()
    qtbot.addWidget(window)
    
    assert str(window.unitsLabel.text()) == "(Test)"


def test_StringSelect_get_result(qtbot):
    
    window = StringSelect()
    window._set_value("Bob")
    window.show()
    qtbot.addWidget(window)
    
    test = window._get_result()
    
    assert test == "Bob"


def test_DirectorySelect(qtbot):

    window = DirectorySelect()
    window.show()
    qtbot.addWidget(window)
    
    assert True


def test_DirectorySelect_get_result(qtbot):
    
    window = DirectorySelect()
    window._set_value("Bob")
    window.show()
    qtbot.addWidget(window)
    
    test = window._get_result()
    
    assert test == "Bob"


def test_CoordSelect(qtbot):
        
    window = CoordSelect(units="Test")
    window.show()
    qtbot.addWidget(window)
    
    assert str(window.unitsLabel.text()) == "(Test)"


def test_CoordSelect_get_result_2D(qtbot):
    
    window = CoordSelect()
    window._set_value([1., 2.])
    
    assert not window.doubleSpinBox_3.isEnabled()
    assert not window.checkBox.isChecked()
    
    window.show()
    qtbot.addWidget(window)
    test = window._get_result()
    
    assert test == [1., 2.]


def test_CoordSelect_get_result_3D(qtbot):
    
    window = CoordSelect()
    window._set_value([1., 2., 3.])
    
    assert window.doubleSpinBox_3.isEnabled()
    assert window.checkBox.isChecked()
    
    window.show()
    qtbot.addWidget(window)
    test = window._get_result()
    
    assert test == [1., 2., 3.]


def test_CoordSelect_get_result_None(qtbot):
    
    window = CoordSelect()
    window._set_value(None)
    
    assert not window.doubleSpinBox_3.isEnabled()
    assert not window.checkBox.isChecked()
    
    window.show()
    qtbot.addWidget(window)
    test = window._get_result()
    
    assert test == [0.0, 0.0]


def test_InputDataTable_edit_cols(qtbot):
        
    window = InputDataTable(None,
                            ["Test", "Test [Brackets]"],
                            units=["test", "test"],
                            edit_cols=True)
    window.show()
    qtbot.addWidget(window)
    
    assert True


def test_InputDataTable_edit_cols_get_result(qtbot):
    
    raw_dict = {"val1": [0, 1, 2, 3],
                "val2": [0, 1, 4, 9]}
                
    vals_df = pd.DataFrame(raw_dict)
    
    window = InputDataTable(None,
                            ["Test", "Test [Brackets]"],
                            units=["test", "test"],
                            edit_cols=True)
    window._set_value(vals_df)
    window.show()
    qtbot.addWidget(window)
    
    test = window._get_result()
    
    assert (test.columns.values == ["Test", "Test"]).all()


def test_InputLineTable(qtbot):
    
    window = InputLineTable(units=["test", "test"])
    window.show()
    qtbot.addWidget(window)
    
    assert True
    

def test_InputLineTable_get_result(qtbot):
    
    raw_dict = {"val1": [0, 1, 2, 3],
                "val2": [0, 1, 4, 9]}
                
    vals_df = pd.DataFrame(raw_dict)
    
    window = InputLineTable(units=["test", "test"])
    window._set_value(vals_df)
    window.show()
    qtbot.addWidget(window)
    
    test = window._get_result()
    
    assert np.isclose(test, vals_df.values).all()


def test_InputLineTable_disable(qtbot):
    
    window = InputLineTable(units=["test", "test"])
    window.show()
    qtbot.addWidget(window)
    window._disable()
    
    assert not window.buttonBox.isEnabled()
    assert not window.datatable.buttonFrame.isEnabled()


def test_InputTriStateTable(qtbot):
        
    window = InputTriStateTable(None, ["test1", "test2"])
    window.show()
    qtbot.addWidget(window)
    
    assert True
    

def test_InputTriStateTable_get_result(qtbot):
    
    raw_dict = {"test1": ["true", "false", "unknown", "None", ""],
                "test2": ["true", "false", "unknown", "None", ""]}
                
    vals_df = pd.DataFrame(raw_dict)
    
    window = InputTriStateTable(None, ["test1", "test2"])
    window._set_value(vals_df)
    window.show()
    qtbot.addWidget(window)
    
    test = window._get_result()
    
    assert set(test["test1"]) == set(["true", "false", "unknown"])
    

def test_InputDictTable(qtbot):
        
    window = InputDictTable(units=["test1", "test2"],
                            fixed_index_names=["a", "b", "c"])
    window.show()
    qtbot.addWidget(window)
    
    assert True
    

def test_InputDictTable_get_result(qtbot):
    
    raw_dict = {"a": 1,
                "b": 2,
                "c": 3}
                
    df_dict = {"Key": raw_dict.keys(),
               "Value": raw_dict.values()}
    value = pd.DataFrame(df_dict)
    
    window = InputDictTable(units=["test1", "test2"],
                            fixed_index_names=["a", "b", "c"])
    window._set_value(value)
    window.show()
    qtbot.addWidget(window)
    
    test = window._get_result()
    
    assert test == raw_dict


def test_InputDictTable_get_result_none(qtbot):
    
    raw_dict = {"a": None,
                "b": None,
                "c": None}
                
    df_dict = {"Key": raw_dict.keys(),
               "Value": raw_dict.values()}
    value = pd.DataFrame(df_dict)
    
    window = InputDictTable(units=["test1", "test2"],
                            fixed_index_names=["a", "b", "c"])
    window._set_value(value)
    window.show()
    qtbot.addWidget(window)
    
    test = window._get_result()
    
    assert test is None


def test_InputPointTable(qtbot):
        
    window = InputPointTable()
    window.show()
    qtbot.addWidget(window)
    
    assert True
    

def test_InputPointTable_get_result(qtbot):
    
    raw_dict = {"x": [1, 2, 3],
                "y": [1, 2, 3],
                "z": [1, 2, 3]}
                        
    point_df = pd.DataFrame(raw_dict)
    
    window = InputPointTable()
    window._set_value(point_df)
    window.show()
    qtbot.addWidget(window)
    
    test = window._get_result()
    
    assert np.array_equal(test, point_df.values)


def test_InputPointTable_get_result_znone(qtbot):
    
    raw_dict = {"x": [1, 2, 3],
                "y": [1, 2, 3],
                "z": [None, None, None]}
                        
    point_df = pd.DataFrame(raw_dict)
    
    window = InputPointTable()
    window._set_value(point_df)
    window.show()
    qtbot.addWidget(window)
    
    test = window._get_result()
    
    assert np.array_equal(test, point_df[["x", "y"]].values)
    

def test_InputPointDictTable(qtbot):
        
    window = InputPointDictTable(fixed_index_names=["a", "b", "c"])
    window.show()
    qtbot.addWidget(window)
    
    assert True


def test_InputPointDictTable_get_result(qtbot):
    
    raw_dict = {"Key": ["a", "b", "c"],
                "x": [1, 2, 3],
                "y": [1, 2, 3],
                "z": [1, 2, 3]}
                        
    point_df = pd.DataFrame(raw_dict)
    
    window = InputPointDictTable(fixed_index_names=["a", "b", "c"])
    window._set_value(point_df)
    window.show()
    qtbot.addWidget(window)
    
    test = window._get_result()
    point_df = point_df.set_index("Key")
    
    assert set(test.keys()) == set(raw_dict["Key"])
    
    for test_key, test_row in test.items():
        point_row = point_df.loc[test_key]
        assert np.isclose(test_row, point_row.values).all()


def test_InputPointDictTable_get_result_znone(qtbot):
    
    raw_dict = {"Key": ["a", "b", "c"],
                "x": [1, 2, 3],
                "y": [1, 2, 3],
                "z": [None, None, None]}
                        
    point_df = pd.DataFrame(raw_dict)
    
    window = InputPointDictTable(fixed_index_names=["a", "b", "c"])
    window._set_value(point_df)
    window.show()
    qtbot.addWidget(window)
    
    test = window._get_result()
    point_df = point_df.set_index("Key")
    point_df = point_df.drop("z", axis=1)
    
    assert set(test.keys()) == set(raw_dict["Key"])
    
    for test_key, test_row in test.items():
        point_row = point_df.loc[test_key]
        assert np.isclose(test_row, point_row.values).all()
        

def test_InputPointDictTable_get_result_none(qtbot):
    
    raw_dict = {"Key": ["a", "b", "c"],
                "x": [None, None, None],
                "y": [None, None, None],
                "z": [None, None, None]}
                        
    point_df = pd.DataFrame(raw_dict)
    
    window = InputPointDictTable(fixed_index_names=["a", "b", "c"])
    window._set_value(point_df)
    window.show()
    qtbot.addWidget(window)
    
    test = window._get_result()
    
    assert test is None


def test_InputHistogram(qtbot):
        
    window = InputHistogram()
    window.show()
    qtbot.addWidget(window)
    
    assert True
    

def test_InputHistogram_get_result(qtbot):
    
    bins = [0, 1, 2, 3, 4, 5]
    values = [1, 1, 2, 1, 1]

    raw_dict = {"Bin Separators": bins,
                "Values": values + [None],
                }
                
    hist_df = pd.DataFrame(raw_dict)
    
    window = InputHistogram()
    window._set_value(hist_df)
    window.show()
    qtbot.addWidget(window)
    
    test = window._get_result()
    
    assert np.isclose(test[0], bins).all()
    assert np.isclose(test[1], values).all()


def test_InputTimeSeries(qtbot):
        
    window = InputTimeSeries(labels=["Data"], units=["test"])
    window.show()
    qtbot.addWidget(window)
    
    assert True
    

def test_InputTimeSeries_get_result(qtbot):
    
    rng = pd.date_range('1/1/2011', periods=72, freq='H')
    ts = pd.Series(np.random.randn(len(rng)), index=rng)

    window = InputTimeSeries(labels=["Data"], units=["test"])
    window._set_value(ts)
    window.show()
    qtbot.addWidget(window)
    
    test = window._get_result()
    
    assert test.equals(ts)
