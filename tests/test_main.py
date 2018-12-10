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

import pytest
from PyQt4 import QtCore, QtGui

from polite.paths import Directory
from dtocean_core.interfaces import ModuleInterface
from dtocean_app.core import GUICore
from dtocean_app.main import DTOceanWindow, Shell
from dtocean_app.pipeline import InputVarControl
from dtocean_app.widgets.input import ListSelect


class MockModule(ModuleInterface):
    
    @classmethod
    def get_name(cls):
        
        return "Mock Module"
        
    @classmethod         
    def declare_weight(cls):
        
        return 998

    @classmethod
    def declare_inputs(cls):
        
        input_list = ['bathymetry.layers',
                      'device.system_type',
                      'device.power_rating',
                      'device.cut_in_velocity',
                      'device.turbine_interdistance']
        
        return input_list

    @classmethod
    def declare_outputs(cls):
        
        output_list = ['project.layout',
                       'project.annual_energy',
                       'project.number_of_devices']
        
        return output_list
        
    @classmethod
    def declare_optional(cls):
        
        return None
        
    @classmethod
    def declare_id_map(self):
        
        id_map = {"dummy1": "bathymetry.layers",
                  "dummy2": "device.cut_in_velocity",
                  "dummy3": "device.system_type",
                  "dummy4": "device.power_rating",
                  "dummy5": "project.layout",
                  "dummy6": "project.annual_energy",
                  "dummy7": "project.number_of_devices",
                  "dummy8": "device.turbine_interdistance"}
                  
        return id_map
                 
    def connect(self, debug_entry=False,
                      export_data=True):
        
        return


@pytest.fixture
def core():
    
    core = GUICore()
    core._create_data_catalog()
    core._create_control()
    core._create_sockets()
    core._init_plots()
    
    return core


def test_open_dtocean_window(qtbot, mocker, core):
        
    shell = Shell(core)
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
    
    assert window.windowTitle() == "DTOcean"


def test_close_open_dock(qtbot, mocker, core):
        
    shell = Shell(core)
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
    
    assert window.windowTitle() == "DTOcean"
    
    # Close the system dock
    window._system_dock.close()
    
    def dock_is_closed(): assert window._system_dock.isHidden()

    qtbot.waitUntil(dock_is_closed)
    
    # Reopen the system dock
    menu_click(qtbot,
               window,
               window.menuView,
               "actionSystem_Log")
    
    def dock_is_open(): assert window._system_dock.isVisible()

    qtbot.waitUntil(dock_is_open)


def test_new_project(qtbot, mocker, core):
    
    shell = Shell(core)
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
                      
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
    
    assert window.windowTitle() == "DTOcean: Untitled project*"
    
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
    
    assert test_var._id == "device.system_type"


def test_set_device_type(qtbot, mocker, core):
    
    shell = Shell(core)
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
                      
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
        
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
    
    # obtain the rectangular coordinates of the child item
    tree_view = window._pipeline_dock.treeView
    index = test_var._get_index_from_address()
    proxy_index = test_var._proxy.mapFromSource(index)
    rect = tree_view.visualRect(proxy_index)
    
    # simulate the mouse click within the button coordinates
    qtbot.mouseClick(tree_view.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.topLeft())
    
    selected_index = tree_view.selectedIndexes()[0]
    
    assert selected_index == proxy_index
    assert window._data_context._bottom_contents is not None
    assert isinstance(window._data_context._bottom_contents, ListSelect)
                                  
    list_select = window._data_context._bottom_contents
    
    # Set the combo box to "Wave Floating" anc click OK
    idx = list_select.comboBox.findText("Wave Floating",
                                        QtCore.Qt.MatchFixedString)
    list_select.comboBox.setCurrentIndex(idx)

    qtbot.mouseClick(
                list_select.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                QtCore.Qt.LeftButton)
    
    def check_status():
        
        # Pick up pipeline item again as it's been rebuilt
        test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
        
        assert test_var._status == "satisfied"
    
    qtbot.waitUntil(check_status)
    
    assert True


def test_initiate_pipeline(qtbot, mocker, core):
    
    shell = Shell(core)
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
                      
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
        
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
    
    # obtain the rectangular coordinates of the child item
    tree_view = window._pipeline_dock.treeView
    index = test_var._get_index_from_address()
    proxy_index = test_var._proxy.mapFromSource(index)
    rect = tree_view.visualRect(proxy_index)
    
    # simulate the mouse click within the button coordinates
    qtbot.mouseClick(tree_view.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.topLeft())
                                  
    list_select = window._data_context._bottom_contents
    
    # Set the combo box to "Wave Floating" anc click OK
    idx = list_select.comboBox.findText("Wave Floating",
                                        QtCore.Qt.MatchFixedString)
    list_select.comboBox.setCurrentIndex(idx)

    qtbot.mouseClick(
                list_select.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                QtCore.Qt.LeftButton)
    
    def check_status():
        
        # Pick up pipeline item again as it's been rebuilt
        test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
        
        assert test_var._status == "satisfied"
    
    qtbot.waitUntil(check_status)
    
    # Initiate the pipeline
    init_pipeline_button = \
        window.scenarioToolBar.widgetForAction(window.actionInitiate_Pipeline)
    qtbot.mouseClick(init_pipeline_button, QtCore.Qt.LeftButton)
    
    data_check = window._data_check
    
    def data_check_visible(): assert data_check.isVisible()
    
    qtbot.waitUntil(data_check_visible)
    
    qtbot.mouseClick(data_check.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                     QtCore.Qt.LeftButton)
    
    def check_dataflow(): assert window.actionInitiate_Dataflow.isEnabled()
    
    qtbot.waitUntil(check_dataflow)
    
    assert True


def test_export_data(qtbot, mocker, tmpdir, core):

    # File path
    datastate_file_name = "my_datastate.dts"
    datastate_file_path = os.path.join(str(tmpdir), datastate_file_name)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
                      
    mocker.patch.object(QtGui.QFileDialog,
                        'getSaveFileName',
                        return_value=datastate_file_path)
    
    shell = Shell(core)
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
                      
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
        
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
    
    # obtain the rectangular coordinates of the child item
    tree_view = window._pipeline_dock.treeView
    index = test_var._get_index_from_address()
    proxy_index = test_var._proxy.mapFromSource(index)
    rect = tree_view.visualRect(proxy_index)
    
    # simulate the mouse click within the button coordinates
    qtbot.mouseClick(tree_view.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.topLeft())
                                  
    list_select = window._data_context._bottom_contents
    
    # Set the combo box to "Wave Floating" anc click OK
    idx = list_select.comboBox.findText("Wave Floating",
                                        QtCore.Qt.MatchFixedString)
    list_select.comboBox.setCurrentIndex(idx)

    qtbot.mouseClick(
                list_select.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                QtCore.Qt.LeftButton)
    
    def check_status():
        
        # Pick up pipeline item again as it's been rebuilt
        test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
        
        assert test_var._status == "satisfied"
    
    qtbot.waitUntil(check_status)
    
    # Export data
    menu_click(qtbot,
               window,
               window.menuData,
               "actionExport")
        
    assert os.path.isfile(datastate_file_path)
    
    
