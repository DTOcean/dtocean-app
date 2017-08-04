
from attrdict import AttrDict
from dtocean_app.data.definitions import (SimpleList,
                                          SimpleListColumn)


def setup_none(structure):

    structure.parent = None
    structure.meta = AttrDict({'result': AttrDict({"identifier": "test",
                                                   "structure": "test",
                                                   "title": "test",
                                                   "types": ["str"],
                                                   "units": None})})
    
    structure.data = AttrDict({'result': None})
    
    return

 
def setup_data(structure):

    structure.parent = None
    structure.meta = AttrDict({'result': AttrDict({"identifier": "test",
                                                   "structure": "test",
                                                   "title": "test",
                                                   "types": ["str"],
                                                   "units": None})})
    
    test_data = ["a", "b", "c"]
    structure.data = AttrDict({'result': test_data})
    
    return


def setup_data_units(structure):

    structure.parent = None
    structure.meta = AttrDict({'result': AttrDict({"identifier": "test",
                                                   "structure": "test",
                                                   "title": "test",
                                                   "types": ["str"],
                                                   "units": ["m"]})})
    
    test_data = ["a", "b", "c"]
    structure.data = AttrDict({'result': test_data})
    
    return
    
    
def test_SimpleList_output(qtbot):
    
    test = SimpleList()
    setup_data(test)
    
    test.auto_output(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_SimpleList_output_units(qtbot):
    
    test = SimpleList()
    setup_data_units(test)
    
    test.auto_output(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_SimpleList_output_none(qtbot):
    
    test = SimpleList()
    setup_none(test)

    test.auto_output(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_SimpleListColumn_output(qtbot):
    
    test = SimpleListColumn()
    setup_data(test)
    
    test.auto_output(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
    
    
def test_SimpleListColumn_output_none(qtbot):
    
    test = SimpleListColumn()
    setup_none(test)

    test.auto_output(test)
    widget = test.data.result
    
    widget.show()
    qtbot.addWidget(widget)
    
    assert True
