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

import sip
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image
from PyQt4 import QtCore, QtGui

from dtocean_core.strategies.position import AdvancedPosition
from dtocean_core.strategies.position_optimiser import (dump_config,
                                                        load_config_template)
from dtocean_qt.models.DataFrameModel import DataFrameModel

from . import GUIStrategy, StrategyWidget, PyQtABCMeta
from ..utils.display import is_high_dpi
from ..widgets.datatable import DataTableWidget
from ..widgets.dialogs import ProgressBar
from ..widgets.display import (MPLWidget,
                               get_current_figure_size,
                               get_current_filetypes)
from ..widgets.scientificselect import ScientificDoubleSpinBox

if is_high_dpi():
    
    from ..designer.high.advancedposition import Ui_AdvancedPositionWidget
    
else:
    
    from ..designer.low.advancedposition import Ui_AdvancedPositionWidget

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

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
        self._plot_ext_types = get_current_filetypes()
        self._progress = None
        self._results_df = None
        self._protect_default = True
        self._sims_to_load = None
        self._load_sims_thread = None
        self._param_boxes = {}
        self._param_lines = []
        
        self._name_map = {"sim_number": "Simulation #",
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
                              "Lifetime Energy Mode",
                          "device.minimum_distance_x":
                              "Minimum device spacing in x-direction",
                          "device.minimum_distance_y":
                              "Minimum device spacing in y-direction"}
        
        self._unit_map = {"project.lcoe_mode": "Euro/kWh",
                          "array_orientation": "Deg",
                          "delta_row": "m",
                          "delta_col": "m",
                          "project.annual_energy": "MWh",
                          "project.capex_total": "Euro",
                          "project.capex_breakdown": "Euro",
                          "project.lifetime_opex_mode": "Euro",
                          "project.lifetime_energy_mode": "MWh"}
        
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
        
        # Signals
        
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
        
        ## PARAMS TAB
        
        param_names = ["array_orientation",
                       "delta_row",
                       "delta_col",
                       "n_nodes",
                       "t1",
                       "t2"]
        
        param_box_classes = {"array_orientation": QtGui.QDoubleSpinBox,
                             "delta_row": QtGui.QDoubleSpinBox,
                             "delta_col": QtGui.QDoubleSpinBox,
                             "n_nodes": QtGui.QSpinBox,
                             "t1": QtGui.QDoubleSpinBox,
                             "t2": QtGui.QDoubleSpinBox}
        
        param_multipier_vars = {"delta_row": ["device.minimum_distance_x"],
                                "delta_col": ["device.minimum_distance_y"]}
        
        param_limits_dict = {"array_orientation": (-90, 90),
                             "delta_row": (0, None),
                             "delta_col": (0, None),
                             "n_nodes": (0, None),
                             "t1": (0, 1),
                             "t2": (0, 1)}
        
        for param_name in param_names:
            
            if param_name in self._name_map:
                human_name = self._name_map[param_name]
            else:
                human_name = param_name
            
            if param_name in self._unit_map:
                human_name += " ({})".format(self._unit_map[param_name])
            
            box_class = param_box_classes[param_name]
            var_box = make_var_box(self,
                                   self.paramsFrame,
                                   human_name,
                                   box_class)
            self.paramsFrameLayout.addWidget(var_box["root"])
            
            box_minimum = -sys.maxint
            box_maximum = sys.maxint
            set_box_min = False
            set_box_max = False
            
            if param_name in param_limits_dict:
                
                param_limits = param_limits_dict[param_name]
                
                if param_limits[0] is not None:
                    box_minimum = param_limits[0]
                    set_box_min = True
                
                if param_limits[1] is not None:
                    box_maximum = param_limits[1]
                    set_box_max = True
            
            var_box["fixed.box"].setMinimum(box_minimum)
            var_box["fixed.box"].setMaximum(box_maximum)
            
            var_box["range.box.min"].setMinimum(box_minimum)
            var_box["range.box.min"].setMaximum(box_maximum)
            if set_box_min: var_box["range.box.min"].setValue(box_minimum)
            
            var_box["range.box.max"].setMinimum(box_minimum)
            var_box["range.box.max"].setMaximum(box_maximum)
            if set_box_max: var_box["range.box.max"].setValue(box_maximum)
            
            var_box["range.box.type"].addItem("Fixed")
            var_box["range.box.var"].setEnabled(False)
            
            if param_name in param_multipier_vars:
            
                var_box["range.box.type"].addItem("Multiplier")
                
                for var in param_multipier_vars[param_name]:
                    
                    mapped_name = self._name_map[var]
                    var_box["range.box.var"].addItem(mapped_name)
            
            self._param_boxes[param_name] = var_box
            
            if i != len(param_names) - 1:
                
                line_name = "{} Line".format(param_name)
                line = QtGui.QFrame(self.paramsFrame)
                line.setFrameShape(QtGui.QFrame.HLine)
                line.setFrameShadow(QtGui.QFrame.Sunken)
                line.setObjectName(_fromUtf8(line_name))
                self.paramsFrameLayout.addWidget(line)
            
                self._param_lines.append(line)
        
        final_spacer = QtGui.QSpacerItem(20,
                                         20,
                                         QtGui.QSizePolicy.Minimum,
                                         QtGui.QSizePolicy.Expanding)
        self.paramsFrameLayout.addItem(final_spacer)
        
        ## RESULTS TAB
        
        self.tabWidget.setTabEnabled(2, False)
        
        self.simButtonGroup.setId(self.bestSimButton, 1)
        self.simButtonGroup.setId(self.worstSimButton, 2)
        self.simButtonGroup.setId(self.top5SimButton, 3)
        self.simButtonGroup.setId(self.bottom5SimButton, 4)
        self.simButtonGroup.setId(self.customSimButton, 5)
        
        # Data table
        
        self.dataTableWidget = DataTableWidget(self,
                                               edit_rows=False,
                                               edit_cols=False,
                                               edit_cells=False)
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Preferred)
        self.dataTableWidget.setSizePolicy(sizePolicy)
        self.dataTableWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.dataTableLayout.addWidget(self.dataTableWidget)
        
        ## PLOTS TAB
        
        # Add spin boxes
        
        self.xAxisMinSpinBox = _init_sci_spin_box(self, "xAxisMinSpinBox")
        self.xAxisMinLayout.addWidget(self.xAxisMinSpinBox)
        self.xAxisMaxSpinBox = _init_sci_spin_box(self, "xAxisMaxSpinBox")
        self.xAxisMaxLayout.addWidget(self.xAxisMaxSpinBox)
        
        self.yAxisMinSpinBox = _init_sci_spin_box(self, "yAxisMinSpinBox")
        self.yAxisMinLayout.addWidget(self.yAxisMinSpinBox)
        self.yAxisMaxSpinBox = _init_sci_spin_box(self, "yAxisMaxSpinBox")
        self.yAxisMaxLayout.addWidget(self.yAxisMaxSpinBox)
        
        self.colorAxisMinSpinBox = _init_sci_spin_box(self,
                                                      "colorAxisMinSpinBox")
        self.colorAxisMinLayout.addWidget(self.colorAxisMinSpinBox)
        self.colorAxisMaxSpinBox = _init_sci_spin_box(self,
                                                      "colorAxisMaxSpinBox")
        self.colorAxisMaxLayout.addWidget(self.colorAxisMaxSpinBox)
        
        self.filterVarMinSpinBox = _init_sci_spin_box(self,
                                                      "filterVarMinSpinBox")
        self.filterVarMinLayout.addWidget(self.filterVarMinSpinBox)
        self.filterVarMaxSpinBox = _init_sci_spin_box(self,
                                                      "filterVarMaxSpinBox")
        self.filterVarMaxLayout.addWidget(self.filterVarMaxSpinBox)
        
        # Add plot widget holder
        self.plotWidget = None
        
        # Signals
        
        self.protectDefaultBox.stateChanged.connect(
                                                self._update_protect_default)
        self.simButtonGroup.buttonClicked['int'].connect(
                                                    self._select_sims_to_load)
        self.simSelectEdit.textEdited.connect(self._update_custom_sims)
        self.simLoadButton.clicked.connect(self._progress_load_sims)
        self.dataExportButton.clicked.connect(self._export_data_table)
        self.plotButton.clicked.connect(self._set_plot)
        self.plotExportButton.clicked.connect(self._get_export_details)
        
        ## GLOBAL
        
        # Set up progress bar
        self._progress = ProgressBar(parent)
        self._progress.setModal(True)
        
        # Signals
        
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
        
        ## PARAMS TAB
        
        # Read the config file
        if init:
            
            parameters = self._config["parameters"]
            
            for param_name in parameters:
                
                param_settings = parameters[param_name]
                var_box = self._param_boxes[param_name]
                
                if "fixed" in param_settings and param_settings["fixed"]:
                    
                    var_box["fixed.check"].toggle()
                    var_box["fixed.box"].setValue(param_settings["fixed"])
                    
                    continue
                
                if "range" in param_settings and param_settings["range"]:
                    
                    range_settings = param_settings["range"]
                    
                    if range_settings["type"] == "multiplier":
                        
                        var_box["range.box.type"].setCurrentIndex(1)
                        
                        range_var_text = self._name_map[
                                                    range_settings["variable"]]
                        multi_var_idx = var_box["range.box.var"].findText(
                                                                range_var_text)
                        var_box["range.box.var"].setCurrentIndex(multi_var_idx)
                        var_box["range.box.var"].setEnabled(True)
                        
                        min_range = range_settings["min_multiplier"]
                        max_range = range_settings["max_multiplier"]
                    
                    elif range_settings["type"] == "fixed":
                        
                        min_range = range_settings["min"]
                        max_range = range_settings["max"]
                    
                    else:
                        
                        err_str = ("Unrecognised range type "
                                   "'{}'").format(range_settings["type"])
                        raise ValueError(err_str)
                    
                    var_box["range.box.min"].setValue(min_range)
                    var_box["range.box.max"].setValue(max_range)
                
                if "interp" in param_settings and param_settings["interp"]:
                    
                    interp_settings = param_settings["interp"]
                    
                    if interp_settings["type"] == "range":
                        
                        var_box["interp.button.range"].toggle()
                        var_box["interp.box.step"].setValue(
                                                interp_settings["delta"])
                    
                    elif interp_settings["type"] == "fixed":
                        
                        var_box["interp.button.fixed"].toggle()
                        
                        val_strs = [str(x) for x in interp_settings["values"]]
                        val_str = ", ".join(val_strs)
                        var_box["interp.edit.values"].setText(val_str)
                    
                    else:
                        
                        err_str = ("Unrecognised interpolation type "
                                   "'{}'").format(interp_settings["type"])
                        raise ValueError(err_str)

        ## RESULTS TAB
        
        results_open = (optimiser_status_str is not None and
                        self._shell.strategy is not None and
                        self._config == self._shell.strategy._config)
        
        if not results_open:
            
            self.tabWidget.setTabEnabled(2, False)
            self.tabWidget.setTabEnabled(3, False)
            self._results_df = None
        
        else:
            
            self.tabWidget.setTabEnabled(2, True)
            self.tabWidget.setTabEnabled(3, True)
            
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
                
                
                df = GUIAdvancedPosition.get_results_table(self._config)
                
                new_columns = []
                
                for column in df.columns:
                    
                    for key in self._name_map.keys():
                        
                        if key in column:
                            
                            column = column.replace(key, self._name_map[key])
                            
                            if key in self._unit_map:
                                column += " ({})".format(self._unit_map[key])
                            
                            break
                    
                    new_columns.append(column)
                
                df.columns = new_columns
                
                self._results_df = df
                
                # Populate plot comboboxes
                new_columns.insert(0, "")
                self.xAxisVarBox.addItems(new_columns)
                self.yAxisVarBox.addItems(new_columns)
                self.colorAxisVarBox.addItems(new_columns)
                self.filterVarBox.addItems(new_columns)
            
            model = DataFrameModel(self._results_df)
            self.dataTableWidget.setViewModel(model)
        
        ## PLOTS TAB
        
        if self.plotWidget is None:
            plot_export_enabled = False
        else:
            plot_export_enabled = True
        
        self.plotExportButton.setEnabled(plot_export_enabled)
        
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
    
    @QtCore.pyqtSlot()
    def _set_plot(self, set_widget=True):
        
        x_axis_str = str(self.xAxisVarBox.currentText())
        y_axis_str = str(self.yAxisVarBox.currentText())
        color_axis_str = str(self.colorAxisVarBox.currentText())
        
        if not (x_axis_str and y_axis_str): return
        
        x_axis_data = self._results_df[x_axis_str]
        y_axis_data = self._results_df[y_axis_str]
        
        data_filter = np.array([True] * len(self._results_df))
        filter_str = str(self.filterVarBox.currentText())
        
        if filter_str:
            
            filter_data = self._results_df[filter_str]
            
            if self.filterVarMinBox.checkState() == QtCore.Qt.Checked:
                filter_val = float(self.filterVarMinSpinBox.value())
                data_filter = data_filter & (filter_data >= filter_val)
            
            if self.filterVarMaxBox.checkState() == QtCore.Qt.Checked:
                filter_val = float(self.filterVarMaxSpinBox.value())
                data_filter = data_filter & (filter_data <= filter_val)
        
        if not data_filter.all():
            x_axis_data = x_axis_data[data_filter]
            y_axis_data = y_axis_data[data_filter]
        
        color_axis_data = None
        cmap = None
        norm = None
        vmin = None
        vmax = None
        xmin = None
        xmax = None
        ymin = None
        ymax = None
        
        if self.xAxisMinBox.checkState() == QtCore.Qt.Checked:
            xmin = float(self.xAxisMinSpinBox.value())
        
        if self.xAxisMaxBox.checkState() == QtCore.Qt.Checked:
            xmax = float(self.xAxisMaxSpinBox.value())
        
        if self.yAxisMinBox.checkState() == QtCore.Qt.Checked:
            ymin = float(self.yAxisMinSpinBox.value())
        
        if self.yAxisMaxBox.checkState() == QtCore.Qt.Checked:
            ymax = float(self.yAxisMaxSpinBox.value())
        
        if self.colorAxisMinBox.checkState() == QtCore.Qt.Checked:
            vmin = float(self.colorAxisMinSpinBox.value())
        
        if self.colorAxisMaxBox.checkState() == QtCore.Qt.Checked:
            vmax = float(self.colorAxisMaxSpinBox.value())
        
        if color_axis_str:
            
            color_axis_data = self._results_df[color_axis_str]
            
            if not data_filter.all():
                color_axis_data = color_axis_data[data_filter]
            
            if color_axis_data.dtype == np.int64:
                
                # define the colormap
                cmap = plt.cm.jet
                
                if vmin is None:
                    color_axis_min = color_axis_data.min()
                else:
                    color_axis_min = int(vmin)
                
                if vmax is None:
                    color_axis_max = color_axis_data.max()
                else:
                    color_axis_max = int(vmax)
                
                # define the bins and normalize
                n_vals = color_axis_max - color_axis_min + 2
                
                bounds = np.linspace(color_axis_min,
                                     color_axis_max + 1,
                                     n_vals)
                
                norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        
        fig, ax = plt.subplots()
        
        im = ax.scatter(x_axis_data,
                        y_axis_data,
                        c=color_axis_data,
                        cmap=cmap,
                        norm=norm,
                        vmin=vmin,
                        vmax=vmax)
        
        ax.set_xlim([xmin, xmax])
        ax.set_ylim([ymin, ymax])
        
        ax.set(xlabel=x_axis_str,
               ylabel=y_axis_str)
        
        # Add a colorbar
        if color_axis_str:
            
            extend =  'neither'
            
            if vmin is not None and vmax is not None:
                extend = 'both'
            elif vmin is not None:
                extend = 'min'
            elif vmax is not None:
                extend = 'max'
            
            cb = fig.colorbar(im, ax=ax, extend=extend)
            cb.set_label(color_axis_str)
            
            if color_axis_data.dtype == np.int64:
            
                # Relabel to centre of intervals
                labels = np.arange(color_axis_min,
                                   color_axis_max + 1,
                                   1)
                loc = labels + .5
                cb.set_ticks(loc)
                cb.set_ticklabels(labels)
        
        fig.subplots_adjust(0.2, 0.2, 0.8, 0.8)
        
        if not set_widget: return
        
        self._clear_plot_widget()
        
        widget = MPLWidget(fig, self)
        widget.setMinimumSize(QtCore.QSize(0, 250))
        
        self.plotWidget = widget
        self.plotLayout.addWidget(widget)
        
        # Draw the widget
        widget.draw_idle()
        
        if len(plt.get_fignums()) > 3:
            
            num_strs = ["{}".format(x) for x in plt.get_fignums()]
            num_str = ", ".join(num_strs)
            err_msg = ("Too many matplotlib figures detected. "
                       "Numbers: {}").format(num_str)
            
            raise RuntimeError(err_msg)
        
        self._update_status()
        
        return
    
    def _clear_plot_widget(self):
        
        if self.plotWidget is None: return
        
        self.plotLayout.removeWidget(self.plotWidget)
        self.plotWidget.setParent(None)
        
        fignum = self.plotWidget.figure.number
        
        log_msg = "Closing figure {}".format(fignum)
        module_logger.debug(log_msg)
        
        sip.delete(self.plotWidget)
        plt.close(fignum)
        
        self.plotWidget = None
        
        return
    
    @QtCore.pyqtSlot()
    def _get_export_details(self):
        
        if self.plotWidget is None: return
        
        msg = "Save plot"
        extlist = ["{} (*.{})".format(v, k) for k, v in
                                           self._plot_ext_types.iteritems()]
        extStr = ";;".join(extlist)
        
        save_path = QtGui.QFileDialog.getSaveFileName(self,
                                                      msg,
                                                      HOME,
                                                      extStr)
        
        if not save_path: return
        
        if self.customSizeBox.checkState() == QtCore.Qt.Checked:
            size = (float(self.customWidthSpinBox.value()),
                    float(self.customHeightSpinBox.value()))
        else:
            size = get_current_figure_size()
        
        self._export_plot(save_path, size)
        
        return
    
    def _export_plot(self, file_path, size, dpi=220):
        
        if self.plotWidget is None: return
        
        self._set_plot(set_widget=False)
        fig_handle = plt.gcf()
        
        fig_handle.set_size_inches(*size)
        
        with plt.rc_context(rc={'font.size': 8,
                                'font.sans-serif': 'Verdana'}):
            
            fig_handle.savefig(str(file_path),
                               dpi=dpi,
                               bbox_inches='tight')
        
        plt.close(fig_handle)
        
        # Ensure DPI is saved
        try:
            im = Image.open(str(file_path))
            im.save(str(file_path), dpi=[dpi, dpi])
        except IOError:
            pass
        
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


