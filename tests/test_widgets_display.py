# -*- coding: utf-8 -*-
"""
Created on Thu Oct 04 13:55:19 2018

@author: Mathew Topper
"""

import matplotlib.pyplot as plt

from dtocean_app.widgets.display import get_current_figure_size


def test_get_current_figure_size_no_figure():
        
    test = get_current_figure_size()
    
    assert test is None


def test_get_current_figure_size():
        
    plt.figure()
    test = get_current_figure_size()
    plt.close('all')
    
    assert (test == [8., 6.]).all()
