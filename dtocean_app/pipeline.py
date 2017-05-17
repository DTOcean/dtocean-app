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


import os
import sys
import runpy
from collections import OrderedDict

import pandas as pd
from PyQt4 import QtGui, QtCore

from dtocean_core.pipeline import Tree

from .widgets.docks import PipeLineDock
from .widgets.display import MPLWidget
from .widgets.dialogs import TestDataPicker
from .widgets.input import CancelWidget
from .utils.icons import (make_redicon_pixmap,
                          make_greenicon_pixmap,
                          make_blueicon_pixmap,
                          make_buttoncancel_pixmap)

class ThreadReadTest(QtCore.QThread):
    
    """QThread for reading test data"""
    
    error_detected =  QtCore.pyqtSignal(object, object, object)
    
    def __init__(self, item, shell, path, overwrite):
        
        super(ThreadReadTest, self).__init__()
        self.item = item
        self.shell = shell
        self.path = path
        self.overwrite = overwrite
        
        return
    
    def run(self):
        
        try:
        
            self.item._read_test_data(self.shell,
                                      self.path,
                                      self.overwrite)
        
        except: 
            
            etype, evalue, etraceback = sys.exc_info()
            self.error_detected.emit(etype, evalue, etraceback)

        return


class PipeLine(PipeLineDock):
    
    error_detected =  QtCore.pyqtSignal(object, object, object)
    
    def __init__(self, parent):

        super(PipeLine, self).__init__(parent)
        self._tree = Tree()
        
        # Root branches
        self._branch_map = None
        self._items = []
        
        # Test data picker
        self._test_data_picker = TestDataPicker(self)
        self._test_data_picker.setModal(True)
        self._active_thread = None
                
        self._init_title()
        
        return
        
    def _init_title(self):
        
        self.setWindowTitle("Pipeline")
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.headerItem().setText(0, "Waiting...")

        return
        
    def _set_branch_map(self, branch_map):
        
        self._branch_map = branch_map
        
        return
        
    def _set_title(self, title):
        
        self.treeWidget.headerItem().setText(0, title)
        
        return
        
    def _draw(self, shell):
        
        self._clear()
        
        for branch_dict in self._branch_map:
            
            HubCls = branch_dict["hub"]
            args = []
            if "args" in branch_dict: args.extend(branch_dict["args"])
            
            new_item = HubCls(self.treeWidget,
                              branch_dict["name"],
                              *args)
            new_item._activate(shell)
            self._items.append(new_item)
            
        return
        
    def _expand(self, shell):
        
        for item in self._items:
            item._expand(shell)
        
        return
    
    def _refresh(self, shell, expand=True):
        
        self._draw(shell)
        if expand: self._expand(shell)
        
        return        
        
    def _clear(self):
        
        root = self.treeWidget.invisibleRootItem()
        
        for widget in self._items:
            
            widget._clear()
            
            if not isinstance(widget, HiddenHub):
                root.removeChild(widget)
            
        self._items = []

        return
        
    def _find_item(self, item_title, item_class=None, root_item=None):
        
        if root_item is None: root_item = self

        for item in root_item._items:
            
            if item._title == item_title:
                if item_class is None or isinstance(item, item_class):
                    return item
                    
            result = self._find_item(item_title, item_class, item)
            
            if result is not None: return result

        return None
        
    def _make_menus(self, shell, position):
                
        item = self.treeWidget.currentItem()

        if isinstance(item, InputBranchItem):
            
            # Set the widget action
            self._test_data_picker.buttonBox.button(
                         QtGui.QDialogButtonBox.Ok).clicked.disconnect()
            self._test_data_picker.buttonBox.button(
                         QtGui.QDialogButtonBox.Ok).clicked.connect(
                             lambda: self._read_test_data(shell, item))
            self._test_data_picker.buttonBox.button(
                         QtGui.QDialogButtonBox.Ok).clicked.connect(
                             self._test_data_picker.close)
            
            # Build module and theme context menu
            if item._hub_title in ["Modules", "Assessment"]:
                
                menu = QtGui.QMenu()
                
                if item._hub_title == "Modules":
                    menu.addAction('Inspect', lambda: item._inspect(shell))
                    menu.addAction('Reset', lambda: item._reset(shell))
                    
                menu.addAction('Load test data...', 
                               self._test_data_picker.show)            
                menu.exec_(self.treeWidget.mapToGlobal(position))
            
        elif isinstance(item, OutputBranchItem):
            
            # Build module context menu
            if item._hub_title == "Modules":
                
                menu = QtGui.QMenu()
                menu.addAction('Inspect', lambda: item._inspect(shell))
                menu.exec_(self.treeWidget.mapToGlobal(position))
     
        return
        
    def _set_top_item(self):
        
        self.treeWidget.itemClicked.emit(self.treeWidget.topLevelItem(0), -1)
        
        return
    
    def _read_auto(self, shell):
        
        self._tree.read_auto(shell.core,
                             shell.project)
                             
        return
    
    @QtCore.pyqtSlot(object, object)
    def _read_test_data(self, shell, item):
        
        self._active_thread = ThreadReadTest(
                             item,
                             shell,
                             str(self._test_data_picker.pathLineEdit.text()),
                             self._test_data_picker.overwriteBox.isChecked())
        self._active_thread.start()
        self._active_thread.error_detected.connect(self._emit_error)
        self._active_thread.finished.connect(self._clear_active_thread)
        
        return
        
    @QtCore.pyqtSlot()
    def _clear_active_thread(self):
        
        self._active_thread = None 
        
        return
        
    @QtCore.pyqtSlot(object, object, object)
    def _emit_error(self, etype, evalue, etraceback):
        
        self.error_detected.emit(etype, evalue, etraceback)
        
        return