def test_import_data(qtbot, mocker, tmpdir, core):

    # File path
    datastate_file_name = "my_datastate.dts"
    datastate_file_path = os.path.join(str(tmpdir), datastate_file_name)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
                      
    mocker.patch.object(QtGui.QFileDialog,
                        'getSaveFileName',
                        return_value=datastate_file_path)
                      
    mocker.patch.object(QtGui.QFileDialog,
                        'getOpenFileName',
                        return_value=datastate_file_path)
    
    shell = Shell(core)
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
                      
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
        
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
    
    # obtain the rectangular coordinates of the child item
    tree_view = window._pipeline_dock.treeView
    index = test_var._get_index_from_address()
    proxy_index = test_var._proxy.mapFromSource(index)
    rect = tree_view.visualRect(proxy_index)
    
    # simulate the mouse click within the button coordinates
    qtbot.mouseClick(tree_view.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.topLeft())
                                  
    list_select = window._data_context._bottom_contents
    
    # Set the combo box to "Wave Floating" anc click OK
    idx = list_select.comboBox.findText("Wave Floating",
                                        QtCore.Qt.MatchFixedString)
    list_select.comboBox.setCurrentIndex(idx)

    qtbot.mouseClick(
                list_select.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                QtCore.Qt.LeftButton)
    
    def check_status():
        
        # Pick up pipeline item again as it's been rebuilt
        test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
        
        assert test_var._status == "satisfied"
    
    qtbot.waitUntil(check_status)
    
    # Export data
    menu_click(qtbot,
               window,
               window.menuData,
               "actionExport")
    
    def file_saved(): assert os.path.isfile(datastate_file_path)
    
    qtbot.waitUntil(file_saved)
    
    # Open a new project
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
    
    # Import data
    menu_click(qtbot,
               window,
               window.menuData,
               "actionImport")
    
    # Check the test variable
    qtbot.waitUntil(check_status)
    
    assert True
    
    
def test_initiate_dataflow(qtbot, mocker, core):
    
    shell = Shell(core)
    
    # Add mock module
    socket = shell.core.control._sequencer.get_socket("ModuleInterface")
    socket.add_interface(MockModule)
    
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'warning',
                        return_value=QtGui.QMessageBox.Discard)
                      
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
        
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
    
    # obtain the rectangular coordinates of the child item
    tree_view = window._pipeline_dock.treeView
    index = test_var._get_index_from_address()
    proxy_index = test_var._proxy.mapFromSource(index)
    rect = tree_view.visualRect(proxy_index)
    
    # simulate the mouse click within the button coordinates
    qtbot.mouseClick(tree_view.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.topLeft())
                                  
    list_select = window._data_context._bottom_contents
    
    # Set the combo box to "Wave Floating" anc click OK
    idx = list_select.comboBox.findText("Tidal Fixed",
                                        QtCore.Qt.MatchFixedString)
    list_select.comboBox.setCurrentIndex(idx)

    qtbot.mouseClick(
                list_select.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                QtCore.Qt.LeftButton)
    
    def check_status():
        
        # Pick up pipeline item again as it's been rebuilt
        test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
        
        assert test_var._status == "satisfied"
    
    qtbot.waitUntil(check_status)
    
    # Initiate the pipeline
    init_pipeline_button = \
        window.scenarioToolBar.widgetForAction(window.actionInitiate_Pipeline)
    qtbot.mouseClick(init_pipeline_button, QtCore.Qt.LeftButton)
    
    data_check = window._data_check
    
    def data_check_visible(): assert data_check.isVisible()
    
    qtbot.waitUntil(data_check_visible)
    
    qtbot.mouseClick(data_check.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                     QtCore.Qt.LeftButton)
    
    def check_dataflow(): assert window.actionInitiate_Dataflow.isEnabled()
    
    qtbot.waitUntil(check_dataflow)
    
    # Add a module
    add_modules_button = \
        window.simulationToolBar.widgetForAction(window.actionAdd_Modules)
    qtbot.mouseClick(add_modules_button, QtCore.Qt.LeftButton)
    
    module_shuttle = window._module_shuttle
    
    def add_modules_visible(): assert module_shuttle.isVisible()
    
    qtbot.waitUntil(add_modules_visible)
    
    # Fake click on last left item
    module_shuttle._left_index = module_shuttle._left_model.rowCount() - 1
    
    # Click "Add" then "OK"
    qtbot.mouseClick(module_shuttle.addButton,
                     QtCore.Qt.LeftButton)
    
    def module_on_right(): assert module_shuttle._get_right_data()
    
    qtbot.waitUntil(module_on_right)
    
    button = module_shuttle.buttonBox.button(QtGui.QDialogButtonBox.Ok)
    qtbot.mouseClick(button,
                     QtCore.Qt.LeftButton)
    
    def add_modules_not_visible(): assert not module_shuttle.isVisible()
    
    qtbot.waitUntil(add_modules_not_visible)
    
    # Initiate the dataflow
    init_pipeline_button = \
        window.scenarioToolBar.widgetForAction(window.actionInitiate_Dataflow)
    qtbot.mouseClick(init_pipeline_button, QtCore.Qt.LeftButton)
    
    qtbot.waitUntil(data_check_visible)
    
    qtbot.mouseClick(data_check.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                     QtCore.Qt.LeftButton)
    
    def check_run_current(): assert window.actionRun_Current.isEnabled()
    
    qtbot.waitUntil(check_run_current)
    
    def check_module_active():
        
        # Pick up pipeline item again as it's been rebuilt
        test_control = window._pipeline_dock._find_controller(
                                            controller_title="Mock Module")
        
        assert test_control is not None
    
    qtbot.waitUntil(check_module_active)
    
    assert True


