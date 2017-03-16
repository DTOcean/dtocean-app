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

from PyQt4 import QtCore, QtGui

import matplotlib.pyplot as plt

from aneris.utilities.misc import OrderedSet
from dtocean_core.pipeline import Tree

from .display import get_current_filetypes, save_current_figure
from ..designer.details import Ui_DetailsWidget
from ..designer.filemanager import Ui_FileManagerWidget
from ..designer.plotmanager import Ui_PlotManagerWidget
from ..designer.levelcomparison import Ui_LevelComparisonWidget
from ..designer.simcomparison import Ui_SimComparisonWidget


class ContextArea(QtGui.QWidget):
    
    def __init__(self, parent=None):
        
        super(ContextArea, self).__init__(parent)
        self._init_ui()
        
        return
        
    def _init_ui(self):
        
        self._topbox = QtGui.QHBoxLayout()
        self._hbox = QtGui.QHBoxLayout()
        self._top = QtGui.QWidget()
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
                                       QtGui.QSizePolicy.Preferred)
        		
        self._top_left = QtGui.QFrame()
        self._top_left.setFrameShape(QtGui.QFrame.StyledPanel)
        self._top_left.setMinimumWidth(350)
        self._top_left.setMinimumHeight(150)
        self._top_left.setMaximumWidth(450)                                       
        self._top_left.setSizePolicy(sizePolicy)
        
        self._top_left_box = QtGui.QHBoxLayout()
        self._top_left.setLayout(self._top_left_box)
        self._top_left_contents = None
        self._top_left_box.setContentsMargins(2, 2, 2, 2)
        
        self._top_right = QtGui.QFrame()
        self._top_right.setFrameShape(QtGui.QFrame.StyledPanel)
        self._top_right.setMinimumWidth(450)
        self._top_right_box = QtGui.QHBoxLayout()
        self._top_right.setLayout(self._top_right_box)
        self._top_right_contents = None
        self._top_right_box.setContentsMargins(2, 2, 2, 2)
        
        self._bottom = QtGui.QFrame()
        self._bottom.setFrameShape(QtGui.QFrame.StyledPanel)
        self._bottom_box = QtGui.QHBoxLayout()
        self._bottom.setLayout(self._bottom_box)
        self._bottom_contents = None
          
        self._topbox.addWidget(self._top_left)
        self._topbox.addWidget(self._top_right)
        self._top.setLayout(self._topbox)
        self._topbox.setContentsMargins(0, 0, 0, 2)
        		
        self._splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self._splitter.addWidget(self._top)
        self._splitter.addWidget(self._bottom)
        self._splitter.setStretchFactor(1, 2)
        
        self._hbox.addWidget(self._splitter)
        self.setLayout(self._hbox)
        self._hbox.setContentsMargins(0, 0, 2, 0)
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)
        
        return


class DetailsWidget(QtGui.QWidget, Ui_DetailsWidget):

    def __init__(self, parent):

        QtGui.QWidget.__init__(self, parent)
        Ui_DetailsWidget.__init__(self)
        
        self.setupUi(self)
        self._set_details(None, None)

        return
        
    def _set_details(self, title, description):
        
        if title is None: title = ""
        if description is None: description = ""
        
        titleStr = title.encode('utf-8')
        descriptionStr = description.encode('utf-8')

        self.titleLabel.setText(titleStr)
        self.descriptionLabel.setText(descriptionStr)

        return


