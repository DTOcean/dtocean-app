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

"""
Created on Thu Apr 23 12:51:14 2015

.. moduleauthor:: Mathew Topper <mathew.topper@dataonlygreater.com>
"""


import os
import runpy
from collections import OrderedDict

import pandas as pd
import matplotlib.pyplot as plt
from PyQt4 import QtGui, QtCore
from  PIL import Image

from dtocean_core.pipeline import Tree, _get_connector

from .widgets.docks import PipeLineDock
from .widgets.display import MPLWidget
from .widgets.dialogs import TestDataPicker
from .widgets.input import CancelWidget
from .utils.icons import (make_redicon_pixmap,
                          make_greenicon_pixmap,
                          make_blueicon_pixmap,
                          make_buttoncancel_pixmap)


class PipelineFilterProxyModel(QtGui.QSortFilterProxyModel):
    ''' Class to override the following behaviour:
            If a parent item doesn't match the filter,
            none of its children will be shown.
 
        This Model matches items which are descendants
        or ascendants of matching items.
        
    Source:
        https://gaganpreet.in/blog/2013/07/04/
        qtreeview-and-custom-filter-models/
    '''
 
    def filterAcceptsRow(self, row_num, source_parent):
 
        # Check if the current row matches
        if self.filter_accepts_row_itself(row_num, source_parent):
            return True

        # Finally, check if any of the children match
        return self.has_accepted_children(row_num, source_parent)
 
    def filter_accepts_row_itself(self, row_num, parent):
        
        model = self.sourceModel()
        source_index = model.index(row_num, 0, parent)
        
        source_data = model.data(source_index)
        source_data_str = source_data.toString()
        
        source_user_data = model.data(source_index, QtCore.Qt.UserRole)
        source_user_data_str = source_user_data.toString()
        
        # If the row is a section title then allow
        if "------" in source_data_str: return True
                
        # If the row address ends in "-" then disallow
        if source_user_data_str[-1] == "-":
            return False
        
        return super(PipelineFilterProxyModel, self).filterAcceptsRow(row_num,
                                                                      parent)

    def has_accepted_children(self, row_num, parent):
        ''' Starting from the current node as root, traverse all
            the descendants and test if any of the children match
        '''
        model = self.sourceModel()
        source_index = model.index(row_num, 0, parent)
 
        children_count =  model.rowCount(source_index)
        for i in xrange(children_count):
            if self.filterAcceptsRow(i, source_index):
                return True
        return False


