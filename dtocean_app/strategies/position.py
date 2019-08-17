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

import os
import multiprocessing
from copy import deepcopy

from PyQt4 import QtCore, QtGui

from dtocean_core.strategies.position import AdvancedPosition
from dtocean_core.strategies.position_optimiser import (dump_config,
                                                        load_config_template)
from dtocean_qt.models.DataFrameModel import DataFrameModel

from . import GUIStrategy, StrategyWidget, PyQtABCMeta
from ..utils.display import is_high_dpi
from ..widgets.datatable import DataTableWidget

if is_high_dpi():
    
    from ..designer.high.advancedposition import Ui_AdvancedPositionWidget
    
else:
    
    from ..designer.low.advancedposition import Ui_AdvancedPositionWidget


class GUIAdvancedPosition(GUIStrategy, AdvancedPosition):
    
    """
    """
    
    __metaclass__ = PyQtABCMeta
    
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
        
        config = load_config_template()
        widget = AdvancedPositionWidget(parent, shell, config)
        
        return widget
    
    @classmethod
    def get_worker_directory_status(cls, config):
        
        worker_directory = config["worker_dir"]
        
        status_str = None
        status_code = None
        
        if os.path.isdir(worker_directory):
            
            if len(os.listdir(worker_directory)) == 0:
                
                status_str = "Worker directory empty"
                status_code = 1
            
            elif not config['clean_existing_dir']:
                
                status_str = "Worker directory contains files"
                status_code = 0
        
        else:
            
            status_str = "Worker directory does not yet exist"
            status_code = 1
        
        return status_str, status_code
    
    @classmethod
    def get_optimiser_status(cls, config):
        
        root_project_path = config['root_project_path']
        worker_directory = config["worker_dir"]
        
        status_str = None
        status_code = None
        
        if os.path.isdir(worker_directory):
            
            _, root_project_name = os.path.split(root_project_path)
            root_project_base_name, _ = os.path.splitext(root_project_name)
            pickle_name = "{}_results.pkl".format(root_project_base_name)
            
            results_path = os.path.join(worker_directory, pickle_name)
            
            if os.path.isfile(results_path):
                
                status_str = "Optimisation complete"
                status_code = 1
        
        return status_str, status_code


class AdvancedPositionWidget(QtGui.QWidget,
                             Ui_AdvancedPositionWidget,
                             StrategyWidget):
    
    __metaclass__ = PyQtABCMeta
    
    config_set = QtCore.pyqtSignal()
    config_null = QtCore.pyqtSignal()
    
    def __init__(self, parent, shell, config):
        
        QtGui.QWidget.__init__(self, parent)
        Ui_AdvancedPositionWidget.__init__(self)
        StrategyWidget.__init__(self)
        
        self._shell = shell
        self._config = self._init_config(config)
        self._max_threads = multiprocessing.cpu_count()
        self._init_ui()
        
        return
    
    def _init_config(cls, config):
        
        config["threads_auto"] = False
        
        if config["root_project_path"] is None:
            config["root_project_path"] = "worker.prj"
        
        return config
    
    
    def _init_ui(self):
        
        ## INIT
        
        self.setupUi(self)
        
        ## CONTROL TAB
        
        self.nThreadSpinBox.setMaximum(self._max_threads)
        self.autoThreadBox.setDisabled(True)
        
        self.set_manual_thread_message()
        self._set_objective_variables()
        
        self.importButton.clicked.connect(self._import_config)
        self.exportButton.clicked.connect(self._export_config)
        self.workdirLineEdit.returnPressed.connect(self._update_worker_dir)
        self.workdirToolButton.clicked.connect(self._select_worker_dir)
        self.nThreadSpinBox.valueChanged.connect(self._update_n_threads)
        self.penaltyDoubleSpinBox.valueChanged.connect(
                                                    self._update_base_penalty)
        self.cleanDirCheckBox.stateChanged.connect(
                                            self._update_clean_existing_dir)
        self.abortSpinBox.valueChanged.connect(self._update_max_simulations)
        
        ## RESULTS TAB
        
        self.tabWidget.setTabEnabled(2, False)
        
        self.dataTableWidget = DataTableWidget(self,
                                               edit_rows=False,
                                               edit_cols=False,
                                               edit_cells=False)
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Expanding)
        self.dataTableWidget.setSizePolicy(sizePolicy)
        
        self.dataTableLayout.addWidget(self.dataTableWidget)
        
        ## GLOBAL
        
        self._shell.project.sims_updated.connect(self._update_status)
        
        self._update_status(init=True)
        
        return
    
    def _set_objective_variables(self):
        
        objective_variable = "project.lcoe_mode"
        var_meta = self._shell.core.get_metadata(objective_variable)
        var_text = var_meta.title
        
        self.costVarComboBox.addItem(var_text)
        
        if not var_meta.units:
            self.penaltyUnitsLabel.clear()
        else:
            label_str = "({})".format(var_meta.units[0])
            self.penaltyUnitsLabel.setText(label_str)
        
        return
    
    def set_manual_thread_message(self):
        
        thread_msg = "({} threads available)".format(self._max_threads)
        self.threadInfoLabel.setText(thread_msg)
        
        return
    
    @QtCore.pyqtSlot()
    def _update_status(self, init=False):
        
