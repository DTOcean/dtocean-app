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


class LeafFilterProxyModel(QtGui.QSortFilterProxyModel):
    ''' Class to override the following behaviour:
            If a parent item doesn't match the filter,
            none of its children will be shown.
 
        This Model matches items which are descendants
        or ascendants of matching items.
    '''
 
    def filterAcceptsRow(self, row_num, source_parent):
        ''' Overriding the parent function '''
 
        # Check if the current row matches
        if self.filter_accepts_row_itself(row_num, source_parent):
            return True
 
        # Traverse up all the way to root and check if any of them match
        if self.filter_accepts_any_parent(source_parent):
            return True
 
        # Finally, check if any of the children match
        return self.has_accepted_children(row_num, source_parent)
 
    def filter_accepts_row_itself(self, row_num, parent):
        return super(LeafFilterProxyModel, self).filterAcceptsRow(row_num, parent)
 
    def filter_accepts_any_parent(self, parent):
        ''' Traverse to the root node and check if any of the
            ancestors match the filter
        '''
        while parent.isValid():
            if self.filter_accepts_row_itself(parent.row(), parent.parent()):
                return True
            parent = parent.parent()
        return False
 
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
        self._proxy = LeafFilterProxyModel()
        self._proxy.setSourceModel(self._model)
#        self._model.setDynamicSortFilter(True)
#        self._model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.treeView.setModel(self._proxy)
        
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
        
        source_model = self._model
        root_item = source_model.invisibleRootItem()
        
        for branch_dict in self._branch_map:
            
            HubCls = branch_dict["hub"]
            args = []
            if "args" in branch_dict: args.extend(branch_dict["args"])
            
            # Model item
            new_item = QtGui.QStandardItem(branch_dict["name"])
            root_item.appendRow(new_item)
            
            # Controller
            new_control = HubCls(new_item,
                                 branch_dict["name"],
                                 self.treeView,
                                 source_model,
                                 self._proxy,
                                 *args)
            new_control._init_ui(new_item)
            new_control._activate(shell, new_item)
            
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
                
        item_index = self.treeView.currentIndex()

        if isinstance(item, InputBranchModel):
            
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
                
                # Enable tooltips
                tips = lambda action: QtGui.QToolTip.showText(
                                                QtGui.QCursor.pos(),
                                                action.toolTip(),
                                                menu,
                                                menu.actionGeometry(action))
                menu.hovered.connect(tips)
                
                if item._hub_title == "Modules":
                    
                    # Can't reset or insepct unless the interface has executed
                    connector = _get_connector(shell.project, "modules")
                    
                    active =  connector.is_interface_completed(shell.core,
                                                               shell.project,
                                                               item._title)
                    
                    action = menu.addAction('Inspect',
                                            lambda: item._inspect(shell))
                    action.setToolTip('Inspect results following '
                                      'execution of this module')
                    action.setEnabled(active)
                    
                    action = menu.addAction('Reset',
                                            lambda: item._reset(shell))
                    action.setToolTip('Reset simulation prior to '
                                      'execution of this module')
                    action.setEnabled(active)
                    
                menu.addAction('Load test data...', 
                               self._test_data_picker.show)
                menu.exec_(self.treeView.mapToGlobal(position))
            
        elif isinstance(item, OutputBranchModel):
            
            # Build module context menu
            if item._hub_title == "Modules":
                
                menu = QtGui.QMenu()
                menu.addAction('Inspect', lambda: item._inspect(shell))
                menu.exec_(self.treeView.mapToGlobal(position))
     
        return
        
    def _set_top_item(self):
        
        source_model = self._model
        index = source_model.indexFromItem(self._controls[0]._item)
        proxy_index = self._proxy.mapFromSource(index)
        self.treeView.clicked.emit(proxy_index)
        
        return
    
    def _read_auto(self, shell):
        
        self._tree.read_auto(shell.core,
                             shell.project)
                             
        return
    
    @QtCore.pyqtSlot(object, object)
    def _read_test_data(self, shell, item):
        
        if shell._active_thread is not None: shell._active_thread.wait()
        
        shell.read_test_data(item,
                             str(self._test_data_picker.pathLineEdit.text()),
                             self._test_data_picker.overwriteBox.isChecked())

        shell._active_thread.error_detected.connect(self._emit_error)
        
        return

        
    @QtCore.pyqtSlot(object, object, object)
    def _emit_error(self, etype, evalue, etraceback):
        
        self.error_detected.emit(etype, evalue, etraceback)
        
        return


