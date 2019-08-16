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

import multiprocessing

from PyQt4 import QtCore, QtGui

from dtocean_core.strategies.position import AdvancedPosition
from dtocean_core.strategies.position_optimiser import (dump_config,
                                                        load_config_template)

from . import GUIStrategy, StrategyWidget, PyQtABCMeta
from ..utils.display import is_high_dpi

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
        
        self._init_config()
        
        return
    
    def _init_config(self):
        
        config = load_config_template()
        self.configure(**config)
        
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
        
        widget = AdvancedPositionWidget(parent, self._config)
        
        return widget


class AdvancedPositionWidget(QtGui.QWidget,
                             Ui_AdvancedPositionWidget,
                             StrategyWidget):
    
    __metaclass__ = PyQtABCMeta
    
    config_set = QtCore.pyqtSignal()
    config_null = QtCore.pyqtSignal()
    
    def __init__(self, parent, config):
        
        QtGui.QWidget.__init__(self, parent)
        Ui_AdvancedPositionWidget.__init__(self)
        StrategyWidget.__init__(self)
        
        self._config = self._init_config(config)
        self._max_threads = multiprocessing.cpu_count()
        self._init_ui()
        
        return
    
    def _init_config(cls, config):
        
        config["threads_auto"] = False
        
        return config
    
    
    def _init_ui(self):
        
        self.setupUi(self)
        
        self.nThreadSpinBox.setMaximum(self._max_threads)
        self.set_manual_thread_message()
        
        self.importButton.clicked.connect(self._import_config)
        self.exportButton.clicked.connect(self._export_config)
        
        self.workdirLineEdit.returnPressed.connect(self._update_worker_dir)
        self.workdirToolButton.clicked.connect(self._select_worker_dir)
        
        self.nThreadSpinBox.valueChanged.connect(self._update_n_threads)
        
        self._update_status()
        
        
        return
    
    def set_manual_thread_message(self):
        
        thread_msg = "(maximum of {} threads available)".format(
                                                        self._max_threads)
        self.threadInfoLabel.setText(thread_msg)
        
        return
    
    def _update_status(self):
        
        (status_str,
         status_code) = GUIAdvancedPosition.get_config_status(self._config)
        
        if status_code == 0:
            str_color = "#aa0000"
        elif status_code == 1:
            str_color = "#00aa00"
        
        status_str_rich = ('<html><head/><body><p><span '
                           'style=" font-size:11pt; color:{};">'
                           '{}</span></p></body></html>').format(str_color,
                                                                 status_str)
        
        self.statusLabel.setText(status_str_rich)
        
        if status_code > 0:
            self.config_set.emit()
        else:
            self.config_null.emit()
        
        if self._config["worker_dir"] is not None:
            self.workdirLineEdit.setText(self._config["worker_dir"])
        
        if self._config["n_threads"] is not None:
            self.nThreadSpinBox.setValue(self._config["n_threads"])
        
        if self._config["threads_auto"]:
            
            if not self.autoThreadBox.isChecked():
                
                self.autoThreadBox.toggle()
                self.threadInfoLabel.setText("Auto mode")
        
        else:
            
            if self.autoThreadBox.isChecked():
                
                self.autoThreadBox.toggle()
                self.set_manual_thread_message()
        
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
        
        self._update_status()
        
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
        
        config = load_config_template()
        config.update(self._config)
        dump_config(config, file_path)
        
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
        
        print self._config["n_threads"]
        
        self._update_status()
        
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