class PipeLine(PipeLineDock):
    
    error_detected =  QtCore.pyqtSignal(object, object, object)
    
    def __init__(self, parent):

        super(PipeLine, self).__init__(parent)
        self._tree = Tree()
        self._model = None
        self._proxy = None
        
        # Root branches
        self._branch_map = None
        self._controls = []
        
        # Test data picker
        self._test_data_picker = TestDataPicker(self)
        self._test_data_picker.setModal(True)
        
        self._init_model()
        self._init_title()
        
        return
    
    def _init_model(self):
        
        self._model = QtGui.QStandardItemModel()
        self._model.setColumnCount(1)
        self._proxy = PipelineFilterProxyModel()
        self._proxy.setSourceModel(self._model)
        self._proxy.setDynamicSortFilter(True)
        self.treeView.setModel(self._proxy)
        
        self.filterLineEdit.textChanged.connect(self._update_filter)
        self.clearButton.clicked.connect(self._clear_filter)
        
        return
    
    def _init_title(self):
        
        self.setWindowTitle("Pipeline")
        self.treeView.setSortingEnabled(False)
        self._model.setHeaderData(0, QtCore.Qt.Horizontal, "Waiting...")

        return
        
    def _set_branch_map(self, branch_map):
        
        self._branch_map = branch_map
        
        return
        
    def _set_title(self, title):
        
        self._model.setHeaderData(0, QtCore.Qt.Horizontal, title)
        
        return
        
    def _draw(self, shell):
        
        self._clear()
        section_address = ""
        
        for branch_dict in self._branch_map:
            
            HubCls = branch_dict["hub"]
            args = []
            if "args" in branch_dict: args.extend(branch_dict["args"])
            
            # Model item
            if HubCls == SectionControl:
                section_address = branch_dict["name"]
                address = section_address
            else:
                address = section_address + "." +  branch_dict["name"]
            
            name_item = QtGui.QStandardItem(address)
            name_item.setData(address, QtCore.Qt.UserRole)
            self._model.appendRow(name_item)

            # Controller
            new_control = HubCls(address,
                                 branch_dict["name"],
                                 self.treeView,
                                 self._model,
                                 self._proxy,
                                 *args)
            new_control._init_ui(name_item)
            new_control._activate(shell, name_item)
            
            self._controls.append(new_control)
        
        return
        
    def _expand(self, shell):
        
        for controller in self._controls:
            controller._expand(shell)
        
        return
    
    def _refresh(self, shell, expand=True):
        
        self._draw(shell)
        if expand: self._expand(shell)
        
        return
        
    def _clear(self):
        
        root = self._model.invisibleRootItem()
        root.removeRows(0, root.rowCount())
        
        self._controls = []

        return
        
    def _find_controller(self, proxy_index,
                               controller_class=None,
                               root=None):
        
        if root is None: root = self
        
        address = self._proxy.data(proxy_index, QtCore.Qt.UserRole)

        for controller in root._controls:
            
            if controller._address == address:
                if (controller_class is None or
                    isinstance(controller, controller_class)):
                    return controller
                    
            result = self._find_controller(proxy_index,
                                           controller_class,
                                           controller)
            
            if result is not None: return result

        return None
        
    def _make_menus(self, shell, position):
                
        proxy_indexes = self.treeView.selectedIndexes()
        proxy_index = proxy_indexes[0]
        controller = self._find_controller(proxy_index)

        if isinstance(controller, InputBranchControl):
            
            # Set the widget action
            self._test_data_picker.buttonBox.button(
                         QtGui.QDialogButtonBox.Ok).clicked.disconnect()
            self._test_data_picker.buttonBox.button(
                         QtGui.QDialogButtonBox.Ok).clicked.connect(
                             lambda: self._read_test_data(shell, controller))
            self._test_data_picker.buttonBox.button(
                         QtGui.QDialogButtonBox.Ok).clicked.connect(
                             self._test_data_picker.close)
            
            # Build module and theme context menu
            if controller._hub_title in ["Modules", "Assessment"]:
                
                menu = QtGui.QMenu()
                
                # Enable tooltips
                tips = lambda action: QtGui.QToolTip.showText(
                                                QtGui.QCursor.pos(),
                                                action.toolTip(),
                                                menu,
                                                menu.actionGeometry(action))
                menu.hovered.connect(tips)
                
                if controller._hub_title == "Modules":
                    
                    # Can't reset or insepct unless the interface has executed
                    connector = _get_connector(shell.project, "modules")
                    
                    active =  connector.is_interface_completed(
                                                            shell.core,
                                                            shell.project,
                                                            controller._title)
                    
                    action = menu.addAction('Inspect',
                                            lambda: controller._inspect(shell))
                    action.setToolTip('Inspect results following '
                                      'execution of this module')
                    action.setEnabled(active)
                    
                    action = menu.addAction('Reset',
                                            lambda: controller._reset(shell))
                    action.setToolTip('Reset simulation prior to '
                                      'execution of this module')
                    action.setEnabled(active)
                    
                menu.addAction('Load test data...', 
                               self._test_data_picker.show)
                menu.exec_(self.treeView.mapToGlobal(position))
            
        elif isinstance(controller, OutputBranchControl):
            
            # Build module context menu
            if controller._hub_title == "Modules":
                
                menu = QtGui.QMenu()
                menu.addAction('Inspect', lambda: controller._inspect(shell))
                menu.exec_(self.treeView.mapToGlobal(position))
     
        return
        
    def _set_top_item(self):
        
        index = self._controls[0]._get_index_from_address()
        proxy_index = self._proxy.mapFromSource(index)
        self.treeView.clicked.emit(proxy_index)
        
        return
    
    def _read_auto(self, shell):
        
        self._tree.read_auto(shell.core,
                             shell.project)
                             
        return
    
    @QtCore.pyqtSlot(str)
    def _update_filter(self, text):
        
        search = QtCore.QRegExp(text,
                                QtCore.Qt.CaseInsensitive,
                                QtCore.QRegExp.RegExp
                                )

        self._proxy.setFilterRegExp(search)
        
        return
    
    @QtCore.pyqtSlot(str)
    def _repeat_filter(self):
        
        text = self.filterLineEdit.text()
        
        search = QtCore.QRegExp(text,
                                QtCore.Qt.CaseInsensitive,
                                QtCore.QRegExp.RegExp
                                )

        self._proxy.setFilterRegExp(search)
        
        return
    
    @QtCore.pyqtSlot()
    def _clear_filter(self):
        
        self.filterLineEdit.clear()
        self._update_filter("")
        
        return
    
    @QtCore.pyqtSlot(object, object)
    def _read_test_data(self, shell, controller):
        
        if shell._active_thread is not None: shell._active_thread.wait()
        
        shell.read_test_data(controller,
                             str(self._test_data_picker.pathLineEdit.text()),
                             self._test_data_picker.overwriteBox.isChecked())

        shell._active_thread.error_detected.connect(self._emit_error)
        
        return

        
    @QtCore.pyqtSlot(object, object, object)
    def _emit_error(self, etype, evalue, etraceback):
        
        self.error_detected.emit(etype, evalue, etraceback)
        
        return