class BaseItem(QtGui.QTreeWidgetItem):
    
    def __init__(self, parent,
                       title):

        super(BaseItem, self).__init__(parent)
        self._title = title
        self._id = None
        self._status = None
        self._items = []

        self._init_ui(title)

        return
        
    def _init_ui(self, title):

        self.setText(0, title)

        return
        
    def _activate(self, shell):
            
        return
        
    def _expand(self, shell):
        
        for item in self._items:
            item._expand(shell)
            
        self.setExpanded(True)
        
        return
        
    def _clear(self):
                
        for widget in self._items:
            
            widget._clear() 
            self.removeChild(widget)
            
        self._items = []

        return
        
    def _get_data_widget(self, shell):
        
        return None
        
    def _get_plot_widget(self, shell, plot_name):
        
        return None


class SectionItem(BaseItem):
    
    def _init_ui(self, title):
        
        # Formatting
        section_wrapper = "------   {}   ------"
        section_title = section_wrapper.format(title)
        
        self.setText(0, section_title)
        self.setTextAlignment(0, QtCore.Qt.AlignCenter)
        bbrush = QtGui.QBrush(QtGui.QColor("lightgrey"))
        self.setBackground(0, bbrush)
        
        return
    
    def _expand(self, shell):
        
        return

        
class HubRoot(object):
    
    def __init__(self, title,
                       hub_name,
                       branch_cls,
                       active=True,
                       branch_order=None):
        
        self._title = title
        self._tree = Tree()
        self._hub_name = hub_name
        self._BranchCls = branch_cls
        self._active = active
        self._branch_order = branch_order
        self._items = []
                
        return
        
    def _activate(self, parent, shell, hub_branches):
                                                                                                                  
        if self._branch_order is None:
            branch_order = hub_branches
        else:
            branch_order = [branch for branch in self._branch_order
                                                    if branch in hub_branches]
                                                         
        for branch_name in branch_order:
            
            branch = self._tree.get_branch(shell.core,
                                           shell.project,
                                           branch_name)

            new_item = self._BranchCls(parent,
                                       branch,
                                       self._title,
                                       branch_name)
            
            if self._active:
                new_item._activate(shell)
            else:
                new_item.setDisabled(True)
            
            self._items.append(new_item)
            
        return
        
        
class HubItem(BaseItem, HubRoot):
    
    def __init__(self, parent,
                       title,
                       hub_name,
                       branch_cls,
                       active=True,
                       branch_order=None):
                           
        BaseItem.__init__(self, parent,
                                title)
        HubRoot.__init__(self, title,
                               hub_name,
                               branch_cls,
                               active,
                               branch_order)       
        return
        
    def _activate(self, shell):
        
        hub_branches = self._tree.get_available_branches(shell.core,
                                                         shell.project,
                                                         [self._hub_name])
                                                         
#        if not hub_branches:
#            self.setHidden(True)
#            return
        
        HubRoot._activate(self, self, shell, hub_branches)
        
        return
        
        
class HiddenHub(HubRoot):
    
    def __init__(self, parent,
                       title,
                       hub_name,
                       branch_cls,
                       active=True,
                       branch_order=None):
        
        self._parent = parent
        super(HiddenHub, self).__init__(title,
                                        hub_name,
                                        branch_cls,
                                        active,
                                        branch_order)
        
        return
        
    def _activate(self, shell):
        
        hub_branches = self._tree.get_available_branches(shell.core,
                                                         shell.project,
                                                         [self._hub_name])
                                                         
        if not hub_branches: return
        
        super(HiddenHub, self)._activate(self._parent, shell, hub_branches)
        
        return
        
    def _expand(self, shell):
                        
        for item in self._items:
            item._expand(shell)  
            
        return
        
    def _clear(self):
                
        for widget in self._items:
            
            widget._clear() 
            
        self._items = []

        return
        
        
