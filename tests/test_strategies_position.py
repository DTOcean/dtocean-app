# -*- coding: utf-8 -*-

#    Copyright (C) 2021 Mathew Topper
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


import pytest

pytest.importorskip("dtocean_hydro")

from dtocean_app.core import GUICore
from dtocean_app.main import Shell
from dtocean_app.strategies.position import AdvancedPositionWidget
from dtocean_core.interfaces import ModuleInterface
from dtocean_core.menu import ModuleMenu, ProjectMenu
from dtocean_core.pipeline import Tree



class MockModule(ModuleInterface):
    
    @classmethod
    def get_name(cls):
        
        return "Mock Module"
    
    @classmethod
    def declare_weight(cls):
        
        return 998
    
    @classmethod
    def declare_inputs(cls):
        
        input_list = ["device.turbine_performance",
                      "device.cut_in_velocity",
                      "device.system_type"]
        
        return input_list
    
    @classmethod
    def declare_outputs(cls):
        
        output_list = None
        
        return output_list
    
    @classmethod
    def declare_optional(cls):
        
        return None
    
    @classmethod
    def declare_id_map(self):
        
        id_map = {"dummy1": "device.turbine_performance",
                  "dummy2": "device.cut_in_velocity",
                  "dummy3": "device.system_type"}
        
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


@pytest.fixture
def project(core):
    
    project_title = "Test"
    
    project_menu = ProjectMenu()
    var_tree = Tree()
    
    project = project_menu.new_project(core, project_title)
    
    options_branch = var_tree.get_branch(core,
                                         project,
                                         "System Type Selection")
    device_type = options_branch.get_input_variable(core,
                                                    project,
                                                    "device.system_type")
    device_type.set_raw_interface(core, "Tidal Fixed")
    device_type.read(core, project)
    
    project_menu.initiate_pipeline(core, project)
    
    return project


@pytest.fixture
def mock_shell(core, project):
    
    module_menu = ModuleMenu()
    
    socket = core.control._sequencer.get_socket("ModuleInterface")
    socket.add_interface(MockModule)
    module_menu.activate(core, project, MockModule.get_name())
    
    shell = Shell(core)
    shell.project = project
    
    return shell


@pytest.fixture
def hydro_shell(core, project):
    
    module_menu = ModuleMenu()
    module_menu.activate(core, project, "Hydrodynamics")
    
    shell = Shell(core)
    shell.project = project
    
    return shell


def test_AdvancedPositionWidget_bad_status(qtbot, mock_shell):
    
    window = AdvancedPositionWidget(None, mock_shell, {})
    window.show()
    qtbot.addWidget(window)
    
    assert not window.tabWidget.isTabEnabled(1)
    assert not window.tabWidget.isTabEnabled(2)
    assert not window.tabWidget.isTabEnabled(3)
    assert not window.tabWidget.isTabEnabled(4)


def test_AdvancedPositionWidget_settings_open(qtbot, tmp_path, hydro_shell):
    
    window = AdvancedPositionWidget(None, hydro_shell, {})
    window.show()
    qtbot.addWidget(window)
    
    window.workDirLineEdit.insert(str(tmp_path))
    window.workDirLineEdit.returnPressed.emit()
    
    def settings_tab_enabled(): assert  window.tabWidget.isTabEnabled(1)
    
    qtbot.waitUntil(settings_tab_enabled)
    
    assert window.tabWidget.isTabEnabled(1)
    assert window.tabWidget.isTabEnabled(2)


def test_AdvancedPositionWidget_fixed_combo_slot_uncheck(qtbot,
                                                         tmp_path,
                                                         hydro_shell):
    
    window = AdvancedPositionWidget(None, hydro_shell, {})
    window.show()
    qtbot.addWidget(window)
    
    window.workDirLineEdit.insert(str(tmp_path))
    window.workDirLineEdit.returnPressed.emit()
    
    def settings_tab_enabled(): assert  window.tabWidget.isTabEnabled(1)
    
    qtbot.waitUntil(settings_tab_enabled)
    
    delta_row = window._param_boxes["delta_row"]
    delta_row["fixed.check"].toggle()
    
    def range_group_disabled():
        assert not delta_row["range.group"].isEnabled()
    
    qtbot.waitUntil(range_group_disabled)
    
    assert window._config["parameters"]["delta_row"] == {"fixed": 0.0}


