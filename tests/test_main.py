# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:16:37 2017

@author: mtopper
"""

import os

from PyQt4 import QtCore, QtGui

from dtocean_app.main import DTOceanWindow, Shell
from dtocean_app.pipeline import InputVarItem
from dtocean_app.widgets.input import ListSelect


def test_open_dtocean_window(qtbot, mocker):
        
    shell = Shell()
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
    
    assert window.windowTitle() == "DTOcean"


def test_new_project(qtbot, mocker):
    
    shell = Shell()
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
    test_var = window._pipeline_dock._find_item("Device Technology Type",
                                                InputVarItem)
    
    assert test_var._id == "device.system_type"


def test_set_device_type(qtbot, mocker):
    
    shell = Shell()
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
    test_var = window._pipeline_dock._find_item("Device Technology Type",
                                                InputVarItem)
    
    # obtain the rectangular coordinates of the child item
    tree_widget = window._pipeline_dock.treeWidget
    rect = tree_widget.visualItemRect(test_var)
    
    # simulate the mouse click within the button coordinates    
    qtbot.mouseClick(tree_widget.viewport(),
                     QtCore.Qt.LeftButton,
                     pos=rect.topLeft())
    
    assert tree_widget.currentItem() == test_var
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
        test_var = window._pipeline_dock._find_item("Device Technology Type",
                                                    InputVarItem)
        
        assert test_var._status == "satisfied"
    
    qtbot.waitUntil(check_status)
    
    assert True


def test_initiate_pipeline(qtbot, mocker):
    
    shell = Shell()
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
    test_var = window._pipeline_dock._find_item("Device Technology Type",
                                                InputVarItem)
    
    # obtain the rectangular coordinates of the child item
    tree_widget = window._pipeline_dock.treeWidget
    rect = tree_widget.visualItemRect(test_var)
    
    # simulate the mouse click within the button coordinates    
    qtbot.mouseClick(tree_widget.viewport(),
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
        test_var = window._pipeline_dock._find_item("Device Technology Type",
                                                    InputVarItem)
        
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


def test_export_data(qtbot, mocker, tmpdir):

    # File path
    datastate_file_name = "my_datastate.dts"
    datastate_file_path = os.path.join(str(tmpdir), datastate_file_name)
    
    mocker.patch.object(QtGui.QMessageBox,
                        'question',
                        return_value=QtGui.QMessageBox.Yes)
                      
    mocker.patch.object(QtGui.QFileDialog,
                        'getSaveFileName',
                        return_value=datastate_file_path)
    
    shell = Shell()
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
                      
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
        
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_item("Device Technology Type",
                                                InputVarItem)
    
    # obtain the rectangular coordinates of the child item
    tree_widget = window._pipeline_dock.treeWidget
    rect = tree_widget.visualItemRect(test_var)
    
    # simulate the mouse click within the button coordinates    
    qtbot.mouseClick(tree_widget.viewport(),
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
        test_var = window._pipeline_dock._find_item("Device Technology Type",
                                                    InputVarItem)
        
        assert test_var._status == "satisfied"
    
    qtbot.waitUntil(check_status)
    
    # Export data
    menu_click(qtbot,
               window,
               window.menuData,
               "actionExport")
        
    assert os.path.isfile(datastate_file_path)
    
    
def test_import_data(qtbot, mocker, tmpdir):

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
    
    shell = Shell()
    window = DTOceanWindow(shell)
    window.show()
    qtbot.addWidget(window)
                      
    # Get the new project button and click it
    new_project_button = window.fileToolBar.widgetForAction(window.actionNew)
    qtbot.mouseClick(new_project_button, QtCore.Qt.LeftButton)
        
    # Pick up the available pipeline item
    test_var = window._pipeline_dock._find_item("Device Technology Type",
                                                InputVarItem)
    
    # obtain the rectangular coordinates of the child item
    tree_widget = window._pipeline_dock.treeWidget
    rect = tree_widget.visualItemRect(test_var)
    
    # simulate the mouse click within the button coordinates    
    qtbot.mouseClick(tree_widget.viewport(),
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
        test_var = window._pipeline_dock._find_item("Device Technology Type",
                                                    InputVarItem)
        
        assert test_var._status == "satisfied"
    
    qtbot.waitUntil(check_status)
    
    # Export data
    menu_click(qtbot,
               window,
               window.menuData,
               "actionExport")
        
    assert os.path.isfile(datastate_file_path)
    
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
    
    
def test_initiate_dataflow(qtbot, mocker):
    
    shell = Shell()
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
    test_var = window._pipeline_dock._find_item("Device Technology Type",
                                                InputVarItem)
    
    # obtain the rectangular coordinates of the child item
    tree_widget = window._pipeline_dock.treeWidget
    rect = tree_widget.visualItemRect(test_var)
    
    # simulate the mouse click within the button coordinates    
    qtbot.mouseClick(tree_widget.viewport(),
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
        test_var = window._pipeline_dock._find_item("Device Technology Type",
                                                    InputVarItem)
        
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
    
    # Fake click on left item
    module_shuttle._left_index = 0
    
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
        test_item = window._pipeline_dock._find_item("Hydrodynamics")
        
        assert test_item is not None
    
    qtbot.waitUntil(check_module_active)
    
    assert True


def test_set_simulation_title(qtbot, mocker):
    
    shell = Shell()
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
    test_var = window._pipeline_dock._find_item("Device Technology Type",
                                                InputVarItem)
    
    # obtain the rectangular coordinates of the child item
    tree_widget = window._pipeline_dock.treeWidget
    rect = tree_widget.visualItemRect(test_var)
    
    # simulate the mouse click within the button coordinates    
    qtbot.mouseClick(tree_widget.viewport(),
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
        test_var = window._pipeline_dock._find_item("Device Technology Type",
                                                    InputVarItem)
        
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
    
    # Fake click on left item
    module_shuttle._left_index = 0
    
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
        test_item = window._pipeline_dock._find_item("Hydrodynamics")
        
        assert test_item is not None
    
    qtbot.waitUntil(check_module_active)
        
    # Close the pipeline
    window._pipeline_dock.close()
    
    def pipeline_not_visible(): assert not window._pipeline_dock.isVisible()
    
    qtbot.waitUntil(pipeline_not_visible)
    
    # Fake change of simulation name
    editor = mocker.Mock()
    editor.text.return_value = "bob"
    
    window._simulation_dock._catch_edit(editor, None)
    
    def check_name():
    
        # Pick up the default simulation
        test_sim = window._simulation_dock.listWidget.item(0)
        
        assert test_sim._title == "bob"
    
    qtbot.waitUntil(check_name)
    
    assert shell.project.get_simulation_title() == "bob"


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