def test_set_simulation_title(qtbot, mocker, core):
    
    shell = Shell(core)
    
    # Add mock module
    socket = shell.core.control._sequencer.get_socket("ModuleInterface")
    socket.add_interface(MockModule)
    
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'warning',
                        return_value=QtGui.QMessageBox.Discard)
                      
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
        
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
    
    # obtain the rectangular coordinates of the child item
    tree_view = window._pipeline_dock.treeView
    index = test_var._get_index_from_address()
    proxy_index = test_var._proxy.mapFromSource(index)
    rect = tree_view.visualRect(proxy_index)
    
    # simulate the mouse click within the button coordinates
    qtbot.mouseClick(tree_view.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.topLeft())
                                  
    list_select = window._data_context._bottom_contents
    
    # Set the combo box to "Wave Floating" anc click OK
    idx = list_select.comboBox.findText("Tidal Fixed",
                                        QtCore.Qt.MatchFixedString)
    list_select.comboBox.setCurrentIndex(idx)

    qtbot.mouseClick(
                list_select.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                QtCore.Qt.LeftButton)
    
    def check_status():
        
        # Pick up pipeline item again as it's been rebuilt
        test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
        
        assert test_var._status == "satisfied"
    
    qtbot.waitUntil(check_status)
    
    # Initiate the pipeline
    init_pipeline_button = \
        window.scenarioToolBar.widgetForAction(window.actionInitiate_Pipeline)
    qtbot.mouseClick(init_pipeline_button, QtCore.Qt.LeftButton)
    
    data_check = window._data_check
    
    def data_check_visible(): assert data_check.isVisible()
    
    qtbot.waitUntil(data_check_visible)
    
    qtbot.mouseClick(data_check.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                     QtCore.Qt.LeftButton)
    
    def check_dataflow(): assert window.actionInitiate_Dataflow.isEnabled()
    
    qtbot.waitUntil(check_dataflow)
    
    # Add a module
    add_modules_button = \
        window.simulationToolBar.widgetForAction(window.actionAdd_Modules)
    qtbot.mouseClick(add_modules_button, QtCore.Qt.LeftButton)
    
    module_shuttle = window._module_shuttle
    
    def add_modules_visible(): assert module_shuttle.isVisible()
    
    qtbot.waitUntil(add_modules_visible)
    
    # Fake click on last left item
    module_shuttle._left_index = module_shuttle._left_model.rowCount() - 1
    
    # Click "Add" then "OK"
    qtbot.mouseClick(module_shuttle.addButton,
                     QtCore.Qt.LeftButton)
    
    def module_on_right(): assert module_shuttle._get_right_data()
    
    qtbot.waitUntil(module_on_right)
    
    button = module_shuttle.buttonBox.button(QtGui.QDialogButtonBox.Ok)
    qtbot.mouseClick(button,
                     QtCore.Qt.LeftButton)
    
    def add_modules_not_visible(): assert not module_shuttle.isVisible()
    
    qtbot.waitUntil(add_modules_not_visible)
    
    # Initiate the dataflow
    init_pipeline_button = \
        window.scenarioToolBar.widgetForAction(window.actionInitiate_Dataflow)
    qtbot.mouseClick(init_pipeline_button, QtCore.Qt.LeftButton)
    
    qtbot.waitUntil(data_check_visible)
    
    qtbot.mouseClick(data_check.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                     QtCore.Qt.LeftButton)
    
    def check_run_current(): assert window.actionRun_Current.isEnabled()
    
    qtbot.waitUntil(check_run_current)
    
    def check_module_active():
        
        # Pick up pipeline item again as it's been rebuilt
        test_control = window._pipeline_dock._find_controller(
                                            controller_title="Mock Module")
        
        assert test_control is not None
    
    qtbot.waitUntil(check_module_active)
        
    # Close the pipeline
    window._pipeline_dock.close()
    
    def pipeline_not_visible(): assert not window._pipeline_dock.isVisible()
    
    qtbot.waitUntil(pipeline_not_visible)
    
    # Fake change of simulation name
    window._simulation_dock.listWidget.setCurrentRow(0)
    editor = mocker.Mock()
    editor.text.return_value = "bob"
    
    window._simulation_dock._catch_edit(editor, None)
    
    def check_name():
    
        # Pick up the default simulation
        test_sim = window._simulation_dock.listWidget.item(0)
        
        assert test_sim._title == "bob"
    
    qtbot.waitUntil(check_name)
    
    assert shell.project.get_simulation_title() == "bob"


def test_simulation_clone_select(qtbot, mocker, core):
    
    shell = Shell(core)
    
    # Add mock module
    socket = shell.core.control._sequencer.get_socket("ModuleInterface")
    socket.add_interface(MockModule)
    
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'warning',
                        return_value=QtGui.QMessageBox.Discard)
                      
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
        
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
    
    # obtain the rectangular coordinates of the child item
    tree_view = window._pipeline_dock.treeView
    index = test_var._get_index_from_address()
    proxy_index = test_var._proxy.mapFromSource(index)
    rect = tree_view.visualRect(proxy_index)
    
    # simulate the mouse click within the button coordinates
    qtbot.mouseClick(tree_view.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.topLeft())
                                  
    list_select = window._data_context._bottom_contents
    
    # Set the combo box to "Wave Floating" anc click OK
    idx = list_select.comboBox.findText("Tidal Fixed",
                                        QtCore.Qt.MatchFixedString)
    list_select.comboBox.setCurrentIndex(idx)

    qtbot.mouseClick(
                list_select.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                QtCore.Qt.LeftButton)
    
    def check_status():
        
        # Pick up pipeline item again as it's been rebuilt
        test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
        
        assert test_var._status == "satisfied"
    
    qtbot.waitUntil(check_status)
    
    # Initiate the pipeline
    init_pipeline_button = \
        window.scenarioToolBar.widgetForAction(window.actionInitiate_Pipeline)
    qtbot.mouseClick(init_pipeline_button, QtCore.Qt.LeftButton)
    
    data_check = window._data_check
    
    def data_check_visible(): assert data_check.isVisible()
    
    qtbot.waitUntil(data_check_visible)
    
    qtbot.mouseClick(data_check.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                     QtCore.Qt.LeftButton)
    
    def check_dataflow(): assert window.actionInitiate_Dataflow.isEnabled()
    
    qtbot.waitUntil(check_dataflow)
    
    # Add a module
    add_modules_button = \
        window.simulationToolBar.widgetForAction(window.actionAdd_Modules)
    qtbot.mouseClick(add_modules_button, QtCore.Qt.LeftButton)
    
    module_shuttle = window._module_shuttle
    
    def add_modules_visible(): assert module_shuttle.isVisible()
    
    qtbot.waitUntil(add_modules_visible)
    
    # Fake click on last left item
    module_shuttle._left_index = module_shuttle._left_model.rowCount() - 1
    
    # Click "Add" then "OK"
    qtbot.mouseClick(module_shuttle.addButton,
                     QtCore.Qt.LeftButton)
    
    def module_on_right(): assert module_shuttle._get_right_data()
    
    qtbot.waitUntil(module_on_right)
    
    button = module_shuttle.buttonBox.button(QtGui.QDialogButtonBox.Ok)
    qtbot.mouseClick(button,
                     QtCore.Qt.LeftButton)
    
    def add_modules_not_visible(): assert not module_shuttle.isVisible()
    
    qtbot.waitUntil(add_modules_not_visible)
    
    # Initiate the dataflow
    init_pipeline_button = \
        window.scenarioToolBar.widgetForAction(window.actionInitiate_Dataflow)
    qtbot.mouseClick(init_pipeline_button, QtCore.Qt.LeftButton)
    
    qtbot.waitUntil(data_check_visible)
    
    qtbot.mouseClick(data_check.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                     QtCore.Qt.LeftButton)
    
    def check_run_current(): assert window.actionRun_Current.isEnabled()
    
    qtbot.waitUntil(check_run_current)
    
    def check_module_active():
        
        # Pick up pipeline item again as it's been rebuilt
        test_control = window._pipeline_dock._find_controller(
                                            controller_title="Mock Module")
        
        assert test_control is not None
    
    qtbot.waitUntil(check_module_active)
    
    # Close the pipeline
    window._pipeline_dock.close()
    
    def pipeline_not_visible(): assert not window._pipeline_dock.isVisible()
    
    qtbot.waitUntil(pipeline_not_visible)
    
    # Fake clone the simulation
    window._simulation_dock._clone_current(window._shell)
    
    def has_two_simulations():
        assert window._simulation_dock.listWidget.count() == 2
    
    qtbot.waitUntil(has_two_simulations)
    
    # Check the new simulation name
    test_sim = window._simulation_dock.listWidget.item(1)
    
    assert test_sim._title == "Default Clone 1"
    
    # Select the default simulation
    item = window._simulation_dock.listWidget.item(0)
    rect = window._simulation_dock.listWidget.visualItemRect(item)
    qtbot.mouseClick(window._simulation_dock.listWidget.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.center())
    
    def is_active_simulation():
        assert window._shell.project.get_simulation_title() == "Default"
    
    qtbot.waitUntil(is_active_simulation)