def test_AdvancedPositionWidget_fixed_combo_slot_check(qtbot,
                                                       tmp_path,
                                                       hydro_shell):
    
    window = AdvancedPositionWidget(None, hydro_shell, {})
    window.show()
    qtbot.addWidget(window)
    
    window.workDirLineEdit.insert(str(tmp_path))
    window.workDirLineEdit.returnPressed.emit()
    
    def settings_tab_enabled(): assert  window.tabWidget.isTabEnabled(1)
    
    qtbot.waitUntil(settings_tab_enabled)
    
    delta_row = window._param_boxes["delta_row"]
    delta_row["fixed.check"].toggle()
    
    def range_group_disabled():
        assert not delta_row["range.group"].isEnabled()
    
    qtbot.waitUntil(range_group_disabled)
    
    delta_row["fixed.check"].toggle()
    
    def range_group_enabled():
        assert delta_row["range.group"].isEnabled()
    
    qtbot.waitUntil(range_group_enabled)
    
    assert window._config["parameters"]["delta_row"].keys() == ["range"]


def test_AdvancedPositionWidget_fixed_value_slot(qtbot,
                                                 tmp_path,
                                                 hydro_shell):
    
    window = AdvancedPositionWidget(None, hydro_shell, {})
    window.show()
    qtbot.addWidget(window)
    
    window.workDirLineEdit.insert(str(tmp_path))
    window.workDirLineEdit.returnPressed.emit()
    
    def settings_tab_enabled(): assert  window.tabWidget.isTabEnabled(1)
    
    qtbot.waitUntil(settings_tab_enabled)
    
    delta_row = window._param_boxes["delta_row"]
    delta_row["fixed.check"].toggle()
    
    def range_group_disabled():
        assert not delta_row["range.group"].isEnabled()
    
    qtbot.waitUntil(range_group_disabled)
    
    delta_row["fixed.box"].setValue(1)
    
    assert window._config["parameters"]["delta_row"] == {"fixed": 1.0}


def test_AdvancedPositionWidget_range_type_slot_multiplier(qtbot,
                                                           tmp_path,
                                                           hydro_shell):
    
    window = AdvancedPositionWidget(None, hydro_shell, {})
    window.show()
    qtbot.addWidget(window)
    
    window.workDirLineEdit.insert(str(tmp_path))
    window.workDirLineEdit.returnPressed.emit()
    
    def settings_tab_enabled(): assert window.tabWidget.isTabEnabled(1)
    
    qtbot.waitUntil(settings_tab_enabled)
    
    delta_row = window._param_boxes["delta_row"]
    delta_row["range.box.type"].setCurrentIndex(1)
    
    def range_box_var_enabled(): assert delta_row["range.box.var"].isEnabled()
    
    qtbot.waitUntil(range_box_var_enabled)
    
    assert window._config[
                "parameters"]["delta_row"]["range"]["type"] == "multiplier"


def test_AdvancedPositionWidget_range_type_slot_fixed(qtbot,
                                                      tmp_path,
                                                      hydro_shell):
    
    window = AdvancedPositionWidget(None, hydro_shell, {})
    window.show()
    qtbot.addWidget(window)
    
    window.workDirLineEdit.insert(str(tmp_path))
    window.workDirLineEdit.returnPressed.emit()
    
    def settings_tab_enabled(): assert window.tabWidget.isTabEnabled(1)
    
    qtbot.waitUntil(settings_tab_enabled)
    
    delta_row = window._param_boxes["delta_row"]
    delta_row["range.box.type"].setCurrentIndex(1)
    
    def range_box_var_enabled(): assert delta_row["range.box.var"].isEnabled()
    
    qtbot.waitUntil(range_box_var_enabled)
    
    delta_row["range.box.type"].setCurrentIndex(0)
    
    def range_box_var_disabled():
        assert not delta_row["range.box.var"].isEnabled()
    
    qtbot.waitUntil(range_box_var_disabled)
    
    assert window._config[
                "parameters"]["delta_row"]["range"]["type"] == "fixed"



def test_AdvancedPositionWidget_generic_range_slot(qtbot,
                                                   tmp_path,
                                                   hydro_shell):
    
    window = AdvancedPositionWidget(None, hydro_shell, {})
    window.show()
    qtbot.addWidget(window)
    
    window.workDirLineEdit.insert(str(tmp_path))
    window.workDirLineEdit.returnPressed.emit()
    
    def settings_tab_enabled(): assert window.tabWidget.isTabEnabled(1)
    
    qtbot.waitUntil(settings_tab_enabled)
    
    delta_row = window._param_boxes["delta_row"]
    delta_row["range.box.max"].setValue(2)
    
    assert window._config["parameters"]["delta_row"]["range"]["max"] == 2
