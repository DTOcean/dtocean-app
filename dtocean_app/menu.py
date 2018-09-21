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

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class DBSelector(ListTableEditor):
    
    database_selected = QtCore.pyqtSignal(str, dict)
    database_deselected = QtCore.pyqtSignal()
    
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
        
        # Add warning about passwords
        label_str = ("NOTE: Passwords are saved as PLAIN TEXT. Do not save "
                     "your password if you have any security concerns, "
                     "instead fill the 'pwd' field in this dialogue, before "
                     "pressing apply.")
        self.extraLabel.setText(label_str)
        
        # Tool tips for standard buttons
        tip_msg = 'Add stored credentials'
        self.addButton.setToolTip(tip_msg)
        
        tip_msg = 'Delete stored credentials'
        self.deleteButton.setToolTip(tip_msg)
        
        tip_msg = 'Store updated credentials'
        self.saveButton.setToolTip(tip_msg)
        
        # Add new buttons
        self.loadButton = self._make_button()
        self.loadButton.setObjectName(_fromUtf8("loadButton"))
        self.loadButton.setText("Load...")
        self.loadButton.setDisabled(True)
        self.verticalLayout.addWidget(self.loadButton)
        
        tip_msg = 'Load database from structured files'
        self.loadButton.setToolTip(tip_msg)
        
        self.dumpButton = self._make_button()
        self.dumpButton.setObjectName(_fromUtf8("dumpButton"))
        self.dumpButton.setText("Dump...")
        self.dumpButton.setDisabled(True)
        self.verticalLayout.addWidget(self.dumpButton)
        
        tip_msg = 'Dump database to structured files'
        self.dumpButton.setToolTip(tip_msg)
        
        self.listWidget.itemClicked.connect(self._update_table)
        self.listWidget.itemDelegate().closeEditor.connect(
                                                        self._rename_database)
        
        self.tableWidget.cellChanged.connect(self._unsaved_data)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)

        self.buttonBox.button(
            QtGui.QDialogButtonBox.Apply).clicked.connect(self._set_database)
        self.buttonBox.button(
            QtGui.QDialogButtonBox.Reset).clicked.connect(self._reset_database)
        self.addButton.clicked.connect(self._add_database)
        self.saveButton.clicked.connect(self._update_database)
        self.deleteButton.clicked.connect(self._delete_database)
        
        self.addButton.setEnabled(True)
        self.deleteButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).setDefault(True)
        
        # Populate the database list
        self._update_list()

        return
    
    def _make_button(self):
        
        button = QtGui.QPushButton(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                       QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(sizePolicy)
        
        return button
        
    def _update_list(self):
        
        db_names = self._data_menu.get_available_databases()
        super(DBSelector, self)._update_list(db_names)
        
        # Make them editable
        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            
        if self.listWidget.count() > 0:
            self.deleteButton.setEnabled(True)
        
        return
        
    @QtCore.pyqtSlot(str)
    def _update_current(self, current_db):
        
        self.topDynamicLabel.setText(current_db)
        
        # Set button default
        if current_db is None:
            self.buttonBox.button(
                    QtGui.QDialogButtonBox.Apply).setDefault(True)
        else:
            self.buttonBox.button(
                    QtGui.QDialogButtonBox.Close).setDefault(True)
        
        return
    
    @QtCore.pyqtSlot(object)
    def _update_table(self, item, template=False):
        
        selected = str(item.text())
        
        key_order =  ['host', 'dbname', 'user', 'pwd']
        value_order = []        
        
        if template:
            db_dict = {}
        else:
            db_dict = self._data_menu.get_database_dict(selected)

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
        if not template:
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
        
        if self._selected is None: return
        
        tabledf = self._read_table()
        valid_keys =  ['host', 'dbname', 'user', 'pwd']
        
        keys = tabledf["Key"]
        values = tabledf["Value"]
        db_dict = {k: v for k, v in zip(keys, values) if k in valid_keys}
        
        name = self._selected
        if self._unsaved: name += " (modified)"
        
        self.database_selected.emit(name, db_dict)
        
        
        
        return
        
    @QtCore.pyqtSlot()
    def _reset_database(self):
        
        self.database_deselected.emit()
        
        # Set apply button as default
        
        
        return
    
    @QtCore.pyqtSlot(object, object)
    def _rename_database(self, editor, hint):
       
        new_name = str(editor.text())
                
        if new_name == self._selected: return
                
        # If the name is already used then reject it
        if new_name in self._data_menu.get_available_databases():
            
            item = self.listWidget.currentItem()
            item.setText(self._selected)
            
            return
        
        self._data_menu.delete_database(self._selected)
        
        tabledf = self._read_table()
        
        keys = tabledf["Key"]
        values = tabledf["Value"]
        db_dict = {k: v for k, v in zip(keys, values)}
        
        self._data_menu.update_database(new_name,
                                        db_dict,
                                        True)
        
        self._selected = new_name
        
        return
    
    @QtCore.pyqtSlot()
    def _add_database(self):
        
        # Ensure name is unique
        base_name = "unnamed"
        new_name = base_name
        add_number = 1
        
        while True:
                        
            if new_name in self._data_menu.get_available_databases():
                new_name = "{}-{}".format(base_name, add_number)
                add_number += 1
            else:
                break
        
        new_item = self._add_item(new_name)
        new_item.setFlags(new_item.flags() | QtCore.Qt.ItemIsEditable)
        self._update_table(new_item, template=True)
        self._unsaved = True
        self._update_database()
        
        self.deleteButton.setEnabled(True)
        
        return

    @QtCore.pyqtSlot()
    def _update_database(self):
        
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
    
    @QtCore.pyqtSlot()
    def _delete_database(self):
        
        # Check again
        qm = QtGui.QMessageBox
        ret = qm.question(self,
                          "Delete '{}'?".format(self._selected),
                          "Are you sure you wish to remove these credentials?",
                          qm.Yes | qm.No)

        if ret == qm.No: return
        
        self._data_menu.delete_database(self._selected)
        self._delete_selected()
        
        if self.listWidget.count() == 0:
            
            self.deleteButton.setDisabled(True)
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
        
        else:
            
            item = self.listWidget.item(self.listWidget.currentRow())
            self._update_table(item)
        
        return