class FileManagerWidget(QtGui.QWidget, Ui_FileManagerWidget):
    
    load_file = QtCore.pyqtSignal(object, str, str)
    save_file = QtCore.pyqtSignal(object, str, str)

    def __init__(self, parent):

        QtGui.QWidget.__init__(self, parent)
        Ui_FileManagerWidget.__init__(self)
        self._load_ext_dict = None
        self._save_ext_dict = None
        self._file_mode = None
        self._variable = None
        self._load_connected = False
        self._save_connected = False
        
        self._init_ui()

        return
        
    def _init_ui(self):
        
        self.setupUi(self)
        
        self.loadButton.clicked.connect(
                            lambda: self._set_file_mode("load"))
        self.saveButton.clicked.connect(
                            lambda: self._set_file_mode("save"))
        
        self.getPathButton.clicked.connect(self._set_path)
        self.pathEdit.textChanged.connect(self._set_okay)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(
                                                        self._emit_file_signal)
        
        return
        
    def _set_files(self, variable, load_ext_dict=None, save_ext_dict=None):
        
        self._variable = variable
        
        self.extBox.clear()
        self.pathEdit.clear()
        self.saveButton.setDisabled(True)
        self.loadButton.setDisabled(True)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDisabled(True)
        
        self._load_ext_dict = None
        self._save_ext_dict = None
        self._file_mode = None
        
        if variable is None or (load_ext_dict is None and
                                save_ext_dict is None):
            
            self.setDisabled(True)
            return
            
        else:
            
            self.setEnabled(True)
        
        if load_ext_dict is not None:
            
            self.loadButton.setEnabled(True)
            self._load_ext_dict = load_ext_dict
            
        if save_ext_dict is not None:
            
            self.saveButton.setEnabled(True)
            self._save_ext_dict = save_ext_dict
                        
        if load_ext_dict is not None:
            self.loadButton.setChecked(True)
            self._set_file_mode("load")
        else:
            self.saveButton.setChecked(True)
            self._set_file_mode("save")
            
        return

    @QtCore.pyqtSlot(str)
    def _set_file_mode(self, file_mode):
        
        self.extBox.clear()
        self.pathEdit.clear()
        
        if file_mode == "load":
            
            self._file_mode = "load"
            valid_exts = self._load_ext_dict.keys()
            
        elif file_mode == "save":
            
            self._file_mode = "save"
            valid_exts = self._save_ext_dict.keys()
            
        else:
            
            errStr = "Argument file_mode may only have values 'load' or 'save'"
            raise ValueError(errStr)
            
        for item in valid_exts:
            self.extBox.addItem(item)
 
        return
        
    @QtCore.pyqtSlot()    
    def _set_path(self):
        
        file_ext = str(self.extBox.currentText())
        file_ext_str = "(*{})".format(file_ext)
        
        if self._file_mode == "load":
            
            msg = "Load file"
            file_path = QtGui.QFileDialog.getOpenFileName(None,
                                                          msg,
                                                          '.',
                                                          file_ext_str)
        elif self._file_mode == "save":
            
            msg = "Save file"
            file_path = QtGui.QFileDialog.getSaveFileName(None,
                                                          msg,
                                                          '.',
                                                          file_ext_str)
            
        else:
            
            errStr = "There are children here somewhere. I can smell them."
            raise SystemError(errStr)
        
        self.pathEdit.setText(file_path)
        
        return
        
    @QtCore.pyqtSlot()    
    def _set_okay(self):
        
        file_path = str(self.pathEdit.text())
        
        if file_path:
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDisabled(True)
            
        return
        
    @QtCore.pyqtSlot()    
    def _emit_file_signal(self):
        
        file_mode = self._file_mode
        file_ext = str(self.extBox.currentText())
        file_path = str(self.pathEdit.text())
        
        if file_mode == "load":
        
            interface_name = self._load_ext_dict[file_ext]
            self.load_file.emit(self._variable, interface_name, file_path)

        elif file_mode == "save":
            
            interface_name = self._save_ext_dict[file_ext]
            self.save_file.emit(self._variable, interface_name, file_path)

        else:
            
            errStr = "Don't cross the streams!"
            raise SystemError(errStr)
        
        return

        