class BaseControl(object):
    
    def __init__(self, address,
                       title,
                       view,
                       model,
                       proxy):

        self._address = address
        self._title = title
        self._view = view
        self._model = model
        self._proxy = proxy
        self._id = None
        self._status = None
        self._controls = []

        return
    
    def _init_ui(self, item):

        item.setText(self._title)

        return
    
    def _is_hidden(self):
        
        result = False
        
        if self._address[-1] == "-": result = True
        
        return result
        
    def _activate(self, shell, parent):
            
        return
        
    def _expand(self, shell):
        
        for controller in self._controls:
            controller._expand(shell)
        
        index = self._get_index_from_address()
        proxy_index = self._proxy.mapFromSource(index)
        self._view.expand(proxy_index)
        
        return
        
    def _clear(self):
        
        for controller in self._controls:
            index = controller._get_index_from_address()
            self._model.removeRow(index.row(), index.parent())
        
        self._controls = []

        return
    
    def _get_index_from_address(self, address=None):
        
        if address is None: address = self._address
                
        indexes = self._model.match(self._model.index(0, 0),
                                    QtCore.Qt.UserRole,
                                    address,
                                    -1,
                                    QtCore.Qt.MatchRecursive)
        
        if not indexes:
            return None
        else:
            return indexes[0]
    
    def _get_data_widget(self, shell):
        
        return None
        
    def _get_plot_widget(self, shell, plot_name):
        
        return None


class SectionControl(BaseControl):
    
    def _init_ui(self, item):
        
        # Formatting
        section_wrapper = "------   {}   ------"
        section_title = section_wrapper.format(self._title)
        
        item.setText(section_title)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        bbrush = QtGui.QBrush(QtGui.QColor("lightgrey"))
        item.setBackground(bbrush)
        
        return
    
    def _expand(self, shell):
        
        return

        
class HubControl(BaseControl):
    
    def __init__(self, address,
                       title,
                       view,
                       model,
                       proxy,
                       hub_name,
                       branch_cls,
                       active=True,
                       branch_order=None):
        
        super(HubControl, self).__init__(address, title, view, model, proxy)
        self._tree = Tree()
        self._hub_name = hub_name
        self._BranchCls = branch_cls
        self._active = active
        self._branch_order = branch_order
        
        return
        
    def _activate(self, shell, parent):
        
        hub_branches = self._tree.get_available_branches(shell.core,
                                                         shell.project,
                                                         [self._hub_name])
                                                                                                                  
        if self._branch_order is None:
            branch_order = hub_branches
        else:
            branch_order = [branch for branch in self._branch_order
                                                    if branch in hub_branches]
                                                         
        for branch_name in branch_order:
            
            branch = self._tree.get_branch(shell.core,
                                           shell.project,
                                           branch_name)
            
            # Model item
            address = self._address + "." + branch_name
            name_item = QtGui.QStandardItem(address)
            name_item.setData(address, QtCore.Qt.UserRole)
            parent.appendRow(name_item)
            
            # Controller
            new_control = self._BranchCls(address,
                                          branch_name,
                                          self._view,
                                          self._model,
                                          self._proxy,
                                          branch,
                                          self._title)
            
            new_control._init_ui(name_item)
            
            if self._active:
                new_control._activate(shell, name_item, address)