def test_credentials_add_delete(qtbot, mocker, tmpdir, core):
    
    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_core.utils.database.UserDataDirectory',
                 return_value=mock_dir,
                 autospec=True)

    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
                      
    
    shell = Shell(core)
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)

    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
    
    assert window.windowTitle() == "DTOcean: Untitled project*"
    
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
    
    assert test_var._id == "device.system_type"
    
    # Get the select database button and click it
    new_project_button = \
        window.scenarioToolBar.widgetForAction(window.actionSelect_Database)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
    
    db_selector = window._db_selector
    
    def db_selector_visible(): assert db_selector.isVisible()
    
    qtbot.waitUntil(db_selector_visible)
    
    n_creds = db_selector.listWidget.count()
    
    # Press the add button
    qtbot.mouseClick(db_selector.addButton,
                     QtCore.Qt.LeftButton)
    
    def added_cred(): assert db_selector.listWidget.count() == n_creds + 1
    
    qtbot.waitUntil(added_cred)
    
    # Add another
    n_creds += 1
    
    qtbot.mouseClick(db_selector.addButton,
                     QtCore.Qt.LeftButton)
    
    def added_cred(): assert db_selector.listWidget.count() == n_creds + 1
    
    qtbot.waitUntil(added_cred)
    
    assert "unnamed-1" in db_selector._data_menu.get_available_databases()
    
    # Delete all credentials
    while db_selector.listWidget.count() > 0:
        
        # Select the last in the list and select
        item = db_selector.listWidget.item(db_selector.listWidget.count() - 1)
        rect = db_selector.listWidget.visualItemRect(item)
        qtbot.mouseClick(db_selector.listWidget.viewport(),
                         QtCore.Qt.LeftButton,
                         pos=rect.center())
                    
        qtbot.mouseClick(db_selector.deleteButton,
                         QtCore.Qt.LeftButton)
        
        def deleted_cred():
            assert db_selector.listWidget.count() == n_creds
        
        qtbot.waitUntil(deleted_cred)
        
        n_creds -= 1
        
    db_selector.close()


def test_select_database(qtbot, mocker, tmpdir, core):

    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_core.utils.database.UserDataDirectory',
                 return_value=mock_dir,
                 autospec=True)
    
    mocker.patch('dtocean_app.main.DataMenu.select_database',
                 autospec=True)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
    
    
    shell = Shell(core)
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)

    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
    
    assert window.windowTitle() == "DTOcean: Untitled project*"
    
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
    
    assert test_var._id == "device.system_type"
    
    # Get the select database button and click it
    new_project_button = \
        window.scenarioToolBar.widgetForAction(window.actionSelect_Database)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
    
    db_selector = window._db_selector
    
    def db_selector_visible(): assert db_selector.isVisible()
    
    qtbot.waitUntil(db_selector_visible)
    
    n_creds = db_selector.listWidget.count()
    
    # Press the add button
    qtbot.mouseClick(db_selector.addButton,
                     QtCore.Qt.LeftButton)
    
    def added_cred(): assert db_selector.listWidget.count() == n_creds + 1
    
    qtbot.waitUntil(added_cred)
    
    # Select the first in the list and apply
    db_selector.listWidget.setCurrentRow(0)
    
    item = db_selector.listWidget.item(0)
    rect = db_selector.listWidget.visualItemRect(item)
    qtbot.mouseClick(db_selector.listWidget.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.center())
    
    qtbot.mouseClick(
            db_selector.buttonBox.button(QtGui.QDialogButtonBox.Apply),
            QtCore.Qt.LeftButton)
    
    # Check for credentials
    def has_credentials():
        assert db_selector.topDynamicLabel.text() == item.text()
        
    qtbot.waitUntil(has_credentials)
    
    db_selector.close()


def test_deselect_database(qtbot, mocker, tmpdir, core):
    
    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_core.utils.database.UserDataDirectory',
                 return_value=mock_dir,
                 autospec=True)
    
    mocker.patch('dtocean_app.main.DataMenu.select_database',
                 autospec=True)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
    
    shell = Shell(core)
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
    
    assert window.windowTitle() == "DTOcean: Untitled project*"
    
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
    
    assert test_var._id == "device.system_type"
    
    # Get the select database button and click it
    new_project_button = \
        window.scenarioToolBar.widgetForAction(window.actionSelect_Database)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
    
    db_selector = window._db_selector
    
    def db_selector_visible(): assert db_selector.isVisible()
    
    qtbot.waitUntil(db_selector_visible)
    
    n_creds = db_selector.listWidget.count()
    
    # Press the add button
    qtbot.mouseClick(db_selector.addButton,
                     QtCore.Qt.LeftButton)
    
    def added_cred(): assert db_selector.listWidget.count() == n_creds + 1
    
    qtbot.waitUntil(added_cred)
    
    # Select the first in the list and apply
    db_selector.listWidget.setCurrentRow(0)
    
    item = db_selector.listWidget.item(0)
    rect = db_selector.listWidget.visualItemRect(item)
    qtbot.mouseClick(db_selector.listWidget.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.center())
    
    qtbot.mouseClick(
            db_selector.buttonBox.button(QtGui.QDialogButtonBox.Apply),
            QtCore.Qt.LeftButton)
    
    # Check for credentials
    def has_credentials():
        assert db_selector.topDynamicLabel.text() == item.text()
        
    qtbot.waitUntil(has_credentials)
    
    # Press reset button
    qtbot.mouseClick(
            db_selector.buttonBox.button(QtGui.QDialogButtonBox.Reset),
            QtCore.Qt.LeftButton)
    
    # Check for credentials
    def has_not_credentials():
        assert db_selector.topDynamicLabel.text() == "None"
        
    qtbot.waitUntil(has_not_credentials)
    
    db_selector.close()