class PlotManagerWidget(QtGui.QWidget, Ui_PlotManagerWidget):
    
    plot = QtCore.pyqtSignal(object, object)

    def __init__(self, parent):

        QtGui.QWidget.__init__(self, parent)
        Ui_PlotManagerWidget.__init__(self)
        self._var_item = None
        self._ext_types = None
        self._plot_connected = False
        
        self._init_ui()

        return
        
    def _init_ui(self):
        
        self.setupUi(self)
        
        self.getPathButton.clicked.connect(self._set_path)
        self.pathEdit.textChanged.connect(self._set_save)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(
                                                    self._emit_named_plot)
        self.buttonBox.button(QtGui.QDialogButtonBox.Reset).clicked.connect(
                                                    self._emit_default_plot)
        self.buttonBox.button(QtGui.QDialogButtonBox.Save).clicked.connect(
                                                    self._save)
        
        return
        
    def _set_plots(self, var_item, plot_list=None, plot_auto=False):
        
        self._var_item = None
        self._ext_types = None
        
        if var_item is None or (plot_list is None and not plot_auto):
            
            self.setDisabled(True)
            return
        
        self.setEnabled(True)
        
        self._var_item = var_item
        self._ext_types = get_current_filetypes()
                
        if not self._ext_types:
            
            self.buttonBox.button(QtGui.QDialogButtonBox.Save
                                                          ).setDisabled(True)
            self.pathEdit.setDisabled(True)
            
        else:
            
            self.buttonBox.button(QtGui.QDialogButtonBox.Save
                                                          ).setEnabled(True)
            self.pathEdit.setEnabled(True)

        self._set_plot_list(plot_list, plot_auto)
        self._set_save()

        return
        
    def _set_plot_list(self, plot_list=None, plot_auto=False):
        
        self.plotBox.clear()
                
        if plot_list is None:
            
            self.plotBox.setDisabled(True)
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok
                                                          ).setDisabled(True)
            
        else:
            
            self.plotBox.setEnabled(True)
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok
                                                          ).setEnabled(True)
            
            for item in plot_list:
                self.plotBox.addItem(item)
                
        if plot_auto:
            self.buttonBox.button(QtGui.QDialogButtonBox.Reset
                                                          ).setEnabled(True)
        else:
            self.buttonBox.button(QtGui.QDialogButtonBox.Reset
                                                          ).setDisabled(True)
        
        return
        
    @QtCore.pyqtSlot()    
    def _set_path(self):

        if self._ext_types is None: return
        
        extlist = ["{} (*.{})".format(v, k) for k, v in
                                               self._ext_types.iteritems()]
        extStr = ";;".join(extlist)
        
        file_path = QtGui.QFileDialog.getSaveFileName(None,
                                                      "Save plot",
                                                      '.',
                                                      extStr)
        
        self.pathEdit.setText(file_path)
        
        return
        
    @QtCore.pyqtSlot()    
    def _set_save(self):
        
        file_path = str(self.pathEdit.text())
        
        if file_path:
            self.buttonBox.button(QtGui.QDialogButtonBox.Save
                                                          ).setEnabled(True)
        else:
            self.buttonBox.button(QtGui.QDialogButtonBox.Save
                                                          ).setDisabled(True)
            
        return

    @QtCore.pyqtSlot()    
    def _emit_named_plot(self):
        
        plot_name = str(self.plotBox.currentText())
        self.plot.emit(self._var_item, plot_name)
                
        return
        
    @QtCore.pyqtSlot()    
    def _emit_default_plot(self):
    
        self.plot.emit(self._var_item, None)

    @QtCore.pyqtSlot()    
    def _save(self):
        
        figure_path = str(self.pathEdit.text())
        save_current_figure(figure_path)
        
        self.pathEdit.clear()
        
        return


class ComparisonWidget(object):
        
    def __init__(self):

        self._var_ids = None
        self._mod_names = None

        self._init_ui()

        return
        
    def _init_ui(self):
        
        self.setupUi(self)
        
        # Buttons
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDisabled(True)
        self.buttonBox.button(QtGui.QDialogButtonBox.Save).setDisabled(True)
        
        return
        
    def _get_var_id(self, var_name):
        
        return self._var_ids[var_name]
        
    def _set_interfaces(self, shell, include_str=False):
        
        self.varBox.clear()
                
        active_modules = shell.module_menu.get_active(shell.core,
                                                      shell.project)
        
        active_themes = shell.theme_menu.get_active(shell.core,
                                                    shell.project)
        
        active_interfaces = active_modules + active_themes
        
        self._mod_names = active_modules
        self._set_variables(shell, active_interfaces, include_str)
            
        return
        
    def _set_variables(self, shell, active_interfaces, include_str=False):
        
        self.varBox.clear()
        
        tree = Tree()
        
        all_var_names = []
        var_id_dict = {}
        
        for interface_name in active_interfaces:
            
            branch = tree.get_branch(shell.core,
                                     shell.project,
                                     interface_name)
            
            var_inputs = branch.get_inputs(shell.core, shell.project)
            var_outputs = branch.get_outputs(shell.core, shell.project)
            
            unique_vars = OrderedSet(var_inputs + var_outputs)
            
            var_names = []
            var_names = []

            for var_id in unique_vars:
                
                var_meta = shell.core.get_metadata(var_id)

                if "SimpleData" in var_meta.structure:
                    
                    if var_meta.types is None:
                        
                        errStr = ("Variable {} with SimpleData structure "
                                  "requires types meta data to be "
                                  "set").format(var_id)
                        raise ValueError(errStr)
                        
                    if "int" in var_meta.types or "float" in var_meta.types:
                        var_names.append(var_meta.title)
                        
                    if include_str and "str" in var_meta.types:
                        var_names.append(var_meta.title)
                    
                    if var_meta.title not in var_id_dict:
                        var_id_dict[var_meta.title] = var_id
            
            all_var_names.extend(var_names)
            
        self._var_ids = var_id_dict
        
        self.varBox.addItems(all_var_names)
        self.varBox.setCurrentIndex(-1)
        
        return
        
    def _get_mode(self):
        
        # Collect the current mode
        if self.plotButton.isChecked():
            mode = "plot"
        elif self.dataButton.isChecked():
            mode = "data"
        else:
            errStr = "Hairy Japanese Bastards!"
            raise SystemError(errStr)
            
        return mode
        