#            else:
#                new_item.setDisabled(True)
            
            self._controls.append(new_control)
            
        return


class InputBranchControl(BaseControl):
    
    def __init__(self, address,
                       title,
                       view,
                       model,
                       proxy,
                       branch,
                       hub_title,
                       ignore_str="hidden",
                       sort=True):
                           
        super(InputBranchControl, self).__init__(address,
                                                 title,
                                                 view,
                                                 model,
                                                 proxy)
        self._branch = branch
        self._hub_title = hub_title
        self._ignore_str = ignore_str
        self._sort = sort
        self._parent_address = None
        
        return
        
    def _activate(self, shell, parent, parent_address):
        
        # Save the parent's address
        self._parent_address = parent_address

        # Update status on variable updated events
        shell.update_pipeline.connect(self._update_status)
        
        # Initiate items
        self._make_input_items(shell)
        
        return
    
    def _expand(self, shell):
            
        input_status = self._branch.get_input_status(shell.core,
                                                     shell.project)
                                                     
        if not set(input_status.values()) == set(["unavailable"]):
            index = self._get_index_from_address()
            proxy_index = self._proxy.mapFromSource(index)
            self._view.expand(proxy_index)
        
        return
    
    def _make_input_items(self, shell):
        
        input_status = self._branch.get_input_status(shell.core,
                                                     shell.project)
        
        parent_index = self._get_index_from_address(self._parent_address)
        parent_item = self._model.itemFromIndex(parent_index)
        
        if self._sort: 
            
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

            # Model item
            address = self._address + "." + metadata.title
            name_item = QtGui.QStandardItem(address)
            name_item.setData(address, QtCore.Qt.UserRole)
            parent_item.appendRow(name_item)
            
            # Controller
            new_control = InputVarControl(self._address + "." + metadata.title,
                                          metadata.title,
                                          self._view,
                                          self._model,
                                          self._proxy,
                                          new_var,
                                          status)
            
            new_control._init_ui(name_item)
            
            self._controls.append(new_control)
        
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

        for controller in self._controls:
            if controller._variable._id in required:
                item_names.append(controller._title)
                
        section_names = [self._hub_title]*len(item_names)
        branch_names = [self._title]*len(item_names)

        address_dict = {"Section": section_names,
                        "Branch" : branch_names,
                        "Item"   : item_names}

        address_df = pd.DataFrame(address_dict)

        return address_df
    
    @QtCore.pyqtSlot(object)
    def _update_status(self, shell):
        
        # Remake the items
        self._clear()
        self._make_input_items(shell)
        
        return

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
        
        if shell._active_thread is not None: shell._active_thread.wait()

        self._branch.inspect(shell.core,
                             shell.project)
        
        return

    @QtCore.pyqtSlot(object)
    def _reset(self, shell):
        
        if shell._active_thread is not None: shell._active_thread.wait()

        self._branch.reset(shell.core,
                           shell.project)
        
        return


