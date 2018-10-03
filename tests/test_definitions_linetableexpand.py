
import pandas as pd
from attrdict import AttrDict

from dtocean_app.data.definitions import LineTableExpand


def setup_none(structure):

    structure.parent = None
    structure.meta = AttrDict({'result': AttrDict({"identifier": "test",
                                                   "structure": "test",
                                                   "title": "test",
                                                   "labels": ["Velocity",
                                                              "Drag 1"],
                                                   "units": ["a", "b"],
                                                   "valid_values": None})})
    
    structure.data = AttrDict({'result': None})
    
    return

 
def setup_data(structure):

    structure.parent = None
    structure.meta = AttrDict({'result': AttrDict({"identifier": "test",
                                                   "structure": "test",
                                                   "title": "test",
                                                   "labels": ["Velocity",
                                                              "Drag"],
                                                   "units": ["a", "b"],
                                                   "valid_values": None})})
    
    velocity = [float(x) for x in range(10)]
    drag1 = [2 * float(x) for x in range(10)]
    drag2 = [3 * float(x) for x in range(10)]
    
    raw = {"Velocity": velocity,
           "Drag 1": drag1,
           "Drag 2": drag2}
    df = pd.DataFrame(raw)
    
    structure.data = AttrDict({'result': df})
    
    return


def setup_data_one_unit(structure):

    structure.parent = None
    structure.meta = AttrDict({'result': AttrDict({"identifier": "test",
                                                   "structure": "test",
                                                   "title": "test",
                                                   "labels": ["Velocity",
                                                              "Drag"],
                                                   "units": ["a"],
                                                   "valid_values": None})})
    
    velocity = [float(x) for x in range(10)]
    drag1 = [2 * float(x) for x in range(10)]
    drag2 = [3 * float(x) for x in range(10)]
    
    raw = {"Velocity": velocity,
           "Drag 1": drag1,
           "Drag 2": drag2}
    df = pd.DataFrame(raw)
    
    structure.data = AttrDict({'result': df})
    
    return


def setup_data_no_unit(structure):

    structure.parent = None
    structure.meta = AttrDict({'result': AttrDict({"identifier": "test",
                                                   "structure": "test",
                                                   "title": "test",
                                                   "labels": ["Velocity",
                                                              "Drag"],
                                                   "units": None,
                                                   "valid_values": None})})
    
    velocity = [float(x) for x in range(10)]
    drag1 = [2 * float(x) for x in range(10)]
    drag2 = [3 * float(x) for x in range(10)]
    
    raw = {"Velocity": velocity,
           "Drag 1": drag1,
           "Drag 2": drag2}
    df = pd.DataFrame(raw)
    
    structure.data = AttrDict({'result': df})
    
    return


def test_LineTableExpand_input(qtbot):
    
    test = LineTableExpand()
    setup_data(test)

    test.auto_input(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_LineTableExpand_input_none(qtbot):
    
    test = LineTableExpand()
    setup_none(test)
    
    test.auto_input(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_LineTableExpand_input_one_unit(qtbot):
    
    test = LineTableExpand()
    setup_data_one_unit(test)
    
    test.auto_input(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_LineTableExpand_input_no_unit(qtbot):
    
    test = LineTableExpand()
    setup_data_no_unit(test)
    
    test.auto_input(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_LineTableExpand_output(qtbot):
    
    test = LineTableExpand()
    setup_data(test)
    
    test.auto_output(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_LineTableExpand_output_none(qtbot):
    
    test = LineTableExpand()
    setup_none(test)

    test.auto_output(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_LineTableExpand_output_one_unit(qtbot):
    
    test = LineTableExpand()
    setup_data_one_unit(test)
    
    test.auto_output(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_LineTableExpand_output_no_unit(qtbot):
    
    test = LineTableExpand()
    setup_data_no_unit(test)
    
    test.auto_output(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
