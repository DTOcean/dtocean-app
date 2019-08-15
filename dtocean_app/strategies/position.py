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

import pandas as pd
from PyQt4 import QtCore, QtGui

from aneris.utilities.misc import OrderedSet
from dtocean_core.pipeline import Tree
from dtocean_core.strategies.position import AdvancedPosition

from . import GUIStrategy, StrategyWidget, PyQtABCMeta
from ..utils.display import is_high_dpi
from ..widgets.extendedcombobox import ExtendedComboBox

if is_high_dpi():
    
    from ..designer.high.advancedposition import Ui_AdvancedPositionWidget
    
else:
    
    from ..designer.low.advancedposition import Ui_AdvancedPositionWidget


class GUIAdvancedPosition(GUIStrategy, AdvancedPosition):
    
    """
    """
    
    def __init__(self):
        
        AdvancedPosition.__init__(self)
        GUIStrategy.__init__(self)
        
        return
    
    @property
    def allow_rerun(self):
        
        return False
    
    def get_weight(self):
        
        '''A method for getting the order of priority of the strategy.
        
        Returns:
          int
        '''
        
        return 4
    
    def get_widget(self, parent, shell):
        
        widget = AdvancedPositionWidget(parent)
        
        return widget


class AdvancedPositionWidget(QtGui.QWidget,
                             Ui_AdvancedPositionWidget,
                             StrategyWidget):
    
    __metaclass__ = PyQtABCMeta
    
    config_set = QtCore.pyqtSignal()
    config_null = QtCore.pyqtSignal()
    
    def __init__(self, parent):
        
        QtGui.QWidget.__init__(self, parent)
        Ui_AdvancedPositionWidget.__init__(self)
        StrategyWidget.__init__(self)
        
        self._init_ui()
        
        return
        
    def _init_ui(self):
        
        self.setupUi(self)
        
        return
    
    def get_configuration(self):
        
        '''A method for getting the dictionary to configure the strategy.
        
        Returns:
          dict
        '''
        
        return {}
    
    def set_configuration(self, config_dict=None):
        
        '''A method for displaying the configuration in the gui.
        
        Arguments:
          config_dict (dict, optional)
        '''
        
        return