class OutputBranchControl(BaseControl):
    
    def __init__(self, address,
                       title,
                       view,
                       model,
                       proxy,
                       branch,
                       hub_title,
                       ignore_str="hidden"):
                           
        super(OutputBranchControl, self).__init__(address,
                                                  title,
                                                  view,
                                                  model,
                                                  proxy)
        self._branch = branch
        self._hub_title = hub_title
        self._ignore_str = ignore_str
        
        return
        
    def _activate(self, shell, parent, parent_address, sort=True):
        
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

            # Model item
            address = self._address + "." + metadata.title
            name_item = QtGui.QStandardItem(address)
            name_item.setData(address, QtCore.Qt.UserRole)
            parent.appendRow(name_item)
            
            # Controller
            new_control = OutputVarControl(
                                        self._address + "." + metadata.title,
                                        metadata.title,
                                        self._view,
                                        self._model,
                                        self._proxy,
                                        new_var,
                                        status)
            
            new_control._init_ui(name_item)
            
            self._controls.append(new_control)
            
        return
        
    def _expand(self, shell):
            
        output_status = self._branch.get_output_status(shell.core,
                                                       shell.project)
                                                     
        if not set(output_status.values()) == set(["unavailable"]):
            index = self._get_index_from_address()
            proxy_index = self._proxy.mapFromSource(index)
            self._view.expand(proxy_index)
        
        return
            
    @QtCore.pyqtSlot(object)
    def _update_status(self, shell):

        output_status = self._branch.get_output_status(shell.core,
                                                       shell.project)
        
        for controller in self._controls:
            status = output_status[controller._variable._id]
            controller._update_status(status)
            
        return
        
    @QtCore.pyqtSlot(object)
    def _inspect(self, shell):
        
        if shell._active_thread is not None: shell._active_thread.wait()

        self._branch.inspect(shell.core,
                             shell.project)
        
        return


class VarControl(BaseControl):
        
    def __init__(self, address,
                       title,
                       view,
                       model,
                       proxy,
                       variable,
                       status):
                           
        super(VarControl, self).__init__(address, title, view, model, proxy)
        self._variable = variable
        self._id = variable._id
        
        self._update_status(status)
        
        return
        
    def _expand(self, shell):
        
        return
        
    def _set_icon_red(self):
        
        index = self._get_index_from_address()
        item = self._model.itemFromIndex(index)

        self._icon = QtGui.QIcon()
        self._icon.addPixmap(make_redicon_pixmap(),
                             QtGui.QIcon.Normal,
                             QtGui.QIcon.Off)
        item.setIcon(self._icon)

        return

    def _set_icon_green(self):
        
        index = self._get_index_from_address()
        item = self._model.itemFromIndex(index)
        
        self._icon = QtGui.QIcon()
        self._icon.addPixmap(make_greenicon_pixmap(),
                             QtGui.QIcon.Normal,
                             QtGui.QIcon.Off)
        item.setIcon(self._icon)

        return

    def _set_icon_blue(self):
        
        index = self._get_index_from_address()
        item = self._model.itemFromIndex(index)

        self._icon = QtGui.QIcon()
        self._icon.addPixmap(make_blueicon_pixmap(),
                             QtGui.QIcon.Normal,
                             QtGui.QIcon.Off)
        item.setIcon(self._icon)

        return

    def _set_icon_cancel(self):
        
        index = self._get_index_from_address()
        item = self._model.itemFromIndex(index)

        self._icon = QtGui.QIcon()
        self._icon.addPixmap(make_buttoncancel_pixmap(),
                             QtGui.QIcon.Normal,
                             QtGui.QIcon.Off)
        item.setIcon(self._icon)

        return
        
    def _update_status(self, status=None):
        
        if status is None:
            status = self._status
        else:
            self._status = status
        
        index = self._get_index_from_address()
        item = self._model.itemFromIndex(index)
        item_user_data = item.data(QtCore.Qt.UserRole).toString()

        if status == "satisfied":

            if item_user_data[-1] == "-":
                item_user_data = item_user_data[:-1]
            
            item.setFlags(QtCore.Qt.ItemIsSelectable |
                          QtCore.Qt.ItemIsUserCheckable |
                          QtCore.Qt.ItemIsEnabled)
            self._set_icon_green()

        elif status == "required":

            if item_user_data[-1] == "-":
                item_user_data = item_user_data[:-1]
            
            item.setFlags(QtCore.Qt.ItemIsSelectable |
                          QtCore.Qt.ItemIsUserCheckable |
                          QtCore.Qt.ItemIsEnabled)
            self._set_icon_red()

        elif status == "optional":

            if item_user_data[-1] == "-":
                item_user_data = item_user_data[:-1]
            
            item.setFlags(QtCore.Qt.ItemIsSelectable |
                          QtCore.Qt.ItemIsUserCheckable |
                          QtCore.Qt.ItemIsEnabled)
            self._set_icon_blue()
        
        self._address = item_user_data
        item.setData(item_user_data, QtCore.Qt.UserRole)

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
        
        # Check that the plot name is valid
        if plot_name is not None:
            if plot_name not in self._variable.get_available_plots(
                                                            shell.core, 
                                                            shell.project,
                                                            include_auto=True):
                plot_name = None
                
        interface = self._variable._get_receiving_interface(shell.core, 
                                                            shell.project,
                                                            "PlotInterface",
                                                            "AutoPlot",
                                                            plot_name)

        if (interface is None or
            not shell.core.can_load_interface(shell.project,
                                              interface)): return None
        
        self._variable._write_interface(shell.core, 
                                        shell.project,
                                        interface)
        
        if interface.fig_handle is None: return None
        
        widget = MPLWidget(interface.fig_handle, shell.core._input_parent)
        
        return widget
    
    def _save_plot(self, shell, file_path, size, plot_name=None, dpi=220):
        
        # Check that the plot name is valid
        if plot_name is not None:
            if plot_name not in self._variable.get_available_plots(
                                                            shell.core, 
                                                            shell.project,
                                                            include_auto=True):
                plot_name = None
        
        interface = self._variable._get_receiving_interface(shell.core, 
                                                            shell.project,
                                                            "PlotInterface",
                                                            "AutoPlot",
                                                            plot_name)

        if (interface is None or
            not shell.core.can_load_interface(shell.project,
                                              interface)): return None
        
        self._variable._write_interface(shell.core, 
                                        shell.project,
                                        interface)
        
        if interface.fig_handle is None: return None
        
        interface.fig_handle.set_size_inches(*size)
                        
        with plt.rc_context(rc={'font.size': 8,
                                'font.sans-serif': 'Verdana'}):
        
            interface.fig_handle.savefig(str(file_path),
                                         dpi=dpi,
                                         bbox_inches='tight')
            
        plt.close(interface.fig_handle)
        
        # Ensure DPI is saved
        try:
            im = Image.open(str(file_path))
            im.save(str(file_path), dpi=[dpi, dpi])
        except IOError:
            pass
        
        return