class InputBranchItem(BaseItem):
    
    def __init__(self, parent,
                       branch,
                       hub_title,
                       title,
                       ignore_str="hidden"):
                           
        super(InputBranchItem, self).__init__(parent, title)
        self._branch = branch
        self._hub_title = hub_title
        self._ignore_str = ignore_str
        
        return
        
    def _activate(self, shell, sort=True):
        
        # Update status on variable updated events
        shell.update_pipeline.connect(self._update_status)
        
        input_status = self._branch.get_input_status(shell.core,
                                                     shell.project)
        if sort: 
            
            input_declaration = self._branch.get_inputs(shell.core,
                                                        shell.project)
            
            sorted_input_status = OrderedDict()
            
            for variable_id in input_declaration:
                sorted_input_status[variable_id] = input_status[variable_id]

            input_status = sorted_input_status
        
        for variable_id, status in input_status.iteritems():
            
            if self._ignore_str in variable_id: continue
            
            new_var = self._branch.get_input_variable(shell.core,
                                                      shell.project,
                                                      variable_id)
            metadata = new_var.get_metadata(shell.core)

            new_item = InputVarItem(self,
                                    new_var,
                                    status,
                                    metadata.title)

            self._items.append(new_item)
            
        return
                
    def _expand(self, shell):
            
        input_status = self._branch.get_input_status(shell.core,
                                                     shell.project)
                                                     
        if not set(input_status.values()) == set(["unavailable"]):
            self.setExpanded(True)
        
        return

    @QtCore.pyqtSlot(object)
    def _update_status(self, shell):
        
        input_status = self._branch.get_input_status(shell.core,
                                                     shell.project)
        
        for item in self._items:
            
            status = input_status[item._variable._id]
            item._update_status(status)
            
        return
        
    def _get_required_address(self, shell):
                                      
        status = self._branch.get_input_status(shell.core,
                                               shell.project)

        required = [k for (k,v) in status.items() if v == "required"]
        required = set(required)
        
        if not required: return None

        # Locate the items providing the required variables and pick up the
        # names:
        item_names = []

        for item in self._items:
            if item._variable._id in required:
                item_names.append(item._title)
                
        section_names = [self._hub_title]*len(item_names)
        branch_names = [self._title]*len(item_names)

        address_dict = {"Section": section_names,
                        "Branch" : branch_names,
                        "Item"   : item_names}

        address_df = pd.DataFrame(address_dict)

        return address_df

    @QtCore.pyqtSlot(object, str, bool)        
    def _read_test_data(self, shell, test_data_path, overwrite=True):
        
        test_data_meta = runpy.run_path(test_data_path, run_name="__main__")
        data_path = test_data_meta["pkl_path"]
        
        self._branch.read_test_data(shell.core,
                                    shell.project,
                                    data_path,
                                    overwrite)
                                    
        os.remove(data_path)
        
        return

    @QtCore.pyqtSlot(object)        
    def _inspect(self, shell):

        self._branch.inspect(shell.core,
                             shell.project)
        
        return

    @QtCore.pyqtSlot(object)        
    def _reset(self, shell):

        self._branch.reset(shell.core,
                           shell.project)
        
        return


class OutputBranchItem(BaseItem):
    
    def __init__(self, parent,
                       branch,
                       hub_title,
                       title,
                       ignore_str="hidden"):
                           
        super(OutputBranchItem, self).__init__(parent, title)
        self._branch = branch
        self._hub_title = hub_title
        self._ignore_str = ignore_str
        
        return
        
    def _activate(self, shell, sort=True):
        
        # Update status on variable updated events
        shell.update_pipeline.connect(self._update_status)
        
        output_status = self._branch.get_output_status(shell.core,
                                                       shell.project)
        
        if sort: 
            
            output_declaration = self._branch.get_outputs(shell.core,
                                                          shell.project)
            
            sorted_output_status = OrderedDict()
            
            for variable_id in output_declaration:
                sorted_output_status[variable_id] = output_status[variable_id]

            output_status = sorted_output_status
        
        for variable_id, status in output_status.iteritems():
            
            if self._ignore_str in variable_id: continue
            
            new_var = self._branch.get_output_variable(shell.core,
                                                       shell.project,
                                                       variable_id)
            metadata = new_var.get_metadata(shell.core)

            new_item = OutputVarItem(self,
                                     new_var,
                                     status,
                                     metadata.title)

            self._items.append(new_item)
            
        return
        
    def _expand(self, shell):
            
        output_status = self._branch.get_output_status(shell.core,
                                                       shell.project)
                                                     
        if not set(output_status.values()) == set(["unavailable"]):
            self.setExpanded(True)
        
        return
            
    def _update_status(self, shell):

        output_status = self._branch.get_output_status(shell.core,
                                                       shell.project)
        for item in self._items:
            
            status = output_status[item._variable._id]
            item._update_status(status)
            
        return
        
    @QtCore.pyqtSlot(object)        
    def _inspect(self, shell):

        self._branch.inspect(shell.core,
                             shell.project)
        
        return