def test_credentials_rename(qtbot, mocker, tmpdir, core):
    
    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_core.utils.database.UserDataDirectory',
                 return_value=mock_dir,
                 autospec=True)

    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
                      
    
    shell = Shell(core)
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)

    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
    
    assert window.windowTitle() == "DTOcean: Untitled project*"
    
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
    
    assert test_var._id == "device.system_type"
    
    # Get the select database button and click it
    new_project_button = \
        window.scenarioToolBar.widgetForAction(window.actionSelect_Database)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
    
    db_selector = window._db_selector
    
    def db_selector_visible(): assert db_selector.isVisible()
    
    qtbot.waitUntil(db_selector_visible)
    
    n_creds = db_selector.listWidget.count()
    
    # Press the add button
    qtbot.mouseClick(db_selector.addButton,
                     QtCore.Qt.LeftButton)
    
    def added_cred(): assert db_selector.listWidget.count() == n_creds + 1
    
    qtbot.waitUntil(added_cred)
    
    # Select the last in the list and chnage its name
    db_selector.listWidget.setCurrentRow(db_selector.listWidget.count() - 1)
    
    editor = mocker.Mock()
    editor.text.return_value = "bob"
    
    db_selector._rename_database(editor, None)
    
    def check_name():
        assert "bob" in db_selector._data_menu.get_available_databases()
    
    qtbot.waitUntil(check_name)
    
    # Press the add button
    n_creds += 1
    
    qtbot.mouseClick(db_selector.addButton,
                     QtCore.Qt.LeftButton)
    
    def added_cred(): assert db_selector.listWidget.count() == n_creds + 1
    
    qtbot.waitUntil(added_cred)
    
    # Select the last in the list and chnage its name
    db_selector.listWidget.setCurrentRow(db_selector.listWidget.count() - 1)
    
    editor = mocker.Mock()
    editor.text.return_value = "bob"
    
    db_selector._rename_database(editor, None)
    
    def check_one_bob():
        assert db_selector._data_menu.get_available_databases(
                                                            ).count("bob") == 1
    
    qtbot.waitUntil(check_one_bob)
    
    db_selector.close()


def test_credentials_save(qtbot, mocker, tmpdir, core):
    
    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_core.utils.database.UserDataDirectory',
                 return_value=mock_dir,
                 autospec=True)

    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
                      
    
    shell = Shell(core)
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)

    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
    
    assert window.windowTitle() == "DTOcean: Untitled project*"
    
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
    
    assert test_var._id == "device.system_type"
    
    # Get the select database button and click it
    new_project_button = \
        window.scenarioToolBar.widgetForAction(window.actionSelect_Database)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
    
    db_selector = window._db_selector
    
    def db_selector_visible(): assert db_selector.isVisible()
    
    qtbot.waitUntil(db_selector_visible)
    
    old_count = db_selector.listWidget.count()
    
    # Press the add button
    qtbot.mouseClick(db_selector.addButton,
                     QtCore.Qt.LeftButton)
    
    def added_cred(): assert db_selector.listWidget.count() == old_count + 1
    
    qtbot.waitUntil(added_cred)
    
    # Select the last in the list and chnage its name
    test_cred = db_selector.listWidget.item(
                                            db_selector.listWidget.count() - 1)
    
    test_cred.setText("bob")
    editor = mocker.Mock()
    editor.text.return_value = "bob"
    
    db_selector._rename_database(editor, None)
    
    def check_name():
        assert "bob" in db_selector._data_menu.get_available_databases()
    
    qtbot.waitUntil(check_name)
    
    item = QtGui.QTableWidgetItem(str("bob"))
    db_selector.tableWidget.setItem(0, 1, item)
    
    def can_save(): assert db_selector.saveButton.isEnabled()
    
    qtbot.waitUntil(can_save)
    
    # Press the save button
    qtbot.mouseClick(db_selector.saveButton,
                     QtCore.Qt.LeftButton)
    
    def can_not_save(): assert not db_selector.saveButton.isEnabled()
    
    qtbot.waitUntil(can_not_save)
    
    db_selector.close()


def test_dump_load_database(qtbot, mocker, tmpdir, core):
    
    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_core.utils.database.UserDataDirectory',
                 return_value=mock_dir,
                 autospec=True)

    mocker.patch('dtocean_app.menu.QtGui.QFileDialog.getExistingDirectory',
                 return_value=str(tmpdir))
    
    mocker.patch('dtocean_app.main.database_to_files',
                 autospec=True)
    
    mocker.patch('dtocean_app.main.database_from_files',
                 autospec=True)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'warning',
                        return_value=QtGui.QMessageBox.Yes)
    
    shell = Shell(core)
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
    
    assert window.windowTitle() == "DTOcean: Untitled project*"
    
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
    
    assert test_var._id == "device.system_type"
    
    # Get the select database button and click it
    new_project_button = \
        window.scenarioToolBar.widgetForAction(window.actionSelect_Database)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
    
    db_selector = window._db_selector
    
    def db_selector_visible(): assert db_selector.isVisible()
    
    qtbot.waitUntil(db_selector_visible)
    
    # Select the first in the list and apply
    db_selector.listWidget.setCurrentRow(0)
    
    item = db_selector.listWidget.item(0)
    rect = db_selector.listWidget.visualItemRect(item)
    qtbot.mouseClick(db_selector.listWidget.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.center())
    
    qtbot.mouseClick(
            db_selector.buttonBox.button(QtGui.QDialogButtonBox.Apply),
            QtCore.Qt.LeftButton)
    
    # Check for credentials
    def has_credentials():
        assert shell.project.get_database_credentials() is not None
        
    qtbot.waitUntil(has_credentials)
    
    # Activate dump
    qtbot.mouseClick(db_selector.dumpButton,
                     QtCore.Qt.LeftButton)
    
    qtbot.waitSignal(shell.database_convert_complete)
    
    def dump_enabled(): assert db_selector.dumpButton.isEnabled()
    
    qtbot.waitUntil(dump_enabled)
    
    # Activate load
    qtbot.mouseClick(db_selector.loadButton,
                     QtCore.Qt.LeftButton)
    
    qtbot.waitSignal(shell.database_convert_complete)
    
    def load_enabled(): assert db_selector.loadButton.isEnabled()
    
    qtbot.waitUntil(load_enabled)
    
    db_selector.close()