class BaseControl(object):
    
    def __init__(self, item,
                       title,
                       view,
                       model,
                       proxy):

        self._item = item
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
        
    def _activate(self, shell, parent):
            
        return
        
    def _expand(self, shell):
        
        for controller in self._controls:
            controller._expand(shell)
        
        index = self._model.indexFromItem(self._item)
        proxy_index = self._proxy.mapFromSource(index)
        self._view.expand(proxy_index)
        
        return
        
    def _clear(self):
                
        for controller in self._controls:
            index = self._model.indexFromItem(controller._item)
            proxy_index = self._proxy.mapFromSource(index)
            self._model.removeRow(proxy_index.row(), proxy_index.parent())
        
        self._controls = []

        return
        
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
    
    def __init__(self, item,
                       title,
                       view,
                       model,
                       proxy,
                       hub_name,
                       branch_cls,
                       active=True,
                       branch_order=None):
        
        super(HubControl, self).__init__(item, title, view, model, proxy)
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
            new_item = QtGui.QStandardItem(branch_name)
            parent.appendRow(new_item)
            
            # Controller
            new_control = self._BranchCls(new_item,
                                          branch_name,
                                          self._view,
                                          self._model,
                                          self._proxy,
                                          branch,
                                          self._title)
            
            new_control._init_ui(new_item)
            
            if self._active:
                new_control._activate(shell, new_item)
#            else:
#                new_item.setDisabled(True)
            
            self._controls.append(new_control)
            
        return


class InputBranchControl(BaseControl):
    
    def __init__(self, item,
                       title,
                       view,
                       model,
                       proxy,
                       branch,
                       hub_title,
                       ignore_str="hidden",
                       sort=True):
                           
        super(InputBranchControl, self).__init__(item, title, view, model, proxy)
        self._branch = branch
        self._hub_title = hub_title
        self._ignore_str = ignore_str
        self._sort = sort
        self._parent = None
        
        return
        
    def _activate(self, shell, parent):
        
        # Store the parent item
        self._parent = parent
        
        # Update status on variable updated events
        shell.update_pipeline.connect(self._update_status)
        
        # Initiate items
        self._make_input_items(shell)
        
        return
    
    def _expand(self, shell):
            
        input_status = self._branch.get_input_status(shell.core,
                                                     shell.project)
                                                     
        if not set(input_status.values()) == set(["unavailable"]):
            index = self._model.indexFromItem(self._item)
            proxy_index = self._proxy.mapFromSource(index)
            self._view.expand(proxy_index)
        
        return
    
    def _make_input_items(self, shell):
        
        input_status = self._branch.get_input_status(shell.core,
                                                     shell.project)
        
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
            new_item = QtGui.QStandardItem(metadata.title)
            self._parent.appendRow(new_item)
            
            # Controller
            new_control = InputVarControl(new_item,
                                          metadata.title,
                                          self._view,
                                          self._model,
                                          self._proxy,
                                          new_var,
                                          status)
            new_control._init_ui(new_item)
            
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
    
    def __init__(self, item,
                       title,
                       view,
                       model,
                       proxy,
                       branch,
                       hub_title,
                       ignore_str="hidden"):
                           
        super(OutputBranchControl, self).__init__(item, title, view, model, proxy)
        self._branch = branch
        self._hub_title = hub_title
        self._ignore_str = ignore_str
        
        return
        
    def _activate(self, shell, parent, sort=True):
        
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
            new_item = QtGui.QStandardItem(metadata.title)
            parent.appendRow(new_item)
            
            # Controller
            new_control = OutputVarControl(new_item,
                                           metadata.title,
                                           self._view,
                                           self._model,
                                           self._proxy,
                                           new_var,
                                           status)
            new_control._init_ui(new_item)
            
            self._controls.append(new_control)
            
        return
        
    def _expand(self, shell):
            
        output_status = self._branch.get_output_status(shell.core,
                                                       shell.project)
                                                     
        if not set(output_status.values()) == set(["unavailable"]):
            index = self._model.indexFromItem(self._item)
            proxy_index = self._proxy.mapFromSource(index)
            self._view.expand(proxy_index)
        
        return
            
    @QtCore.pyqtSlot(object)
    def _update_status(self, shell):

        output_status = self._branch.get_output_status(shell.core,
                                                       shell.project)
        for item in self._items:
            
            status = output_status[item._variable._id]
            item._update_status(status)
            
        return
        
    @QtCore.pyqtSlot(object)
    def _inspect(self, shell):
        
        if shell._active_thread is not None: shell._active_thread.wait()

        self._branch.inspect(shell.core,
                             shell.project)
        
        return