#        # Pick up the current tab to reload after update
#        current_tab_idx = self.tabWidget.currentIndex()
#        print current_tab_idx
        
        ## CONTROL TAB
        
        color_map = {0: "#aa0000",
                     1: "#00aa00"}
        
        (project_status_strs,
         project_status_code) = GUIAdvancedPosition.get_project_status(
                                                         self._shell.core,
                                                         self._shell.project)
        
        (config_status_str,
         config_status_code) = GUIAdvancedPosition.get_config_status(
                                                                 self._config)
        
        status_template = '<li style="color: {};">{}</li>'
        status_str = ""
        optimiser_status_str = None
        
        for project_status_str in project_status_strs:
            status_str += \
                    status_template.format(color_map[project_status_code],
                                           project_status_str)
        
        status_str += status_template.format(color_map[config_status_code],
                                             config_status_str)
        
        if self._config["worker_dir"] is not None:
            
            (worker_dir_status_str,
             worker_dir_status_code) = \
                 GUIAdvancedPosition.get_worker_directory_status(self._config)
            
            if worker_dir_status_str is not None:
                status_str += \
                    status_template.format(color_map[worker_dir_status_code],
                                           worker_dir_status_str)
            
            (optimiser_status_str,
             optimiser_status_code) = \
                     GUIAdvancedPosition.get_optimiser_status(self._config)
            
            if optimiser_status_str is not None:
                status_str += \
                    status_template.format(color_map[optimiser_status_code],
                                           optimiser_status_str)
        
        # Define a global status
        if (config_status_code == 0 or
            project_status_code == 0 or
            worker_dir_status_code == 0):
            
            status_code = 0
            
        else:
            
            status_code = 1
        
        status_str_rich = ('<html><head/><body><p><span '
                           'style="font-size: 10pt;">'
                           '<ul>{}</ul>'
                           '</span></p></body></html>').format(status_str)
        
        self.statusLabel.setText(status_str_rich)
        
        if status_code > 0:
            self.config_set.emit()
        else:
            self.config_null.emit()
        
        if init:
            
            if self._config["worker_dir"] is not None:
                self.workdirLineEdit.setText(self._config["worker_dir"])
            
            if self._config["n_threads"] is not None:
                self.nThreadSpinBox.setValue(self._config["n_threads"])
            
            if self._config["base_penalty"] is not None:
                self.penaltyDoubleSpinBox.setValue(
                                                self._config["base_penalty"])
            
            if self._config["clean_existing_dir"] is not None:
                
                if self._config["clean_existing_dir"]:
                    
                    if not self.cleanDirCheckBox.isChecked():
                        self.cleanDirCheckBox.toggle()
                
                else:
                    
                    if self.cleanDirCheckBox.isChecked():
                        self.cleanDirCheckBox.toggle()
            
            if self._config["max_simulations"] is not None:
                self.abortSpinBox.setValue(self._config["max_simulations"])
            
            if self._config["threads_auto"]:
                
                if not self.autoThreadBox.isChecked():
                    
                    self.autoThreadBox.toggle()
                    self.threadInfoLabel.setText("Auto mode")
        
            else:
                
                if self.autoThreadBox.isChecked():
                    
                    self.autoThreadBox.toggle()
                    self.set_manual_thread_message()
        
        ## RESULTS TAB
        if optimiser_status_str is None:
            
            self.tabWidget.setTabEnabled(2, False)
        
        else:
            
            self.tabWidget.setTabEnabled(2, True)
           
            df = GUIAdvancedPosition.get_results_table(self._config)
            model = DataFrameModel(df)
            self.dataTableWidget.setViewModel(model)
        
        return
    
    @QtCore.pyqtSlot()
    def _import_config(self):
        
        msg = "Import Configuration"
        valid_exts = "Configuration files (*.yaml *.yml)"
        
        file_path = QtGui.QFileDialog.getOpenFileName(self,
                                                      msg,
                                                      '.',
                                                      valid_exts)
        
        if not file_path: return
        
        config = GUIAdvancedPosition.load_config(file_path)
        self._config = self._init_config(config)
        
        self._update_status(init=True)
        
        return
    
    @QtCore.pyqtSlot()
    def _export_config(self):
        
        msg = "Export Configuration"
        valid_exts = "Configuration files (*.yaml *.yml)"
        
        file_path = QtGui.QFileDialog.getSaveFileName(self,
                                                      msg,
                                                      '.',
                                                      valid_exts)
        
        if not file_path: return
        
        config_template = load_config_template()
        config = deepcopy(self._config)
        config.pop("threads_auto")
        
        config_template.update(config)
        dump_config(config_template, file_path)
        
        return
    
    @QtCore.pyqtSlot()
    def _update_worker_dir(self):
        
        self._config["worker_dir"] = str(self.workdirLineEdit.text())
        self.workdirLineEdit.clearFocus()
        self._update_status()
        
        return
    
    @QtCore.pyqtSlot()
    def _select_worker_dir(self):
        
        title_str = 'Select Directory for Worker Files'
        worker_dir = QtGui.QFileDialog.getExistingDirectory(
                                                self,
                                                title_str,
                                                self._config["worker_dir"],
                                                QtGui.QFileDialog.ShowDirsOnly)
        
        if worker_dir:
            
            self._config["worker_dir"] = str(worker_dir)
            self.workdirLineEdit.setText(worker_dir)
            self._update_status()
        
        return
    
    @QtCore.pyqtSlot(int)
    def _update_n_threads(self, n_threads):
        
        if n_threads > 0:
            self._config["n_threads"] = n_threads
        else:
            self._config["n_threads"] = None
        
        self._update_status()
        
        return
    
    @QtCore.pyqtSlot(float)
    def _update_base_penalty(self, penalty_value):
        
        self._config["base_penalty"] = penalty_value
        
        return
    
    @QtCore.pyqtSlot(object)
    def _update_clean_existing_dir(self, checked_state):
        
        if checked_state == QtCore.Qt.Checked:
            self._config["clean_existing_dir"] = True
        else:
            self._config["clean_existing_dir"] = None
        
        self._update_status()
        
        return
    
    @QtCore.pyqtSlot(int)
    def _update_max_simulations(self, max_simulations):
        
        if max_simulations > 0:
            self._config["max_simulations"] = max_simulations
        else:
            self._config["max_simulations"] = None
        
        return
    
    def get_configuration(self):
        
        '''A method for getting the dictionary to configure the strategy.
        
        Returns:
          dict
        '''
        
        # Update any other value that might have been imported.
        self._config["root_project_path"] = "worker.prj"
        
        return self._config
    
    def set_configuration(self, config_dict=None):
        
        '''A method for displaying the configuration in the gui.
        
        Arguments:
          config_dict (dict, optional)
        '''
        
        if config_dict is not None: self._config = config_dict
        
        self._update_status()
        
        return
