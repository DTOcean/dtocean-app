# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:16:37 2017

@author: mtopper
"""

import warnings

from dtocean_app import warn_with_traceback, start_logging


def test_warn_with_traceback():
    
    warnings.showwarning = warn_with_traceback
    warnings.warn("Test warning")
    
    assert True


def test_start_logging():
    
    start_logging()
    
    assert True
    

def test_start_logging_twice():
    
    start_logging()
    start_logging()
    
    assert True