def test_save_modify_close(qtbot, mocker, tmpdir, core):
    
    shell = Shell(core)
    
    # Add mock module
    socket = shell.core.control._sequencer.get_socket("ModuleInterface")
    socket.add_interface(MockModule)
    
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'warning',
                        return_value=QtGui.QMessageBox.Discard)
    
    dto_file_path = os.path.join(str(tmpdir), "test.dto")
    
    mocker.patch.object(QtGui.QFileDialog,
                        'getSaveFileName',
                        return_value=dto_file_path)
                      
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
        
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
    
    # obtain the rectangular coordinates of the child item
    tree_view = window._pipeline_dock.treeView
    index = test_var._get_index_from_address()
    proxy_index = test_var._proxy.mapFromSource(index)
    rect = tree_view.visualRect(proxy_index)
    
    # simulate the mouse click within the button coordinates
    qtbot.mouseClick(tree_view.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.topLeft())
                                  
    list_select = window._data_context._bottom_contents
    
    # Set the combo box to "Wave Floating" anc click OK
    idx = list_select.comboBox.findText("Tidal Fixed",
                                        QtCore.Qt.MatchFixedString)
    list_select.comboBox.setCurrentIndex(idx)

    qtbot.mouseClick(
                list_select.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                QtCore.Qt.LeftButton)
    
    def check_status():
        
        # Pick up pipeline item again as it's been rebuilt
        test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
        
        assert test_var._status == "satisfied"
    
    qtbot.waitUntil(check_status)
    
    # Initiate the pipeline
    init_pipeline_button = \
        window.scenarioToolBar.widgetForAction(window.actionInitiate_Pipeline)
    qtbot.mouseClick(init_pipeline_button, QtCore.Qt.LeftButton)
    
    data_check = window._data_check
    
    def data_check_visible(): assert data_check.isVisible()
    
    qtbot.waitUntil(data_check_visible)
    
    qtbot.mouseClick(data_check.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                     QtCore.Qt.LeftButton)
    
    def check_dataflow(): assert window.actionInitiate_Dataflow.isEnabled()
    
    qtbot.waitUntil(check_dataflow)
    
    # Add a module
    add_modules_button = \
        window.simulationToolBar.widgetForAction(window.actionAdd_Modules)
    qtbot.mouseClick(add_modules_button, QtCore.Qt.LeftButton)
    
    module_shuttle = window._module_shuttle
    
    def add_modules_visible(): assert module_shuttle.isVisible()
    
    qtbot.waitUntil(add_modules_visible)
    
    # Fake click on last left item
    module_shuttle._left_index = module_shuttle._left_model.rowCount() - 1
    
    # Click "Add" then "OK"
    qtbot.mouseClick(module_shuttle.addButton,
                     QtCore.Qt.LeftButton)
    
    def module_on_right(): assert module_shuttle._get_right_data()
    
    qtbot.waitUntil(module_on_right)
    
    button = module_shuttle.buttonBox.button(QtGui.QDialogButtonBox.Ok)
    qtbot.mouseClick(button,
                     QtCore.Qt.LeftButton)
    
    def add_modules_not_visible(): assert not module_shuttle.isVisible()
    
    qtbot.waitUntil(add_modules_not_visible)
    
    # Initiate the dataflow
    init_pipeline_button = \
        window.scenarioToolBar.widgetForAction(window.actionInitiate_Dataflow)
    qtbot.mouseClick(init_pipeline_button, QtCore.Qt.LeftButton)
    
    qtbot.waitUntil(data_check_visible)
    
    qtbot.mouseClick(data_check.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                     QtCore.Qt.LeftButton)
    
    def check_run_current(): assert window.actionRun_Current.isEnabled()
    
    qtbot.waitUntil(check_run_current)
    
    def check_module_active():
        
        # Pick up pipeline item again as it's been rebuilt
        test_control = window._pipeline_dock._find_controller(
                                            controller_title="Mock Module")
        
        assert test_control is not None
    
    qtbot.waitUntil(check_module_active)
    
    # Save the simulation
    save_button = window.fileToolBar.widgetForAction(window.actionSave)
    qtbot.mouseClick(save_button, QtCore.Qt.LeftButton)

    def dto_file_saved():
        assert (len(os.listdir(str(tmpdir))) > 0 and
                os.listdir(str(tmpdir))[0] == "test.dto")
    
    qtbot.waitUntil(dto_file_saved)
    
    # Modify a variable
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Rated Power",
                                    controller_class=InputVarControl)
    
    # obtain the rectangular coordinates of the child item
    tree_view = window._pipeline_dock.treeView
    index = test_var._get_index_from_address()
    proxy_index = test_var._proxy.mapFromSource(index)
    rect = tree_view.visualRect(proxy_index)
    
    # simulate the mouse click within the button coordinates
    qtbot.mouseClick(tree_view.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.topLeft())
    
    # Let the system catch up
    qtbot.wait(200)
    
    float_select = window._data_context._bottom_contents
    
    # Set the value to 1 and click OK
    float_select.doubleSpinBox.setValue(1)

    qtbot.mouseClick(
                float_select.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                QtCore.Qt.LeftButton)
    
    def check_status_two():
        
        # Pick up pipeline item again as it's been rebuilt
        test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Rated Power",
                                    controller_class=InputVarControl)
        
        assert test_var._status == "satisfied"
    
    qtbot.waitUntil(check_status_two)
    
    def title_unsaved(): assert "*" in window.windowTitle()
    
    qtbot.waitUntil(title_unsaved)
    
    # Close the project
    close_button = window.fileToolBar.widgetForAction(window.actionClose)
    qtbot.mouseClick(close_button, QtCore.Qt.LeftButton)
    
    def close_button_not_enabled(): assert not close_button.isEnabled()
    
    qtbot.waitUntil(close_button_not_enabled)


def test_save_project(qtbot, mocker, tmpdir, core):
    
    shell = Shell(core)
    
    # Add mock module
    socket = shell.core.control._sequencer.get_socket("ModuleInterface")
    socket.add_interface(MockModule)
    
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'warning',
                        return_value=QtGui.QMessageBox.Discard)
    
    dto_file_path = os.path.join(str(tmpdir), "test.prj")
    
    mocker.patch.object(QtGui.QFileDialog,
                        'getSaveFileName',
                        return_value=dto_file_path)
                      
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
        
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
    
    # obtain the rectangular coordinates of the child item
    tree_view = window._pipeline_dock.treeView
    index = test_var._get_index_from_address()
    proxy_index = test_var._proxy.mapFromSource(index)
    rect = tree_view.visualRect(proxy_index)
    
    # simulate the mouse click within the button coordinates
    qtbot.mouseClick(tree_view.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.topLeft())
                                  
    list_select = window._data_context._bottom_contents
    
    # Set the combo box to "Wave Floating" anc click OK
    idx = list_select.comboBox.findText("Tidal Fixed",
                                        QtCore.Qt.MatchFixedString)
    list_select.comboBox.setCurrentIndex(idx)

    qtbot.mouseClick(
                list_select.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                QtCore.Qt.LeftButton)
    
    def check_status():
        
        # Pick up pipeline item again as it's been rebuilt
        test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
        
        assert test_var._status == "satisfied"
    
    qtbot.waitUntil(check_status)
    
    # Initiate the pipeline
    init_pipeline_button = \
        window.scenarioToolBar.widgetForAction(window.actionInitiate_Pipeline)
    qtbot.mouseClick(init_pipeline_button, QtCore.Qt.LeftButton)
    
    data_check = window._data_check
    
    def data_check_visible(): assert data_check.isVisible()
    
    qtbot.waitUntil(data_check_visible)
    
    qtbot.mouseClick(data_check.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                     QtCore.Qt.LeftButton)
    
    def check_dataflow(): assert window.actionInitiate_Dataflow.isEnabled()
    
    qtbot.waitUntil(check_dataflow)
    
    # Add a module
    add_modules_button = \
        window.simulationToolBar.widgetForAction(window.actionAdd_Modules)
    qtbot.mouseClick(add_modules_button, QtCore.Qt.LeftButton)
    
    module_shuttle = window._module_shuttle
    
    def add_modules_visible(): assert module_shuttle.isVisible()
    
    qtbot.waitUntil(add_modules_visible)
    
    # Fake click on last left item
    module_shuttle._left_index = module_shuttle._left_model.rowCount() - 1
    
    # Click "Add" then "OK"
    qtbot.mouseClick(module_shuttle.addButton,
                     QtCore.Qt.LeftButton)
    
    def module_on_right(): assert module_shuttle._get_right_data()
    
    qtbot.waitUntil(module_on_right)
    
    button = module_shuttle.buttonBox.button(QtGui.QDialogButtonBox.Ok)
    qtbot.mouseClick(button,
                     QtCore.Qt.LeftButton)
    
    def add_modules_not_visible(): assert not module_shuttle.isVisible()
    
    qtbot.waitUntil(add_modules_not_visible)
    
    # Initiate the dataflow
    init_pipeline_button = \
        window.scenarioToolBar.widgetForAction(window.actionInitiate_Dataflow)
    qtbot.mouseClick(init_pipeline_button, QtCore.Qt.LeftButton)
    
    qtbot.waitUntil(data_check_visible)
    
    qtbot.mouseClick(data_check.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                     QtCore.Qt.LeftButton)
    
    def check_run_current(): assert window.actionRun_Current.isEnabled()
    
    qtbot.waitUntil(check_run_current)
    
    def check_module_active():
        
        # Pick up pipeline item again as it's been rebuilt
        test_control = window._pipeline_dock._find_controller(
                                            controller_title="Mock Module")
        
        assert test_control is not None
    
    qtbot.waitUntil(check_module_active)
    
    # Save the simulation
    save_button = window.fileToolBar.widgetForAction(window.actionSave)
    qtbot.mouseClick(save_button, QtCore.Qt.LeftButton)
    
    def dto_file_saved():
         assert (len(os.listdir(str(tmpdir))) > 0 and
                 os.listdir(str(tmpdir))[0] == "test.prj")
    
    qtbot.waitUntil(dto_file_saved)