class LevelComparison(QtGui.QWidget,
                      Ui_LevelComparisonWidget,
                      ComparisonWidget):
    
    plot_levels = QtCore.pyqtSignal(str, bool)
    tab_levels = QtCore.pyqtSignal(str, bool)
    save_plot = QtCore.pyqtSignal()
    save_data = QtCore.pyqtSignal()
    
    def __init__(self, parent):
        
        QtGui.QWidget.__init__(self, parent)
        Ui_LevelComparisonWidget.__init__(self)
        ComparisonWidget.__init__(self)
        
        return
        
    def _init_ui(self):
        
        super(LevelComparison, self)._init_ui()
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(
                                                self._emit_widget_request)
        self.buttonBox.button(QtGui.QDialogButtonBox.Save).clicked.connect(
                                                self._save)
        
        # Signals
        self.varBox.currentIndexChanged.connect(self._ok_button_ui_switch)
        
        return
        
    def _emit_widget_request(self):
                
        current_var = str(self.varBox.currentText())
        var_id = self._get_var_id(current_var)

        ignore_strategy = self.strategyBox.isChecked()
        
        if self._get_mode() == "plot":
            self.plot_levels.emit(var_id, ignore_strategy)
        elif self._get_mode() == "data":
            self.tab_levels.emit(var_id, ignore_strategy)
        else:
            errStr = "Down with this sort of thing"
            raise SystemError(errStr)
        
        return
        
    @QtCore.pyqtSlot()    
    def _save(self):
        
        if self._get_mode() == "plot":
            self.save_plot.emit()
        elif self._get_mode() == "data":
            self.save_data.emit()
        else:
            raise SystemError("We're hit! We took a hit!")
        
        return
        
    @QtCore.pyqtSlot(int)
    def _ok_button_ui_switch(self, box_number):
        
        if box_number == -1:
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDisabled(True)
        else:
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        
        return


class SimulationComparison(QtGui.QWidget,
                           Ui_SimComparisonWidget,
                           ComparisonWidget):
    
    plot_levels = QtCore.pyqtSignal(str, str, bool)
    tab_levels = QtCore.pyqtSignal(str, str, bool)
    save_plot = QtCore.pyqtSignal()
    save_data = QtCore.pyqtSignal()
    
    def __init__(self, parent):
        
        QtGui.QWidget.__init__(self, parent)
        Ui_SimComparisonWidget.__init__(self)
        ComparisonWidget.__init__(self)
        
        return
        
    def _init_ui(self):
        
        super(SimulationComparison, self)._init_ui()
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(
                                                    self._emit_widget_request)
        self.buttonBox.button(QtGui.QDialogButtonBox.Save).clicked.connect(
                                                    self._save)
        
        # Signals
        self.varBox.currentIndexChanged.connect(self._set_modules)
        self.modBox.currentIndexChanged.connect(self._ok_button_ui_switch)
        
        return
        
    @QtCore.pyqtSlot(int)
    def _set_modules(self, box_number):
        
        self.modBox.clear()
                
        if box_number != -1: self.modBox.addItems(self._mod_names)
        
        self.modBox.setCurrentIndex(-1)
                
        return

    @QtCore.pyqtSlot()
    def _emit_widget_request(self):
        
        current_var = str(self.varBox.currentText())
        var_id = self._get_var_id(current_var)

        current_mod = str(self.modBox.currentText())

        ignore_strategy = self.strategyBox.isChecked()

        if self._get_mode() == "plot":
            self.plot_levels.emit(var_id, current_mod, ignore_strategy)
        elif self._get_mode() == "data":
            self.tab_levels.emit(var_id, current_mod, ignore_strategy)
        else:
            errStr = "Careful now"
            raise SystemError(errStr)
        
        return
        
    @QtCore.pyqtSlot()    
    def _save(self):
        
        if self._get_mode() == "plot":
            self.save_plot.emit()
        elif self._get_mode() == "data":
            self.save_data.emit()
        else:
            raise SystemError("Shut up, shut up, shut up!")
        
        return
        
    @QtCore.pyqtSlot(int)
    def _ok_button_ui_switch(self, box_number):
        
        if box_number == -1:
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDisabled(True)
        else:
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        
        return