def make_var_box(widget, parent, name, box_class):
    
    var_box_dict = {}
    
    var_box_dict["root"] = QtGui.QGroupBox(parent)
    var_box_dict["root"].setFlat(False)
    var_box_dict["root"].setCheckable(False)
    var_box_dict["root"].setObjectName(get_obj_name(name, "root"))
    
    var_box_dict["root.layout"] = QtGui.QVBoxLayout(var_box_dict["root"])
    var_box_dict["root.layout"].setObjectName(get_obj_name(name,
                                                           "root.layout"))
    
    var_box_dict["fixed.layout"] = QtGui.QHBoxLayout()
    var_box_dict["fixed.layout"].setObjectName(get_obj_name(name,
                                                             "fixed.layout"))
    
    var_box_dict["fixed.check"] = QtGui.QCheckBox(var_box_dict["root"])
    var_box_dict["fixed.check"].setObjectName(get_obj_name(name,
                                                           "fixed.check"))
    var_box_dict["fixed.layout"].addWidget(var_box_dict["fixed.check"])
    
    var_box_dict["fixed.box"] = box_class(var_box_dict["root"])
    
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                   QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(
            var_box_dict["fixed.box"].sizePolicy().hasHeightForWidth())
    
    var_box_dict["fixed.box"].setSizePolicy(sizePolicy)
    var_box_dict["fixed.box"].setMinimumSize(QtCore.QSize(75, 0))
    var_box_dict["fixed.box"].setObjectName(get_obj_name(name,
                                                         "fixed.box"))
    var_box_dict["fixed.layout"].addWidget(var_box_dict["fixed.box"])
    
    spacerItem6 = QtGui.QSpacerItem(40,
                                    20,
                                    QtGui.QSizePolicy.Expanding,
                                    QtGui.QSizePolicy.Minimum)
    var_box_dict["fixed.layout"].addItem(spacerItem6)
    
    var_box_dict["root.layout"].addLayout(var_box_dict["fixed.layout"])
    
    var_box_dict["range.group"] = QtGui.QGroupBox(var_box_dict["root"])
    var_box_dict["range.group"].setFlat(True)
    var_box_dict["range.group"].setObjectName(get_obj_name(name,
                                                           "range.group"))
    
    var_box_dict["range.layout"] = QtGui.QVBoxLayout(
                                                var_box_dict["range.group"])
    var_box_dict["range.layout"].setObjectName(get_obj_name(name,
                                                            "range.layout"))
    
    var_box_dict["range.grid"] = QtGui.QGridLayout()
    var_box_dict["range.grid"].setSpacing(10)
    var_box_dict["range.grid"].setObjectName(get_obj_name(name, "range.grid"))
    
    var_box_dict["range.label.type"] = QtGui.QLabel(
                                                var_box_dict["range.group"])
    
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                   QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(
            var_box_dict["range.label.type"].sizePolicy().hasHeightForWidth())
    
    var_box_dict["range.label.type"].setSizePolicy(sizePolicy)
    var_box_dict["range.label.type"].setLayoutDirection(QtCore.Qt.RightToLeft)
    var_box_dict["range.label.type"].setAlignment(QtCore.Qt.AlignRight |
                                                  QtCore.Qt.AlignTrailing |
                                                  QtCore.Qt.AlignVCenter)
    var_box_dict["range.label.type"].setObjectName(
                                    get_obj_name(name, "range.label.type"))
    
    var_box_dict["range.grid"].addWidget(var_box_dict["range.label.type"],
                                         0,
                                         0,
                                         1,
                                         1)
    
    var_box_dict["range.box.type"] = QtGui.QComboBox(
                                                var_box_dict["range.group"])
    
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                   QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(
            var_box_dict["range.box.type"].sizePolicy().hasHeightForWidth())
    
    var_box_dict["range.box.type"].setSizePolicy(sizePolicy)
    var_box_dict["range.box.type"].setObjectName(
                                        get_obj_name(name, "range.box.type"))
    
    var_box_dict["range.grid"].addWidget(var_box_dict["range.box.type"],
                                         0,
                                         1,
                                         1,
                                         1)
    
    var_box_dict["range.label.var"] = QtGui.QLabel(var_box_dict["range.group"])
    
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                   QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(
            var_box_dict["range.label.var"].sizePolicy().hasHeightForWidth())
    
    var_box_dict["range.label.var"].setSizePolicy(sizePolicy)
    var_box_dict["range.label.var"].setLayoutDirection(QtCore.Qt.RightToLeft)
    var_box_dict["range.label.var"].setAlignment(QtCore.Qt.AlignRight |
                                                 QtCore.Qt.AlignTrailing |
                                                 QtCore.Qt.AlignVCenter)
    var_box_dict["range.label.var"].setObjectName(
                                        get_obj_name(name, "range.label.var"))
    
    var_box_dict["range.grid"].addWidget(var_box_dict["range.label.var"],
                                         0,
                                         2,
                                         1,
                                         1)
    
    var_box_dict["range.box.var"] = QtGui.QComboBox(
                                                var_box_dict["range.group"])
    
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(
            var_box_dict["range.box.var"].sizePolicy().hasHeightForWidth())
    
    var_box_dict["range.box.var"].setSizePolicy(sizePolicy)
    var_box_dict["range.box.var"].setObjectName(
                                        get_obj_name(name, "range.box.var"))
    
    var_box_dict["range.grid"].addWidget(var_box_dict["range.box.var"], 
                                         0,
                                         3,
                                         1,
                                         1)
    
    var_box_dict["range.label.min"] = QtGui.QLabel(var_box_dict["range.group"])
    
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                   QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(
            var_box_dict["range.label.min"].sizePolicy().hasHeightForWidth())
    
    var_box_dict["range.label.min"].setSizePolicy(sizePolicy)
    var_box_dict["range.label.min"].setLayoutDirection(QtCore.Qt.RightToLeft)
    var_box_dict["range.label.min"].setAlignment(QtCore.Qt.AlignRight |
                                                 QtCore.Qt.AlignTrailing |
                                                 QtCore.Qt.AlignVCenter)
    var_box_dict["range.label.min"].setObjectName(
                                        get_obj_name(name, "range.label.min"))
    
    var_box_dict["range.grid"].addWidget(var_box_dict["range.label.min"],
                                         1,
                                         0,
                                         1,
                                         1)
    
    var_box_dict["range.box.min"] = box_class(var_box_dict["range.group"])
    
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                   QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(
            var_box_dict["range.box.min"].sizePolicy().hasHeightForWidth())
    
    var_box_dict["range.box.min"].setSizePolicy(sizePolicy)
    var_box_dict["range.box.min"].setMinimumSize(QtCore.QSize(75, 0))
    var_box_dict["range.box.min"].setObjectName(
                                        get_obj_name(name, "range.box.min"))
    
    var_box_dict["range.grid"].addWidget(var_box_dict["range.box.min"],
                                         1,
                                         1,
                                         1,
                                         1)
    
    var_box_dict["range.label.max"] = QtGui.QLabel(var_box_dict["range.group"])
    
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                   QtGui.QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(
            var_box_dict["range.label.max"].sizePolicy().hasHeightForWidth())
    
    var_box_dict["range.label.max"].setSizePolicy(sizePolicy)
    var_box_dict["range.label.max"].setLayoutDirection(QtCore.Qt.RightToLeft)
    var_box_dict["range.label.max"].setAlignment(QtCore.Qt.AlignRight |
                                                 QtCore.Qt.AlignTrailing |
                                                 QtCore.Qt.AlignVCenter)
    var_box_dict["range.label.max"].setObjectName(
                                        get_obj_name(name, "range.label.max"))
    
    var_box_dict["range.grid"].addWidget(var_box_dict["range.label.max"],
                                         1,
                                         2,
                                         1,
                                         1)
    
    var_box_dict["range.box.max"] = box_class(var_box_dict["range.group"])
    
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                   QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(
            var_box_dict["range.box.max"].sizePolicy().hasHeightForWidth())
    
    var_box_dict["range.box.max"].setSizePolicy(sizePolicy)
    var_box_dict["range.box.max"].setMinimumSize(QtCore.QSize(75, 0))
    var_box_dict["range.box.max"].setObjectName(
                                        get_obj_name(name, "range.box.max"))
    
    var_box_dict["range.grid"].addWidget(var_box_dict["range.box.max"],
                                         1,
                                         3,
                                         1,
                                         1)
    
    var_box_dict["range.layout"].addLayout(var_box_dict["range.grid"])
    var_box_dict["root.layout"].addWidget(var_box_dict["range.group"])
    
    var_box_dict["interp.group"] = QtGui.QGroupBox(var_box_dict["root"])
    var_box_dict["interp.group"].setFlat(True)
    var_box_dict["interp.group"].setObjectName(
                                        get_obj_name(name, "interp.group"))
    
    var_box_dict["interp.layout"] = QtGui.QHBoxLayout(
                                                var_box_dict["interp.group"])
    var_box_dict["interp.layout"].setObjectName(
                                        get_obj_name(name, "interp.layout"))
    
    var_box_dict["interp.grid"] = QtGui.QGridLayout()
    var_box_dict["interp.grid"].setSpacing(10)
    var_box_dict["interp.grid"].setObjectName(
                                            get_obj_name(name, "interp.grid"))
    
    var_box_dict["interp.button.range"] = QtGui.QRadioButton(
                                                var_box_dict["interp.group"])
    var_box_dict["interp.button.range"].setObjectName(
                                    get_obj_name(name, "interp.button.range"))
    
    var_box_dict["interp.grid"].addWidget(var_box_dict["interp.button.range"],
                                          0,
                                          0,
                                          1,
                                          1)
    
    var_box_dict["interp.label.step"] = QtGui.QLabel(
                                                var_box_dict["interp.group"])
    var_box_dict["interp.label.step"].setLayoutDirection(QtCore.Qt.RightToLeft)
    var_box_dict["interp.label.step"].setAlignment(QtCore.Qt.AlignRight |
                                                   QtCore.Qt.AlignTrailing|
                                                   QtCore.Qt.AlignVCenter)
    var_box_dict["interp.label.step"].setObjectName(
                                    get_obj_name(name, "interp.label.step"))
    
    var_box_dict["interp.grid"].addWidget(var_box_dict["interp.label.step"],
                                          0,
                                          1,
                                          1,
                                          1)
    
    var_box_dict["interp.box.step"] = box_class(var_box_dict["interp.group"])
    var_box_dict["interp.box.step"].setMaximum(sys.maxint)
    
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                   QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(
            var_box_dict["interp.box.step"].sizePolicy().hasHeightForWidth())
    
    var_box_dict["interp.box.step"].setSizePolicy(sizePolicy)
    var_box_dict["interp.box.step"].setMinimumSize(QtCore.QSize(75, 0))
    var_box_dict["interp.box.step"].setObjectName(
                                    get_obj_name(name, "interp.box.step"))
    
    var_box_dict["interp.grid"].addWidget(var_box_dict["interp.box.step"],
                                          0,
                                          2,
                                          1,
                                          1)
    
    var_box_dict["interp.button.fixed"] = QtGui.QRadioButton(
                                                var_box_dict["interp.group"])
    var_box_dict["interp.button.fixed"].setObjectName(
                                    get_obj_name(name, "interp.button.fixed"))
    
    var_box_dict["interp.grid"].addWidget(var_box_dict["interp.button.fixed"],
                                          1,
                                          0,
                                          1,
                                          1)
    
    var_box_dict["interp.label.values"] = QtGui.QLabel(
                                                var_box_dict["interp.group"])
    var_box_dict["interp.label.values"].setAlignment(QtCore.Qt.AlignRight |
                                                     QtCore.Qt.AlignTrailing |
                                                     QtCore.Qt.AlignVCenter)
    var_box_dict["interp.label.values"].setObjectName(
                                    get_obj_name(name, "interp.label.values"))
    
    var_box_dict["interp.grid"].addWidget(var_box_dict["interp.label.values"],
                                          1,
                                          1,
                                          1,
                                          1)
    
    var_box_dict["interp.edit.values"] = QtGui.QLineEdit(
                                                var_box_dict["interp.group"])
    var_box_dict["interp.edit.values"].setObjectName(
                                    get_obj_name(name, "interp.edit.values"))
    
    var_box_dict["interp.grid"].addWidget(var_box_dict["interp.edit.values"],
                                          1,
                                          2,
                                          1,
                                          1)
    
    var_box_dict["interp.label.commas"] = QtGui.QLabel(
                                                var_box_dict["interp.group"])
    var_box_dict["interp.label.commas"].setObjectName(
                                    get_obj_name(name, "interp.label.commas"))
    
    var_box_dict["interp.grid"].addWidget(var_box_dict["interp.label.commas"],
                                          1,
                                          3,
                                          1,
                                          1)
    
    var_box_dict["interp.layout"].addLayout(var_box_dict["interp.grid"])
    var_box_dict["root.layout"].addWidget(var_box_dict["interp.group"])
    
    var_box_dict["button.group"] = QtGui.QButtonGroup(widget)
    var_box_dict["button.group"].setObjectName(_fromUtf8("buttonGroup"))
    var_box_dict["button.group"].addButton(var_box_dict["interp.button.range"])
    var_box_dict["button.group"].addButton(var_box_dict["interp.button.fixed"])
    
    widget_name = str(widget.objectName())

    var_box_dict["root"].setTitle(get_translation(widget_name,
                                                  name))
    var_box_dict["fixed.check"].setText(get_translation(widget_name,
                                                        "Fixed Value:"))
    var_box_dict["range.group"].setTitle(get_translation(widget_name,
                                                         "Range"))
    var_box_dict["range.label.type"].setText(get_translation(widget_name,
                                                             "Type:"))
    var_box_dict["range.label.var"].setText(get_translation(widget_name,
                                                            "Variable:"))
    var_box_dict["range.label.min"].setText(get_translation(widget_name,
                                                            "Min:"))
    var_box_dict["range.label.max"].setText(get_translation(widget_name,
                                                            "Max:"))
    var_box_dict["interp.group"].setTitle(get_translation(widget_name,
                                                          "Interpolation"))
    var_box_dict["interp.button.range"].setText(get_translation(widget_name,
                                                                "Range"))
    var_box_dict["interp.label.step"].setText(get_translation(widget_name,
                                                                "Step:"))
    var_box_dict["interp.button.fixed"].setText(get_translation(widget_name,
                                                                "Fixed"))
    var_box_dict["interp.label.values"].setText(get_translation(widget_name,
                                                                "Values:"))
    var_box_dict["interp.label.commas"].setText(get_translation(
                                                    widget_name,
                                                    "(seperated by commas)"))
    
    return var_box_dict


def get_obj_name(name, key):
    
    ext_key = "{}.{}".format(name, key)
    
    return _fromUtf8(ext_key)


def get_translation(widget_name, text):
    
    return _translate(widget_name, text, None)



def _init_sci_spin_box(parent, name):
    
    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    
    sciSpinBox = ScientificDoubleSpinBox(parent)
    sciSpinBox.setSizePolicy(sizePolicy)
    sciSpinBox.setMinimumSize(QtCore.QSize(0, 0))
    sciSpinBox.setKeyboardTracking(False)
    sciSpinBox.setObjectName(_fromUtf8(name))
    
    return sciSpinBox