class InputVarControl(VarControl):
    
    @QtCore.pyqtSlot(str)
    def _update_status(self, status=None):
        
        if status is None:
            status = self._status
        else:
            self._status = status
        
        index = self._get_index_from_address()
        item = self._model.itemFromIndex(index)
        item_user_data = item.data(QtCore.Qt.UserRole).toString()

        if "unavailable" in status:

            if item_user_data[-1] == "-":
                item_user_data = item_user_data[:-1]
            
            item.setFlags(QtCore.Qt.NoItemFlags)
            self._set_icon_cancel()
            
        elif "overwritten" in status:

            if item_user_data[-1] != "-":
                item_user_data += "-"
        
        self._address = item_user_data
        item.setData(item_user_data, QtCore.Qt.UserRole)
        
        super(InputVarControl, self)._update_status(status)

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
                                                   
        widget = super(InputVarControl, self)._get_data_widget(shell, interface)
        
        # Provide the cancel widget if no other can be found
        if widget is None: widget = CancelWidget()

        return widget


class OutputVarControl(VarControl):
    
    @QtCore.pyqtSlot(str)
    def _update_status(self, status=None):
        
        if status is None:
            status = self._status
        else:
            self._status = status
        
        index = self._get_index_from_address()
        item = self._model.itemFromIndex(index)
        item_user_data = item.data(QtCore.Qt.UserRole).toString()

        if "unavailable" in status or "overwritten" in status:

            if item_user_data[-1] != "-":
                item_user_data += "-"
        
        self._address = item_user_data
        item.setData(item_user_data, QtCore.Qt.UserRole)
        
        super(OutputVarControl, self)._update_status(status)

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
                                                   
        widget = super(OutputVarControl, self)._get_data_widget(shell, interface)

        return widget

