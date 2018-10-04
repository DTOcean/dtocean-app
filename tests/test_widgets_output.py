# -*- coding: utf-8 -*-
"""
Created on Thu Oct 04 13:55:19 2018

@author: Mathew Topper
"""

import pytest
import pandas as pd

from dtocean_app.widgets.output import OutputDataTable


def test_OutputDataTable(qtbot):
        
    window = OutputDataTable(None,
                             ["Test1", "Test2"],
                             units=["test", "test"])
    window.show()
    qtbot.addWidget(window)
    
    assert True


def test_OutputDataTable_set_value(qtbot):
    
    raw_dict = {"Test1": [0, 1, 2, 3],
                "Test2": [0, 1, 4, 9]}
                
    vals_df = pd.DataFrame(raw_dict)
    
    window = OutputDataTable(None,
                             ["Test1", "Test2"],
                             units=["test", "test"])
    window._set_value(vals_df)
    window.show()
    qtbot.addWidget(window)
    
    assert True



def test_OutputDataTable_set_value_None(qtbot):
    
    window = OutputDataTable(None,
                             ["Test1", "Test2"],
                             units=["test", "test"])
    window._set_value(None)
    window.show()
    qtbot.addWidget(window)
    
    assert True


def test_OutputDataTable_set_value_missing_cols(qtbot):
    
    raw_dict = {"Test1": [0, 1, 2, 3]}
                
    vals_df = pd.DataFrame(raw_dict)
    
    window = OutputDataTable(None,
                             ["Test1", "Test2"],
                             units=["test", "test"])
    window._set_value(vals_df)
    window.show()
    qtbot.addWidget(window)
    
    assert True


def test_OutputDataTable_set_value_extra_cols(qtbot):
    
    raw_dict = {"Test1": [0, 1, 2, 3],
                "Test2": [0, 1, 4, 9],
                "Test3": [0, 1, 8, 27]}
                
    vals_df = pd.DataFrame(raw_dict)
    
    window = OutputDataTable(None,
                             ["Test1", "Test2"],
                             units=["test", "test"])
    
    with pytest.raises(ValueError):
        window._set_value(vals_df)