class VarControl(BaseControl):
        
    def __init__(self, item,
                       title,
                       view,
                       model,
                       proxy,
                       variable,
                       status):
                           
        super(VarControl, self).__init__(item, title, view, model, proxy)
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
        self._item.setIcon(self._icon)

        return

    def _set_icon_blue(self):

        self._icon = QtGui.QIcon()
        self._icon.addPixmap(make_blueicon_pixmap(),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self._item.setIcon(self._icon)

        return

    def _set_icon_cancel(self):

        self._icon = QtGui.QIcon()
        self._icon.addPixmap(make_buttoncancel_pixmap(),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self._item.setIcon(self._icon)

        return
        
    def _update_status(self, status):

        self._status = status
        index = self._model.indexFromItem(self._item)
        proxy_index = self._proxy.mapFromSource(index)

        if status == "satisfied":

            self._view.setRowHidden(proxy_index.row(),
                                    proxy_index.parent(),
                                    False)
            self._item.setFlags(QtCore.Qt.ItemIsSelectable |
                                QtCore.Qt.ItemIsUserCheckable |
                                QtCore.Qt.ItemIsEnabled)
            self._set_icon_green()

        elif status == "required":

            self._view.setRowHidden(proxy_index.row(),
                                    proxy_index.parent(),
                                    False)
            self._item.setFlags(QtCore.Qt.ItemIsSelectable |
                                QtCore.Qt.ItemIsUserCheckable |
                                QtCore.Qt.ItemIsEnabled)
            self._set_icon_red()

        elif status == "optional":

            self._view.setRowHidden(proxy_index.row(),
                                    proxy_index.parent(),
                                    False)
            self._item.setFlags(QtCore.Qt.ItemIsSelectable |
                                QtCore.Qt.ItemIsUserCheckable |
                                QtCore.Qt.ItemIsEnabled)
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
            not shell.core.can_load_interface(shell.project,
                                              interface)): return None
        
        self._variable._write_interface(shell.core, 
                                        shell.project,
                                        interface)
        
        if interface.fig_handle is None: return None
        
        widget = MPLWidget(interface.fig_handle, shell.core._input_parent)
        
        return widget
    
    def _save_plot(self, shell, file_path, size, plot_name=None, dpi=220):
                        
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
    
    def _update_status(self, status):
        
        index = self._model.indexFromItem(self._item)
        proxy_index = self._proxy.mapFromSource(index)

        if "unavailable" in status:

            self._view.setRowHidden(proxy_index.row(),
                                    proxy_index.parent(),
                                    False)
            self._item.setFlags(QtCore.Qt.NoItemFlags)
            self._set_icon_cancel()
            
        elif "overwritten" in status:

            self._view.setRowHidden(proxy_index.row(),
                                    proxy_index.parent(),
                                    True)
        
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
    
    def _update_status(self, status):
        
        index = self._model.indexFromItem(self._item)
        proxy_index = self._proxy.mapFromSource(index)

        if "unavailable" in status or "overwritten" in status:
            
            self._view.setRowHidden(proxy_index.row(),
                                    proxy_index.parent(),
                                    True)
        
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

