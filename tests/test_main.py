# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:16:37 2017

@author: mtopper
"""

import pytest
from PyQt4.QtGui import QMessageBox

from dtocean_app.main import DTOceanWindow, Shell


@pytest.fixture(scope="module")
def shell():
    '''Share a Shell object'''
    
    new_shell = Shell()
    
    return new_shell


def test_open_dtocean_window(qtbot, mock, shell):
    
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    mock.patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes)
    
    assert window.windowTitle() == "DTOcean"