class VarItem(BaseItem):
        
    def __init__(self, parent,
                       variable,
                       status,
                       title):
                           
        super(VarItem, self).__init__(parent, title)
        self._variable = variable
        self._id = variable._id
        
        self._update_status(status)
        
        return
        
    def _expand(self, shell):
        
        return
        
    def _set_icon_red(self):

        self._icon = QtGui.QIcon()
        self._icon.addPixmap(make_redicon_pixmap(),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.setIcon(0, self._icon)

        return

    def _set_icon_green(self):

        self._icon = QtGui.QIcon()
        self._icon.addPixmap(make_greenicon_pixmap(),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.setIcon(0, self._icon)

        return

    def _set_icon_blue(self):

        self._icon = QtGui.QIcon()
        self._icon.addPixmap(make_blueicon_pixmap(),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.setIcon(0, self._icon)

        return

    def _set_icon_cancel(self):

        self._icon = QtGui.QIcon()
        self._icon.addPixmap(make_buttoncancel_pixmap(),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.setIcon(0, self._icon)

        return
        
    def _update_status(self, status):

        self._status = status

        if status == "satisfied":

            self.setHidden(False)
            self.setDisabled(False)
            self._set_icon_green()

        elif status == "required":

            self.setHidden(False)
            self.setDisabled(False)
            self._set_icon_red()

        elif status == "optional":

            self.setHidden(False)
            self.setDisabled(False)
            self._set_icon_blue()

        return
        
    def _get_data_widget(self, shell, interface):
        
        if interface is None: return None
        
        if not shell.core.can_load_interface(shell.project, interface):
            
            errStr = ("The inputs to interface {} are not "
                      "satisfied.").format(interface.get_name())
            raise ValueError(errStr)
        
        interface = shell.core.load_interface(shell.project, interface)
        interface = shell.core.connect_interface(shell.project, interface)
        widget = interface.get_data(self._variable._id)

        return widget
                    
    def _get_plot_widget(self, shell, plot_name=None):
                
        interface = self._variable._get_receiving_interface(shell.core, 
                                                            shell.project,
                                                            "PlotInterface",
                                                            "AutoPlot",
                                                            plot_name)

        if (interface is None or 
            not shell.core.has_data(shell.project,
                                    self._variable._id)): return None
        
        self._variable._write_interface(shell.core, 
                                        shell.project,
                                        interface)
        
        if interface.fig_handle is None: return None
        
        widget = MPLWidget(interface.fig_handle, shell.core._input_parent)
        
        return widget


class InputVarItem(VarItem):
    
    def _update_status(self, status):

        if "unavailable" in status:

            self.setHidden(False)
            self.setDisabled(True)
            self._set_icon_cancel()
            
        elif "overwritten" in status:

            self.setHidden(True)
        
        super(InputVarItem, self)._update_status(status)

        return
        
    def _get_data_widget(self, shell):
        
        interface = self._variable._find_providing_interface(
                                                   shell.core,
                                                   "InputWidgetInterface",
                                                   allow_missing=True)
                                                   
        if interface is None:
        
            interface = self._variable._find_providing_interface(
                                                       shell.core,
                                                       "AutoInput",
                                                       allow_missing=True)
                                                   
        widget = super(InputVarItem, self)._get_data_widget(shell, interface)
        
        # Provide the cancel widget if no other can be found
        if widget is None: widget = CancelWidget()

        return widget
    

class OutputVarItem(VarItem):
    
    def _update_status(self, status):

        if "unavailable" in status or "overwritten" in status:
            self.setHidden(True)
        
        super(OutputVarItem, self)._update_status(status)

        return
        
    def _get_data_widget(self, shell):
        
        interface = self._variable._find_providing_interface(
                                                   shell.core,
                                                   "OutputWidgetInterface",
                                                   allow_missing=True)
                                                   
        if interface is None:
        
            interface = self._variable._find_providing_interface(
                                                       shell.core,
                                                       "AutoOutput",
                                                       allow_missing=True)
                                                   
        widget = super(OutputVarItem, self)._get_data_widget(shell, interface)

        return widget