def test_select_strategy(qtbot, mocker, tmpdir, core):
    
    shell = Shell(core)
    
    # Add mock module
    socket = shell.core.control._sequencer.get_socket("ModuleInterface")
    socket.add_interface(MockModule)
    
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'warning',
                        return_value=QtGui.QMessageBox.Discard)
    
    dto_file_path = os.path.join(str(tmpdir), "test.dto")
    
    mocker.patch.object(QtGui.QFileDialog,
                        'getSaveFileName',
                        return_value=dto_file_path)
                      
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
        
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
    
    # obtain the rectangular coordinates of the child item
    tree_view = window._pipeline_dock.treeView
    index = test_var._get_index_from_address()
    proxy_index = test_var._proxy.mapFromSource(index)
    rect = tree_view.visualRect(proxy_index)
    
    # simulate the mouse click within the button coordinates
    qtbot.mouseClick(tree_view.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.topLeft())
                                  
    list_select = window._data_context._bottom_contents
    
    # Set the combo box to "Wave Floating" anc click OK
    idx = list_select.comboBox.findText("Tidal Fixed",
                                        QtCore.Qt.MatchFixedString)
    list_select.comboBox.setCurrentIndex(idx)

    qtbot.mouseClick(
                list_select.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                QtCore.Qt.LeftButton)
    
    def check_status():
        
        # Pick up pipeline item again as it's been rebuilt
        test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
        
        assert test_var._status == "satisfied"
    
    qtbot.waitUntil(check_status)
    
    # Initiate the pipeline
    init_pipeline_button = \
        window.scenarioToolBar.widgetForAction(window.actionInitiate_Pipeline)
    qtbot.mouseClick(init_pipeline_button, QtCore.Qt.LeftButton)
    
    data_check = window._data_check
    
    def data_check_visible(): assert data_check.isVisible()
    
    qtbot.waitUntil(data_check_visible)
    
    qtbot.mouseClick(data_check.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                     QtCore.Qt.LeftButton)
    
    def check_dataflow(): assert window.actionInitiate_Dataflow.isEnabled()
    
    qtbot.waitUntil(check_dataflow)
    
    # Add a module
    add_modules_button = \
        window.simulationToolBar.widgetForAction(window.actionAdd_Modules)
    qtbot.mouseClick(add_modules_button, QtCore.Qt.LeftButton)
    
    module_shuttle = window._module_shuttle
    
    def add_modules_visible(): assert module_shuttle.isVisible()
    
    qtbot.waitUntil(add_modules_visible)
    
    # Fake click on last left item
    module_shuttle._left_index = module_shuttle._left_model.rowCount() - 1
    
    # Click "Add" then "OK"
    qtbot.mouseClick(module_shuttle.addButton,
                     QtCore.Qt.LeftButton)
    
    def module_on_right(): assert module_shuttle._get_right_data()
    
    qtbot.waitUntil(module_on_right)
    
    button = module_shuttle.buttonBox.button(QtGui.QDialogButtonBox.Ok)
    qtbot.mouseClick(button,
                     QtCore.Qt.LeftButton)
    
    def add_modules_not_visible(): assert not module_shuttle.isVisible()
    
    qtbot.waitUntil(add_modules_not_visible)
    
    # Initiate the dataflow
    init_pipeline_button = \
        window.scenarioToolBar.widgetForAction(window.actionInitiate_Dataflow)
    qtbot.mouseClick(init_pipeline_button, QtCore.Qt.LeftButton)
    
    qtbot.waitUntil(data_check_visible)
    
    qtbot.mouseClick(data_check.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                     QtCore.Qt.LeftButton)
    
    def check_run_current(): assert window.actionRun_Current.isEnabled()
    
    qtbot.waitUntil(check_run_current)
    
    def check_module_active():
        
        # Pick up pipeline item again as it's been rebuilt
        test_control = window._pipeline_dock._find_controller(
                                            controller_title="Mock Module")
        
        assert test_control is not None
    
    qtbot.waitUntil(check_module_active)
    
    # Add a strategy
    add_strategy_button = \
        window.simulationToolBar.widgetForAction(window.actionAdd_Strategy)
    qtbot.mouseClick(add_strategy_button, QtCore.Qt.LeftButton)
    
    strategy_manager = window._strategy_manager
    qtbot.addWidget(strategy_manager)
    
    def strategy_manager_visible(): assert strategy_manager.isVisible()
    
    qtbot.waitUntil(strategy_manager_visible)
    
    # Click on first strategy and apply
    item = strategy_manager.listWidget.item(0)
    rect = strategy_manager.listWidget.visualItemRect(item)
    qtbot.mouseClick(strategy_manager.listWidget.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.center())
    
    # Wait to register click
    qtbot.wait(200)
    
    qtbot.mouseClick(
            strategy_manager.buttonBox.button(QtGui.QDialogButtonBox.Apply),
            QtCore.Qt.LeftButton)
    
    assert str(strategy_manager.topDynamicLabel.text()) == str(item.text())


