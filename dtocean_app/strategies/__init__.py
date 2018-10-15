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

import abc

from PyQt4.QtCore import pyqtWrapperType


class GUIStrategy(object):
    
    __metaclass__ = abc.ABCMeta

    '''The base abstract class for discovery of GUI supported strategy 
    classes'''
    
    def __init__(self):
        
        self.strategy_run = None
        
        return
    
    @abc.abstractproperty
    def allow_rerun(self):
        
        """Can the strategy be rerun after first execution"""
        
        return NotImplementedError

    @abc.abstractmethod
    def get_widget(self):

        '''A method for getting the configuration widget of the strategy.

        Returns:
          StrategyWidget
        '''

        return
        
    @abc.abstractmethod
    def get_weight(self):

        '''A method for getting the order of priority of the strategy.

        Returns:
          int
        '''

        return


class StrategyWidget(object):
    
    __metaclass__ = abc.ABCMeta
    
    '''The base abstract class for widgets used to configure the strategy 
    classes'''
    
    @abc.abstractmethod
    def get_configuration(self):
        
        '''A method for getting the dictionary to configure the strategy.

        Returns:
          dict
        '''
        
        return {}

    @abc.abstractmethod
    def set_configuration(self, config_dict=None):
        
        '''A method for displaying the configuration in the gui.

        Arguments:
          config_dict (dict, optional)
        '''
        
        return

    @staticmethod
    def string2types(raw_string_input):
        
        """Convert a raw strings into a list of typed objects"""
        
        # Split the string
        words = raw_string_input.split(",")
        words = [x.strip() for x in words]
                 
        params = []
                 
        for word in words:
            
            if word in ["True", "False"]:
                param = eval(word)
            elif word.isdigit():
                param = int(word)
            else:
                try:
                    param = float(word)
                except ValueError:
                    param = word
            
            params.append(param)
            
        return params
        
class PyQtABCMeta(pyqtWrapperType, abc.ABCMeta):
    
    pass
