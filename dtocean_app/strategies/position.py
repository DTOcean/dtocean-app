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
import sys
import logging
import traceback
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
from ..widgets.dialogs import ProgressBar

if is_high_dpi():
    
    from ..designer.high.advancedposition import Ui_AdvancedPositionWidget
    
else:
    
    from ..designer.low.advancedposition import Ui_AdvancedPositionWidget

# Set up logging
module_logger = logging.getLogger(__name__)

# User home directory
HOME = os.path.expanduser("~")


class ThreadLoadSimulations(QtCore.QThread):
    
    """QThread for loading simulations"""
    
    taskFinished = QtCore.pyqtSignal()
    error_detected =  QtCore.pyqtSignal(object, object, object)
    
    def __init__(self, shell, sim_numbers, exclude_default):
        
        super(ThreadLoadSimulations, self).__init__()
        self._shell = shell
        self._sim_numbers = sim_numbers
        self._exclude_default = exclude_default
        
        return
    
    def run(self):
        
        try:
            
            # Block signals
            self._shell.core.blockSignals(True)
            self._shell.project.blockSignals(True)
            
            self._shell.strategy.remove_simulations(
                                        self._shell.core,
                                        self._shell.project,
                                        exclude_default=self._exclude_default)
            
            self._shell.strategy.load_simulations(self._shell.core,
                                                  self._shell.project,
                                                  self._sim_numbers)
        
        except: 
            
            etype, evalue, etraceback = sys.exc_info()
            self.error_detected.emit(etype, evalue, etraceback)
        
        finally:
            
            # Reinstate signals and emit
            self._shell.core.blockSignals(False)
            self._shell.project.blockSignals(False)
            self.taskFinished.emit()
        
        return


