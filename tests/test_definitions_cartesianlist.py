
import numpy as np

from attrdict import AttrDict
from dtocean_app.data.definitions import (CartesianList,
                                          CartesianListColumn)

def setup_none(structure):

    structure.parent = None
    structure.meta = AttrDict({'result': AttrDict({"identifier": "test",
                                                   "structure": "test",
                                                   "title": "test"})}) 
    
    structure.data = AttrDict({'result': None})
    
    return

 
def setup_data(structure):

    structure.parent = None
    structure.meta = AttrDict({'result': AttrDict({"identifier": "test",
                                                   "structure": "test",
                                                   "title": "test"})}) 
    
    test_data = np.array([(0, 1),
                          (1, 2)])
    structure.data = AttrDict({'result': test_data})
    
    return


def test_CartesianList_input(qtbot):
    
    test = CartesianList()
    setup_data(test)

    test.auto_input(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_CartesianList_input_none(qtbot):
    
    test = CartesianList()
    setup_none(test)
    
    test.auto_input(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_CartesianList_output(qtbot):
    
    test = CartesianList()
    setup_data(test)
    
    test.auto_output(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_CartesianList_output_none(qtbot):
    
    test = CartesianList()
    setup_none(test)

    test.auto_output(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_CartesianListColumn_input(qtbot):
    
    test = CartesianListColumn()
    setup_data(test)

    test.auto_input(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_CartesianListColumn_input_none(qtbot):
    
    test = CartesianListColumn()
    setup_none(test)
    
    test.auto_input(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_CartesianListColumn_output(qtbot):
    
    test = CartesianListColumn()
    setup_data(test)
    
    test.auto_output(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_CartesianListColumn_output_none(qtbot):
    
    test = CartesianListColumn()
    setup_none(test)

    test.auto_output(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
