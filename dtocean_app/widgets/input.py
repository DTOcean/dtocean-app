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
Created on Thu Apr 23 12:51:14 2015

@author: Mathew Topper
"""

import pandas as pd
import numpy as np

from PyQt4 import QtCore, QtGui
from dtocean_qt.models.DataFrameModel import DataFrameModel
from shapely.geometry import Polygon, Point

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

from .datatable import DataTableWidget
from ..designer.listselect import Ui_ListSelect
from ..designer.floatselect import Ui_FloatSelect
from ..designer.intselect import Ui_IntSelect
from ..designer.pointselect import Ui_PointSelect
from ..designer.stringselect import Ui_StringSelect
from ..designer.boolselect import Ui_BoolSelect
from ..designer.pathselect import Ui_PathSelect
from ..designer.dateselect import Ui_DateSelect

# DOCK WINDOW INPUT WIDGETS

class CancelWidget(QtGui.QWidget):
    
    dummy_read = QtCore.pyqtSignal()

    def __init__(self, parent=None):

        super(CancelWidget, self).__init__(parent)
        
        self._init_ui()

        return
        
    def _init_ui(self):
        
        self.verticalLayout = QtGui.QVBoxLayout(self)
        
        spacerItem = QtGui.QSpacerItem(20,
                                       100,
                                       QtGui.QSizePolicy.Minimum,
                                       QtGui.QSizePolicy.Expanding)

        self.verticalLayout.addItem(spacerItem)
        
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setCenterButtons(False)
        
        self.verticalLayout.addWidget(self.buttonBox)
        
        return
        
    def _set_value(self, value):
        
        return

    def _get_result(self):

        return
        
    def _get_read_event(self):

        return self.dummy_read
        
    def _get_nullify_event(self):

        return self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked


class ListSelect(QtGui.QWidget, Ui_ListSelect):

    def __init__(self, parent, data, question=None):

        QtGui.QWidget.__init__(self, parent)
        Ui_ListSelect.__init__(self)
        
        self.setupUi(self)
        self._init_ui(data, question=question)

        return

    def _init_ui(self, data, value=None, question=None):

        for item in data:
            self.comboBox.addItem(item)

        self.comboBox.setCurrentIndex(-1)
        
        self._set_value(value)
        
        if question is not None:
            self.questionLabel.setText(question)

        return
    
    def _set_value(self, value):
        
        valueStr = str(value)
        self.valueLabel.setText(valueStr)
        
        return

    def _get_result(self):

        current_index = self.comboBox.currentIndex()

        if current_index < 0:
            result = None
        else:
            result = self.comboBox.currentText()

        return result
        
    def _get_read_event(self):

        return self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked
        
    def _get_nullify_event(self):

        return self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked


class FloatSelect(QtGui.QWidget, Ui_FloatSelect):
    
    read_value = QtCore.pyqtSignal()

    def __init__(self, parent, units=None):

        QtGui.QWidget.__init__(self, parent)
        Ui_FloatSelect.__init__(self)
        
        self.setupUi(self)
        self._init_ui(units)

        return

    def _init_ui(self, units):

        if units is None:
            unitsStr = ""
        else:
            unitsStr = "({})".format(units)
        
        self.unitsLabel.setText(unitsStr)
        
        self.doubleSpinBox.valueChanged.connect(self._emit_read)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(
                                          self._emit_read)

        return
        
    def _set_value(self, value):
        
        valueStr = str(value)
        self.valueLabel.setText(valueStr)
        
        if value is not None:
            self.doubleSpinBox.setValue(value)
        
        return

    def _get_result(self):

        result = self.doubleSpinBox.value()
        
        return result

    def _get_read_event(self):

        return self.read_value
        
    def _get_nullify_event(self):

        return self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked
        
    @QtCore.pyqtSlot(object)     
    def _emit_read(self, *args):
        
        self.read_value.emit()
        
        return


class IntSelect(QtGui.QWidget, Ui_IntSelect):
    
    read_value = QtCore.pyqtSignal()

    def __init__(self, parent, units=None):

        QtGui.QWidget.__init__(self, parent)
        Ui_FloatSelect.__init__(self)
        
        self.setupUi(self)
        self._init_ui(units)

        return

    def _init_ui(self, units):

        if units is None:
            unitsStr = ""
        else:
            unitsStr = "({})".format(units)
        
        self.unitsLabel.setText(unitsStr)
        
        self.spinBox.valueChanged.connect(self._emit_read)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(
                                          self._emit_read)

        return
        
    def _set_value(self, value):
        
        valueStr = str(value)
        self.valueLabel.setText(valueStr)
        
        if value is not None:
            self.spinBox.setValue(value)
        
        return

    def _get_result(self):

        result = self.spinBox.value()
        
        return result
       
    def _get_read_event(self):

        return self.read_value
        
    def _get_nullify_event(self):

        return self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked
        
    @QtCore.pyqtSlot(object)     
    def _emit_read(self, *args):
        
        self.read_value.emit()
        
        return
        
        
class StringSelect(QtGui.QWidget, Ui_StringSelect):
    
    read_value = QtCore.pyqtSignal()

    def __init__(self, parent, units=None):

        QtGui.QWidget.__init__(self, parent)
        Ui_StringSelect.__init__(self)
        
        self.setupUi(self)
        self._init_ui(units)

        return

    def _init_ui(self, units):

        if units is None:
            unitsStr = ""
        else:
            unitsStr = "({})".format(units)
        
        self.unitsLabel.setText(unitsStr)
        
        self.lineEdit.textChanged.connect(self._emit_read)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(
                                          self._emit_read)

        return
        
    def _set_value(self, value):
        
        valueStr = str(value)
        self.valueLabel.setText(valueStr)
        
        if value is not None:
            self.lineEdit.setText(value)
        
        return

    def _get_result(self):

        result = str(self.lineEdit.text())
        
        return result
       
    def _get_read_event(self):

        return self.read_value
        
    def _get_nullify_event(self):

        return self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked
        
    @QtCore.pyqtSlot(object)     
    def _emit_read(self, *args):
        
        self.read_value.emit()
        
        return

        
class DirectorySelect(QtGui.QWidget, Ui_PathSelect):
    
    read_value = QtCore.pyqtSignal()

    def __init__(self, parent):

        QtGui.QWidget.__init__(self, parent)
        Ui_StringSelect.__init__(self)
        
        self.setupUi(self)
        self._init_ui()

        return

    def _init_ui(self):

        self.toolButton.clicked.connect(self._set_path)
        self.lineEdit.textChanged.connect(self._emit_read)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(
                                          self._emit_read)

        return
        
    def _set_value(self, value):
        
        valueStr = str(value)
        self.valueLabel.setText(valueStr)
        
        if value is not None:
            self.lineEdit.setText(value)
        
        return

    def _get_result(self):

        result = str(self.lineEdit.text())
        
        return result
       
    def _get_read_event(self):

        return self.read_value
        
    def _get_nullify_event(self):

        return self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked
        
    @QtCore.pyqtSlot()    
    def _set_path(self):
        
        msg = "Select directory"
        file_path = QtGui.QFileDialog.getExistingDirectory(None,
                                                           msg)
        
        self.lineEdit.setText(file_path)
        
        return
        
    @QtCore.pyqtSlot(object)     
    def _emit_read(self, *args):
        
        self.read_value.emit()
        
        return
        

class BoolSelect(QtGui.QWidget, Ui_BoolSelect):
    
    read_value = QtCore.pyqtSignal()

    def __init__(self, parent):

        QtGui.QWidget.__init__(self, parent)
        Ui_StringSelect.__init__(self)
        
        self.setupUi(self)
        self._init_ui()

        return

    def _init_ui(self):
                
        self.checkBox.stateChanged.connect(self._emit_read)

        return
        
    def _set_value(self, value):
        
        valueStr = str(value)
        self.valueLabel.setText(valueStr)
        
        if value is not None:
            
            if value:
                state = QtCore.Qt.Checked
            else:
                state = QtCore.Qt.Unchecked

            self.checkBox.setCheckState(state)
        
        return

    def _get_result(self):

        result = self.checkBox.isChecked()
        
        return result
       
    def _get_read_event(self):

        return self.read_value
        
    def _get_nullify_event(self):

        return self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked
        
    @QtCore.pyqtSlot(object)     
    def _emit_read(self, *args):
        
        self.read_value.emit()
        
        return


class DateSelect(QtGui.QWidget, Ui_DateSelect):
    
    read_value = QtCore.pyqtSignal()

    def __init__(self, parent):

        QtGui.QWidget.__init__(self, parent)
        Ui_DateSelect.__init__(self)
        
        self.setupUi(self)
        self._init_ui()

        return

    def _init_ui(self):
        
        self.dateTimeEdit.dateTimeChanged.connect(self._emit_read)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(
                                          self._emit_read)

        return
        
    def _set_value(self, value):
        
        valueStr = str(value)
        self.valueLabel.setText(valueStr)
        
        if value is not None:
            self.dateTimeEdit.setDateTime(value)
        
        return

    def _get_result(self):

        qtdt = self.dateTimeEdit.dateTime()
        result = qtdt.toPyDateTime()
        
        return result

    def _get_read_event(self):

        return self.read_value
        
    def _get_nullify_event(self):

        return self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked
        
    @QtCore.pyqtSlot(object)     
    def _emit_read(self, *args):
        
        self.read_value.emit()
        
        return
        
        
class CoordSelect(QtGui.QWidget, Ui_PointSelect):
    
    read_value = QtCore.pyqtSignal()

    def __init__(self, parent, units=None):

        QtGui.QWidget.__init__(self, parent)
        Ui_PointSelect.__init__(self)
        
        self.setupUi(self)
        self._init_ui(units)

        return

    def _init_ui(self, units):

        if units is None:
            unitsStr = ""
        else:
            unitsStr = "({})".format(units)
        
        self.unitsLabel.setText(unitsStr)
        
        self.checkBox.clicked.connect(self._check_z)
        
        self.doubleSpinBox_1.valueChanged.connect(self._emit_read)
        self.doubleSpinBox_2.valueChanged.connect(self._emit_read)
        self.doubleSpinBox_3.valueChanged.connect(self._emit_read)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(
                                          self._emit_read)

        return
        
    def _set_value(self, value):
        
        self.checkBox.setChecked

        if value is not None:
            
            self.doubleSpinBox_1.setValue(value[0])
            self.doubleSpinBox_2.setValue(value[1])
            
            if len(value) == 3:
  
                self.checkBox.setChecked(True)
                valueStr = str((value[0],value[1],value[2]))
                
            else:
                
                self.checkBox.setChecked(False)
                valueStr = str((value[0],value[1]))
                
        else:
            
            self.checkBox.setChecked(False)
            valueStr = "None"

        self.valueLabel.setText(valueStr)
        self._check_z()
        
        return

    def _get_result(self):
        
        coords = [self.doubleSpinBox_1.value(),
                  self.doubleSpinBox_2.value()]
        
        if self.checkBox.isChecked():
            coords.append(self.doubleSpinBox_3.value())
        
        return coords

    def _get_read_event(self):

        return self.read_value
        
    def _get_nullify_event(self):

        return self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked
        
    @QtCore.pyqtSlot(object)     
    def _emit_read(self, *args):
        
        self.read_value.emit()
        
        return
        
    @QtCore.pyqtSlot(object)     
    def _check_z(self, *args):
        
        if self.checkBox.isChecked():
            self.doubleSpinBox_3.setEnabled(True)
        else:
            self.doubleSpinBox_3.setDisabled(True)
                
        return


class PointSelect(CoordSelect):

    def _get_result(self):
        
        coords = super(PointSelect, self)._get_result()

        result = Point(*coords)
        
        return result
        
        
class InputDataTable(QtGui.QWidget):
    
    null_signal = QtCore.pyqtSignal()
    
    def __init__(self, parent,
                       columns,
                       units=None,
                       fixed_index_col=None,
                       fixed_index_names=None):

        QtGui.QWidget.__init__(self, parent)
        self._columms = columns
        self._units = units
        self._fixed_index_col = fixed_index_col
        self._fixed_index_names = fixed_index_names
        
        self._setup_ui()
        self._init_ui()
        
        return
    
    def _setup_ui(self):
        
        spacerItem = QtGui.QSpacerItem(20,
                                       20,
                                       QtGui.QSizePolicy.Fixed,
                                       QtGui.QSizePolicy.Fixed)
        
        self.setObjectName(_fromUtf8("dataTableObject"))
        
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        
        if (self._fixed_index_col is not None and
                self._fixed_index_names is not None):
            self.datatable = DataTableWidget(self, edit_cols=False,
                                                   edit_rows=False,
                                                   edit_cells=True)
        else:
            self.datatable = DataTableWidget(self, edit_cols=False)
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Expanding)
        self.datatable.setSizePolicy(sizePolicy)
        
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | 
                                          QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        
        self.verticalLayout.addWidget(self.datatable)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.buttonBox)

        QtCore.QMetaObject.connectSlotsByName(self)
        
        return
        
    def _init_ui(self):
        
        "Store the metadata for modifying the DataFrame which is displayed"
                
        self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(
                                                              self._emit_null)
        
        return

    def _set_value(self, value, dtypes=None):
                
        # setup a new empty model
        model = DataFrameModel()
        
        # Modify the appearance and function of the table if fixed rows are
        # required.
        if (self._fixed_index_col is not None and
            self._fixed_index_names is not None):
            
            model.freeze_first = True
            self.datatable.hideVerticalHeader(True)

        # set table view widget model
        self.datatable.setViewModel(model)
        
        # fill the model with data
        data = self._get_dataframe(value, dtypes)
        model.setDataFrame(data)
        
        return
        
    def _get_dataframe(self, value, dtypes=None):
        
        if self._units is None:
            units = [None] * len(self._columms)
        else:
            units = self._units
        
        # Build new columns
        new_cols = []        
        
        for col, unit in zip(self._columms, units):
            
            if unit is not None:
                new_col = "{} [{}]".format(col, unit)
            else:
                new_col = col
                
            new_cols.append(new_col)

        if value is None:
            
            data = pd.DataFrame(columns=new_cols)
                
            if (self._fixed_index_col is not None and
                self._fixed_index_names is not None):
                                
                for index_name in self._fixed_index_names:
                    
                    vals = [index_name] + [None] * (len(data.columns) - 1)
                    s1 = pd.Series(vals, index=data.columns)
                    data = data.append(s1, ignore_index=True)
                    
            if dtypes is not None:
                    
                for column, dtype in zip(data.columns, dtypes):
                    data[column] = data[column].astype(dtype)
                    
        else:
            
            data = value
            data.columns = new_cols
            
            if (self._fixed_index_col is not None and
                self._fixed_index_names is not None):
                
                data = data.set_index(self._fixed_index_col)
                data = data.reindex(self._fixed_index_names)
                data = data.reset_index()
                            
        return data

    def _get_result(self):
        
        model = self.datatable.model()
        df = model.dataFrame()
        
        # Nullify the variable if the dataframe is empty
        if df.empty: return
        
        # Rename the columns
        df.columns = self._columms

        return df
        
    def _get_read_event(self):

        return self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked
        
    def _get_nullify_event(self):

        return self.null_signal
        
    @QtCore.pyqtSlot(object)     
    def _emit_null(self, *args):
        
        self.null_signal.emit()
        
        return


class InputTimeTable(InputDataTable):
    
    null_signal = QtCore.pyqtSignal()

    def __init__(self, parent, columns, units=None):

        columns = ["DateTime"] + columns
        if units is not None: units = [None] + units

        InputDataTable.__init__(self, parent, columns, units)
        
        return
        
    def _get_dataframe(self, value, dtype=None):
        
        data = super(InputTimeTable, self)._get_dataframe(value, dtype)        
        data["DateTime"] = pd.to_datetime(data["DateTime"])
        
        return data

        
class InputLineTable(InputDataTable):
    
    null_signal = QtCore.pyqtSignal()
    
    def __init__(self, parent):
        
        columns = ["val1", "val2"]
        InputDataTable.__init__(self, parent, columns)
        
        return
    
    def _get_result(self):
        
        model = self.datatable.model()
        df = model.dataFrame()
        
        # Nullify the variable if the dataframe is empty
        if df.empty: return
            
        first_row = df.iloc[0]
        df.append(first_row, ignore_index=True)
        df = df.apply(pd.to_numeric)
        
        return df.values
        
        
class InputTriStateTable(InputDataTable):
    
    null_signal = QtCore.pyqtSignal()
    
    def _get_dataframe(self, value, dtype=None):
        
        data = super(InputTriStateTable, self)._get_dataframe(value, dtype)
        data = data.replace(["true", "false", "unknown"],
                            ["True", "False", None])
        
        return data
        
    def _get_result(self):
        
        model = self.datatable.model()
        df = model.dataFrame()
        
        # Nullify the variable if the dataframe is empty
        if df.empty: return
        
        # Rename the columns
        df.columns = self._columms
        
        get_cols = range(1, len(df.columns))
        
        check_df = df.iloc[:, get_cols]

        if not np.all(check_df.isin(["True", "False", "None", "", None])):
            
            errStr = ('Given input data is incorrectly formatted. It must '
                      'have values "True", "False", "None" or be empty.')
            raise ValueError(errStr)
        
        df = df.replace(["True", "False", "None", "", None],
                        ["true", "false", "unknown", "unknown", "unknown"])

        return df
        
        
class InputPointTable(InputDataTable):
    
    null_signal = QtCore.pyqtSignal()
    
    def __init__(self, parent):
        
        columns = ["x", "y", "z"]
        InputDataTable.__init__(self, parent, columns)
        
        return
    
    def _get_result(self):
        
        model = self.datatable.model()
        df = model.dataFrame()
        
        # Nullify the variable if the dataframe is empty
        if df.empty: return
            
        first_row = df.iloc[0]
        df.append(first_row, ignore_index=True)
        df = df.apply(pd.to_numeric)
        
        if df["z"].isnull().any(): df = df.drop("z", 1)
        
        return df.values
        

class InputDictTable(InputDataTable):
    
    null_signal = QtCore.pyqtSignal()
    
    def __init__(self, parent,
                       units=None,
                       fixed_index_names=None):
        
        columns = ["Key", "Value"]
        if units is not None: units = [None, units[0]]

        InputDataTable.__init__(self, parent,
                                      columns,
                                      units,
                                      "Key",
                                      fixed_index_names)
        
        return
    
    def _get_result(self):
        
        model = self.datatable.model()
        df = model.dataFrame()
        
        # Nullify the variable if the dataframe is empty or all values are
        # None
        if df.empty: return None
        
        df = df.replace(["None", ""],
                        [None, None])
            
        unique_values = df["Value"].unique()
        if len(unique_values) == 1 and unique_values[0] is None: return None 
      
        var_dict = {k: v for k, v in zip(df["Key"], df["Value"])}
        
        return var_dict


class InputHistogram(InputDataTable):
    
    def __init__(self, parent):
        
        columns = ["bins", "values"]
        InputDataTable.__init__(self, parent, columns)
        
        return
    
    def _get_result(self):
        
        model = self.datatable.model()
        df = model.dataFrame()
        
        # Nullify the variable if the dataframe is empty
        if df.empty: return
            
        first_row = df.iloc[0]
        df.append(first_row, ignore_index=True)
        df = df.apply(pd.to_numeric)
        
        values = df['values'].values
        bins = np.append(0,df['bins'].values)

        hist = (values,bins)
        
        return hist

        
class InputTimeSeries(InputDataTable):
    
    null_signal = QtCore.pyqtSignal()

    def __init__(self, parent, labels, units=None):

        columns = ["DateTime", labels[0]]

        if units is not None: units = [None, units[0]]

        InputDataTable.__init__(self, parent, columns, units)
        
        return
        
    def _get_dataframe(self, value, dtype=None):
        
        if value is not None:
            value.index.name = "DateTime"
            value = value.to_frame()
            value = value.reset_index()
        
        data = super(InputTimeSeries, self)._get_dataframe(value, dtype)        
        data["DateTime"] = pd.to_datetime(data["DateTime"])
        
        return data
        
    def _get_result(self):
        
        model = self.datatable.model()
        df = model.dataFrame()
        
        # Nullify the variable if the dataframe is empty
        if df.empty: return
            
        df = df.set_index("DateTime")
        series = df.ix[:,0]
        
        return series