def test_strategy_save_close_open(qtbot, mocker, tmpdir, core):
    
    shell = Shell(core)
    
    # Add mock module
    socket = shell.core.control._sequencer.get_socket("ModuleInterface")
    socket.add_interface(MockModule)
    
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'warning',
                        return_value=QtGui.QMessageBox.Discard)
    
    dto_file_path = os.path.join(str(tmpdir), "test.dto")
    
    mocker.patch.object(QtGui.QFileDialog,
                        'getSaveFileName',
                        return_value=dto_file_path)
    
    mocker.patch.object(QtGui.QFileDialog,
                        'getOpenFileName',
                        return_value=dto_file_path)
    
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
        
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
    
    # obtain the rectangular coordinates of the child item
    tree_view = window._pipeline_dock.treeView
    index = test_var._get_index_from_address()
    proxy_index = test_var._proxy.mapFromSource(index)
    rect = tree_view.visualRect(proxy_index)
    
    # simulate the mouse click within the button coordinates
    qtbot.mouseClick(tree_view.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.topLeft())
                                  
    list_select = window._data_context._bottom_contents
    
    # Set the combo box to "Wave Floating" anc click OK
    idx = list_select.comboBox.findText("Tidal Fixed",
                                        QtCore.Qt.MatchFixedString)
    list_select.comboBox.setCurrentIndex(idx)

    qtbot.mouseClick(
                list_select.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                QtCore.Qt.LeftButton)
    
    def check_status():
        
        # Pick up pipeline item again as it's been rebuilt
        test_var = window._pipeline_dock._find_controller(
                                    controller_title="Device Technology Type",
                                    controller_class=InputVarControl)
        
        assert test_var._status == "satisfied"
    
    qtbot.waitUntil(check_status)
    
    # Initiate the pipeline
    init_pipeline_button = \
        window.scenarioToolBar.widgetForAction(window.actionInitiate_Pipeline)
    qtbot.mouseClick(init_pipeline_button, QtCore.Qt.LeftButton)
    
    data_check = window._data_check
    
    def data_check_visible(): assert data_check.isVisible()
    
    qtbot.waitUntil(data_check_visible)
    
    qtbot.mouseClick(data_check.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                     QtCore.Qt.LeftButton)
    
    def check_dataflow(): assert window.actionInitiate_Dataflow.isEnabled()
    
    qtbot.waitUntil(check_dataflow)
    
    # Add a module
    add_modules_button = \
        window.simulationToolBar.widgetForAction(window.actionAdd_Modules)
    qtbot.mouseClick(add_modules_button, QtCore.Qt.LeftButton)
    
    module_shuttle = window._module_shuttle
    
    def add_modules_visible(): assert module_shuttle.isVisible()
    
    qtbot.waitUntil(add_modules_visible)
    
    # Fake click on last left item
    module_shuttle._left_index = module_shuttle._left_model.rowCount() - 1
    
    # Click "Add" then "OK"
    qtbot.mouseClick(module_shuttle.addButton,
                     QtCore.Qt.LeftButton)
    
    def module_on_right(): assert module_shuttle._get_right_data()
    
    qtbot.waitUntil(module_on_right)
    
    button = module_shuttle.buttonBox.button(QtGui.QDialogButtonBox.Ok)
    qtbot.mouseClick(button,
                     QtCore.Qt.LeftButton)
    
    def add_modules_not_visible(): assert not module_shuttle.isVisible()
    
    qtbot.waitUntil(add_modules_not_visible)
    
    # Initiate the dataflow
    init_pipeline_button = \
        window.scenarioToolBar.widgetForAction(window.actionInitiate_Dataflow)
    qtbot.mouseClick(init_pipeline_button, QtCore.Qt.LeftButton)
    
    qtbot.waitUntil(data_check_visible)
    
    qtbot.mouseClick(data_check.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                     QtCore.Qt.LeftButton)
    
    def check_run_current(): assert window.actionRun_Current.isEnabled()
    
    qtbot.waitUntil(check_run_current)
    
    def check_module_active():
        
        # Pick up pipeline item again as it's been rebuilt
        test_control = window._pipeline_dock._find_controller(
                                            controller_title="Mock Module")
        
        assert test_control is not None
    
    qtbot.waitUntil(check_module_active)
    
    # Add a strategy
    add_strategy_button = \
        window.simulationToolBar.widgetForAction(window.actionAdd_Strategy)
    qtbot.mouseClick(add_strategy_button, QtCore.Qt.LeftButton)
    
    strategy_manager = window._strategy_manager
    
    def strategy_manager_visible(): assert strategy_manager.isVisible()
    
    qtbot.waitUntil(strategy_manager_visible)
    
    # Click on first strategy and apply
    item = strategy_manager.listWidget.item(0)
    rect = strategy_manager.listWidget.visualItemRect(item)
    qtbot.mouseClick(strategy_manager.listWidget.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.center())
    
    # Wait to register click
    qtbot.wait(200)
    
    qtbot.mouseClick(
            strategy_manager.buttonBox.button(QtGui.QDialogButtonBox.Apply),
            QtCore.Qt.LeftButton)
    
    assert str(strategy_manager.topDynamicLabel.text()) == str(item.text())
    
    # Close the dialog
    qtbot.mouseClick(
            strategy_manager.buttonBox.button(QtGui.QDialogButtonBox.Close),
            QtCore.Qt.LeftButton)
    
    # Save the simulation
    save_button = window.fileToolBar.widgetForAction(window.actionSave)
    qtbot.mouseClick(save_button, QtCore.Qt.LeftButton)
    
    def dto_file_saved():
         assert (len(os.listdir(str(tmpdir))) > 0 and
                 os.listdir(str(tmpdir))[0] == "test.dto")
    
    qtbot.waitUntil(dto_file_saved)
    
    # Close the project
    close_button = window.fileToolBar.widgetForAction(window.actionClose)
    qtbot.mouseClick(close_button, QtCore.Qt.LeftButton)
    
    def close_button_not_enabled(): assert not close_button.isEnabled()
    
    qtbot.waitUntil(close_button_not_enabled)
    
    # Open the project
    open_button = window.fileToolBar.widgetForAction(window.actionOpen)
    qtbot.mouseClick(open_button, QtCore.Qt.LeftButton)
    
    def close_button_enabled(): assert close_button.isEnabled()
    
    qtbot.waitUntil(close_button_enabled)
    
    # Reopen strategy manager and check value
    add_strategy_button = \
        window.simulationToolBar.widgetForAction(window.actionAdd_Strategy)
    qtbot.mouseClick(add_strategy_button, QtCore.Qt.LeftButton)
    
    strategy_manager = window._strategy_manager
    qtbot.addWidget(strategy_manager)
    
    def strategy_manager_visible(): assert strategy_manager.isVisible()
    
    qtbot.waitUntil(strategy_manager_visible)
    
    assert str(strategy_manager.topDynamicLabel.text()) == str(item.text())


def menu_click(qtbot, main_window, menu, action_name):
        
    qtbot.keyClick(main_window, menu.title().at(1).toLatin1(),
                   QtCore.Qt.AltModifier)
                
    for action in menu.actions():
        
        if not action.objectName(): continue
            
        if action.objectName() and action.objectName() == action_name:
            qtbot.keyClick(menu, QtCore.Qt.Key_Enter)
            return
        
        qtbot.wait(200)
        qtbot.keyClick(menu, QtCore.Qt.Key_Down)
        
    errStr = "Action '{}' not found in menu '{}'".format(action_name,
                                                         menu.objectName())
    raise ValueError(errStr)