class GUIAdvancedPosition(GUIStrategy, AdvancedPosition):
    
    """GUI for AdvancedPosition strategy.
    """
    
    __metaclass__ = PyQtABCMeta
    
    def __init__(self):
        
        AdvancedPosition.__init__(self)
        GUIStrategy.__init__(self)
        
        return
    
    @property
    def allow_rerun(self):
        
        return True
    
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
        self._progress = None
        self._results_df = None
        self._protect_default = True
        self._sims_to_load = None
        self._load_sims_thread = None
        
        self._init_ui(parent)
        
        return
    
    def _init_config(cls, config):
        
        config["threads_auto"] = False
        
        if config["root_project_path"] is None:
            config["root_project_path"] = "worker.prj"
        
        return config
    
    
    def _init_ui(self, parent):
        
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
        
        self.simButtonGroup.setId(self.bestSimButton, 1)
        self.simButtonGroup.setId(self.worstSimButton, 2)
        self.simButtonGroup.setId(self.top5SimButton, 3)
        self.simButtonGroup.setId(self.bottom5SimButton, 4)
        self.simButtonGroup.setId(self.customSimButton, 5)
        
        self.dataTableWidget = DataTableWidget(self,
                                               edit_rows=False,
                                               edit_cols=False,
                                               edit_cells=False)
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Expanding)
        self.dataTableWidget.setSizePolicy(sizePolicy)
        
        self.dataTableLayout.addWidget(self.dataTableWidget)
        
        self.protectDefaultBox.stateChanged.connect(
                                                self._update_protect_default)
        self.simButtonGroup.buttonClicked['int'].connect(
                                                    self._select_sims_to_load)
        self.simSelectEdit.textEdited.connect(self._update_custom_sims)
        self.simLoadButton.clicked.connect(self._progress_load_sims)
        self.dataExportButton.clicked.connect(self._export_data_table)
        
        ## GLOBAL
        
        # Set up progress bar
        self._progress = ProgressBar(parent)
        self._progress.setModal(True)
        
        self._shell.project.sims_updated.connect(self._update_status)
        self._shell.strategy_selected.connect(self._update_status)
        
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
            
            if optimiser_status_str is not None:
            
                status_code = 1
                self._config["force_strategy_run"] = False
            
            else:
                
                status_code = 0
            
        else:
            
            status_code = 1
            
            if "force_strategy_run" in self._config:
                self._config.pop("force_strategy_run")
        
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
        
        results_open = (optimiser_status_str is not None and
                        self._shell.strategy is not None and
                        self._config == self._shell.strategy._config)
        
        if not results_open:
            
            self.tabWidget.setTabEnabled(2, False)
            self._results_df = None
        
        else:
            
            self.tabWidget.setTabEnabled(2, True)
            
            if "Default" not in self._shell.project.get_simulation_titles():
                self.protectDefaultBox.setEnabled(False)
                self._protect_default = False
            else:
                self.protectDefaultBox.setEnabled(True)
                self.protectDefaultBox.stateChanged.emit(
                                        self.protectDefaultBox.checkState())
            
            if self._sims_to_load is None:
                self.simLoadButton.setDisabled(True)
            else:
                self.simLoadButton.setEnabled(True)
            
            if self._results_df is None:
            
                # TODO: This needs automating.
                # Consider adding names and units to config file and using
                # meta data for variables.
                name_map = {"sim_number": "Simulation #",
                            "project.lcoe_mode": "LCOE Mode",
                            "array_orientation": "Grid Orientation",
                            "delta_row": "Row Spacing",
                            "delta_col": "Column Spacing",
                            "n_nodes": "No. of Devices Requested",
                            "project.number_of_devices":
                                "No. of Devices Simulated",
                            "project.annual_energy":
                                "Annual Mechanical Energy",
                            "project.q_factor": "q-factor",
                            "project.capex_total": "CAPEX",
                            "project.capex_breakdown": "CAPEX",
                            "project.lifetime_opex_mode": "OPEX Mode",
                            "project.lifetime_energy_mode":
                                "Lifetime Energy Mode"}
                
                unit_map = {"project.lcoe_mode": "Euro/kWh",
                            "array_orientation": "Rad",
                            "delta_row": "m",
                            "delta_col": "m",
                            "project.annual_energy": "MWh",
                            "project.capex_total": "Euro",
                            "project.capex_breakdown": "Euro",
                            "project.lifetime_opex_mode": "Euro",
                            "project.lifetime_energy_mode": "MWh"}
                
                df = GUIAdvancedPosition.get_results_table(self._config)
                
                new_columns = []
                
                for column in df.columns:
                    
                    for key in name_map.keys():
                        
                        if key in column:
                            
                            column = column.replace(key, name_map[key])
                            
                            if key in unit_map:
                                column += " ({})".format(unit_map[key])
                            
                            break
                    
                    new_columns.append(column)
                
                df.columns = new_columns
                
                self._results_df = df
            
            model = DataFrameModel(self._results_df)
            self.dataTableWidget.setViewModel(model)
        
        return
    
    @QtCore.pyqtSlot()
    def _import_config(self):
        
        msg = "Import Configuration"
        valid_exts = "Configuration files (*.yaml *.yml)"
        
        file_path = QtGui.QFileDialog.getOpenFileName(self,
                                                      msg,
                                                      HOME,
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
                                                      HOME,
                                                      valid_exts)
        
        if not file_path: return
        
        config_template = load_config_template()
        config = deepcopy(self._config)
        config.pop("threads_auto")
        
        if "force_strategy_run" in self.config:
            config.pop("force_strategy_run")
        
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
        
        if self._config["worker_dir"]:
            start_dir = self._config["worker_dir"]
        else:
            start_dir = HOME
        
        title_str = 'Select Directory for Worker Files'
        worker_dir = QtGui.QFileDialog.getExistingDirectory(
                                                self,
                                                title_str,
                                                start_dir,
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
    
    @QtCore.pyqtSlot(object)
    def _update_protect_default(self, checked_state):
        
        if checked_state == QtCore.Qt.Checked:
            self._protect_default = True
        else:
            self._protect_default = False
        
        return
    
    @QtCore.pyqtSlot(int)
    def _select_sims_to_load(self, button_id):
        
        lcoe_column = self._results_df.columns[1]
        print lcoe_column
        
        if button_id == 1:
            
            check_df = self._results_df.sort_values(by=[lcoe_column])
            self._sims_to_load = check_df["Simulation #"][:1].tolist()
        
        elif button_id == 2:
            
            check_df = self._results_df.sort_values(by=[lcoe_column],
                                                    ascending=False)
            self._sims_to_load = check_df["Simulation #"][:1].tolist()
        
        elif button_id == 3:
            
            check_df = self._results_df.sort_values(by=[lcoe_column])
            self._sims_to_load = check_df["Simulation #"][:5].tolist()
        
        elif button_id == 4:
            
            check_df = self._results_df.sort_values(by=[lcoe_column],
                                                    ascending=False)
            self._sims_to_load = check_df["Simulation #"][:5].tolist()
        
        else:
            
            self._update_custom_sims(update_status=False)
        
        print self._sims_to_load
        
        if button_id == 5:
            custom_enabled = True
        else:
            custom_enabled = False
        
        self.simsLabel.setEnabled(custom_enabled)
        self.simSelectEdit.setEnabled(custom_enabled)
        self.simHelpLabel.setEnabled(custom_enabled)
        
        self._update_status()
        
        return
    
    @QtCore.pyqtSlot()
    def _update_custom_sims(self, update_status=True):
        
        sims_to_load_str = str(self.simSelectEdit.text())
        sims_to_load = None
            
        if sims_to_load_str:
            
            sims_to_load_strs = sims_to_load_str.split(",")
            
            try:
                sims_to_load = [int(x) for x in sims_to_load_strs]
            except:
                pass
        
        self._sims_to_load = sims_to_load
        
        if update_status:
            self._update_status()
        
        return
    
    @QtCore.pyqtSlot()
    def _progress_load_sims(self):
        
        self._progress.allow_close = False
        self._progress.set_pulsing()
        
        if self._load_sims_thread is not None: return
        
        self._load_sims_thread = ThreadLoadSimulations(self._shell,
                                                       self._sims_to_load,
                                                       self._protect_default)
        
        self._load_sims_thread.start()
        self._load_sims_thread.error_detected.connect(self._display_error)
        self._load_sims_thread.taskFinished.connect(self._finish_load_sims)
        
        self._progress.show()
        
        return
    
    @QtCore.pyqtSlot()
    def _finish_load_sims(self):
        
        self._load_sims_thread.error_detected.disconnect()
        self._load_sims_thread.taskFinished.disconnect()
        self._load_sims_thread = None
        
        # Emit signals on project
        self._shell.project.sims_updated.emit()
        self._shell.project.set_active_index(index=0)
        
        # Update the interface status
        self._shell.core.set_interface_status(self._shell.project)
        
        self._progress.allow_close = True
        self._progress.close()
        
        return
    
    @QtCore.pyqtSlot()
    def _export_data_table(self):
        
        extlist = ["comma-separated values (*.csv)"]
        extStr = ";;".join(extlist)
        
        fdialog_msg = "Save data"
            
        save_path = QtGui.QFileDialog.getSaveFileName(self,
                                                      fdialog_msg,
                                                      HOME,
                                                      extStr)
        
        if not save_path:return
        
        self._results_df.to_csv(str(save_path), index=False)
        
        return
    
    @QtCore.pyqtSlot(object, object, object)  
    def _display_error(self, etype, evalue, etraceback):
        
        type_str = str(etype)
        type_strs = type_str.split(".")
        sane_type_str = type_strs[-1].replace("'>", "")
        
        if sane_type_str[0].lower() in "aeiou":
            article = "An"
        else:
            article = "A"
        
        errMsg = "{} {} occurred: {:s}".format(article, sane_type_str, evalue)
        
        module_logger.critical(errMsg)
        module_logger.critical(''.join(traceback.format_tb(etraceback)))
        QtGui.QMessageBox.critical(self, "ERROR", errMsg)
        
        return
    
    def get_configuration(self):
        
        '''A method for getting the dictionary to configure the strategy.
        
        Returns:
          dict
        '''
        
        return self._config
    
    def set_configuration(self, config_dict=None):
        
        '''A method for displaying the configuration in the gui.
        
        Arguments:
          config_dict (dict, optional)
        '''
        
        if config_dict is not None: self._config = config_dict
        
        self._update_status()
        
        return
