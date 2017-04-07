# -*- coding: utf-8 -*-

#    Copyright (C) 2016 Mathew Topper, Rui Duarte
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

"""
Created on Mon Jun 13 12:11:53 2016

@author: 108630
"""

import pandas as pd

from PyQt4 import QtGui, QtCore

from .widgets.dialogs import ListTableEditor


class DBSelector(ListTableEditor):
    
    database_selected = QtCore.pyqtSignal(object)
    
    def __init__(self, parent, data_menu):
        
        super(DBSelector, self).__init__(parent)
        self._data_menu = data_menu
        self._selected = None
        self._unsaved = False
        
        self._init_ui()
                
        return
        
    def _init_ui(self):
        
        self.setWindowTitle("Select database...")
        self.topStaticLabel.setText("Current database:")
        self.listLabel.setText("Available:")
        self.tableLabel.setText("Credentials:")
        self._update_current("None")
        
        self.listWidget.itemClicked.connect(self._update_table)
        self.tableWidget.cellChanged.connect(self._unsaved_data)

        self.buttonBox.button(
            QtGui.QDialogButtonBox.Apply).clicked.connect(self._set_database)
        self.buttonBox.button(
            QtGui.QDialogButtonBox.Reset).clicked.connect(self._reset_database)
        self.saveButton.clicked.connect(self._update_database)
        
        # Disable non-implemented functionality.
        self.addButton.setEnabled(False)
        self.deleteButton.setEnabled(False)
        self.saveButton.setEnabled(False)

        return
        
    def _update_list(self):
        
        db_names = self._data_menu.get_available_databases()
        super(DBSelector, self)._update_list(db_names)
        
        return
        
    @QtCore.pyqtSlot(str)
    def _update_current(self, current_db):
        
        self.topDynamicLabel.setText(current_db)
        
        return
    
    @QtCore.pyqtSlot(object)
    def _update_table(self, item):
        
        selected = str(item.text())
        db_dict = self._data_menu.get_database_dict(selected)
        
        key_order =  ['host', 'dbname', 'user', 'pwd']
        value_order = []        
        
        for key in key_order:
            if key in db_dict:
                value = db_dict[key]
            else:
                value = ""
            value_order.append(value)
    
        frame_dict = {"Key": key_order,
                      "Value": value_order}
        df = pd.DataFrame(frame_dict)
                
        super(DBSelector, self)._update_table(df, ["Key"])
        
        # Record the selected database        
        self._selected = selected
        
        # Set data as saved
        self.tableLabel.setText("Credentials:")
        self.saveButton.setEnabled(False)
        self._unsaved = False
        
        return
        
    @QtCore.pyqtSlot(int, int)
    def _unsaved_data(self, *args):
        
        self.tableLabel.setText("Credentials (unsaved):")
        self.saveButton.setEnabled(True)
        self._unsaved = True
        
        return
        
    @QtCore.pyqtSlot()
    def _set_database(self):
        
        self.database_selected.emit(self._selected)
        
        return
        
    @QtCore.pyqtSlot()
    def _reset_database(self):
        
        self.database_selected.emit(None)
        
        return
        
    @QtCore.pyqtSlot(int)
    def _update_database(self, *args):
        
        if not self._unsaved: return
        
        tabledf = self._read_table()
        
        keys = tabledf["Key"]
        values = tabledf["Value"]
        db_dict = {k: v for k, v in zip(keys, values)}
        
        self._data_menu.update_database(self._selected,
                                        db_dict,
                                        True)
                                        
        # Set data as saved
        self.tableLabel.setText("Credentials:")
        self.saveButton.setEnabled(False)
        self._unsaved = False
                                        
        return

    def show(self):
        
        self._update_list()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        super(DBSelector, self).show()
        
        return

