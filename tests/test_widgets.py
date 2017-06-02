# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:16:37 2017

@author: mtopper
"""

from dtocean_app.widgets.input import FloatSelect


def test_FloatSelect(qtbot):
        
    window = FloatSelect(units="Test")
    window.show()
    qtbot.addWidget(window)
    
    assert str(window.unitsLabel.text()) == "(Test)"
