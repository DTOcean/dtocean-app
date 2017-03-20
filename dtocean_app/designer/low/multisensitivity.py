# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\low\multisensitivity.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MultiSensitivityWidget(object):
    def setupUi(self, MultiSensitivityWidget):
        MultiSensitivityWidget.setObjectName(_fromUtf8("MultiSensitivityWidget"))
        MultiSensitivityWidget.resize(600, 450)
        self.verticalLayout = QtGui.QVBoxLayout(MultiSensitivityWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.instructionsLabel = QtGui.QLabel(MultiSensitivityWidget)
        self.instructionsLabel.setWordWrap(True)
        self.instructionsLabel.setObjectName(_fromUtf8("instructionsLabel"))
        self.verticalLayout.addWidget(self.instructionsLabel)
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.modLabel = QtGui.QLabel(MultiSensitivityWidget)
        self.modLabel.setObjectName(_fromUtf8("modLabel"))
        self.gridLayout.addWidget(self.modLabel, 0, 0, 1, 1)
        self.modBox = QtGui.QComboBox(MultiSensitivityWidget)
        self.modBox.setObjectName(_fromUtf8("modBox"))
        self.gridLayout.addWidget(self.modBox, 0, 1, 1, 1)
        self.varLabel = QtGui.QLabel(MultiSensitivityWidget)
        self.varLabel.setObjectName(_fromUtf8("varLabel"))
        self.gridLayout.addWidget(self.varLabel, 1, 0, 1, 1)
        self.varBox = QtGui.QComboBox(MultiSensitivityWidget)
        self.varBox.setObjectName(_fromUtf8("varBox"))
        self.gridLayout.addWidget(self.varBox, 1, 1, 1, 1)
        self.lineLabel = QtGui.QLabel(MultiSensitivityWidget)
        self.lineLabel.setObjectName(_fromUtf8("lineLabel"))
        self.gridLayout.addWidget(self.lineLabel, 2, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(MultiSensitivityWidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line = QtGui.QFrame(MultiSensitivityWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.tableLabel = QtGui.QLabel(MultiSensitivityWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tableLabel.setFont(font)
        self.tableLabel.setObjectName(_fromUtf8("tableLabel"))
        self.verticalLayout.addWidget(self.tableLabel)
        self.tableView = QtGui.QTableView(MultiSensitivityWidget)
        self.tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.tableView.horizontalHeader().setDefaultSectionSize(150)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableView)
        self.line_2 = QtGui.QFrame(MultiSensitivityWidget)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.addButton = QtGui.QPushButton(MultiSensitivityWidget)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.horizontalLayout.addWidget(self.addButton)
        self.removeButton = QtGui.QPushButton(MultiSensitivityWidget)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.horizontalLayout.addWidget(self.removeButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.subsetLabel = QtGui.QLabel(MultiSensitivityWidget)
        self.subsetLabel.setObjectName(_fromUtf8("subsetLabel"))
        self.horizontalLayout.addWidget(self.subsetLabel)
        self.subsetSpinBox = QtGui.QDoubleSpinBox(MultiSensitivityWidget)
        self.subsetSpinBox.setMaximum(100.0)
        self.subsetSpinBox.setSingleStep(5.0)
        self.subsetSpinBox.setProperty("value", 100.0)
        self.subsetSpinBox.setObjectName(_fromUtf8("subsetSpinBox"))
        self.horizontalLayout.addWidget(self.subsetSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem2 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.infoLabel = QtGui.QLabel(MultiSensitivityWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.infoLabel.setFont(font)
        self.infoLabel.setObjectName(_fromUtf8("infoLabel"))
        self.verticalLayout.addWidget(self.infoLabel)

        self.retranslateUi(MultiSensitivityWidget)
        QtCore.QMetaObject.connectSlotsByName(MultiSensitivityWidget)

    def retranslateUi(self, MultiSensitivityWidget):
        MultiSensitivityWidget.setWindowTitle(_translate("MultiSensitivityWidget", "Form", None))
        self.instructionsLabel.setText(_translate("MultiSensitivityWidget", "Select a variable from a module to vary, and click the Add button to include it in the search space. The range of values must be supplied using commas to separate them.", None))
        self.modLabel.setText(_translate("MultiSensitivityWidget", "Module: ", None))
        self.varLabel.setText(_translate("MultiSensitivityWidget", "Variable: ", None))
        self.lineLabel.setText(_translate("MultiSensitivityWidget", "Values: ", None))
        self.tableLabel.setText(_translate("MultiSensitivityWidget", "Chosen variable ranges:", None))
        self.addButton.setText(_translate("MultiSensitivityWidget", "Add", None))
        self.removeButton.setText(_translate("MultiSensitivityWidget", "Remove", None))
        self.subsetLabel.setText(_translate("MultiSensitivityWidget", "Subset percentage:", None))
        self.infoLabel.setText(_translate("MultiSensitivityWidget", "TextLabel", None))

