# -*- coding: utf-8 -*-

#    Copyright (C) 2022 Mathew Topper
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

# pylint: disable=redefined-outer-name

import pytest
from PyQt4 import QtCore, QtGui

from dtocean_app.widgets.dialogs import TestDataPicker, About


@pytest.fixture
def picker_widget(qtbot):
    
    widget = TestDataPicker()
    widget.show()
    qtbot.addWidget(widget)
    
    return widget


def test_TestDataPicker_init(picker_widget):
    assert picker_widget.isVisible()


def test_TestDataPicker_write_path(mocker, qtbot, picker_widget):
    
    expected = "mock.pkl"
    mocker.patch.object(QtGui.QFileDialog,
                        'getOpenFileName',
                        return_value=expected)
    
    qtbot.mouseClick(picker_widget.browseButton, QtCore.Qt.LeftButton)
    
    def has_path():
        assert str(picker_widget.pathLineEdit.text())
    
    qtbot.waitUntil(has_path)
    
    assert str(picker_widget.pathLineEdit.text()) == expected


def test_About_init(qtbot):
    
    widget = About()
    widget.show()
    qtbot.addWidget(widget)
    
    assert widget.isVisible()


def test_About_names_none(qtbot, mocker):
    
    from dtocean_app.widgets.dialogs import yaml
    
    mocker.patch.object(yaml, 'load', return_value=None)
    
    widget = About()
    widget.show()
    qtbot.addWidget(widget)
    
    assert widget.peopleIntroLabel is None
    assert widget.peopleLabel is None
    assert widget.line is None
