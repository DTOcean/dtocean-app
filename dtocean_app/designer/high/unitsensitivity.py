# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\high\unitsensitivity.ui'
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

class Ui_UnitSensitivityWidget(object):
    def setupUi(self, UnitSensitivityWidget):
        UnitSensitivityWidget.setObjectName(_fromUtf8("UnitSensitivityWidget"))
        UnitSensitivityWidget.resize(600, 450)
        self.verticalLayout = QtGui.QVBoxLayout(UnitSensitivityWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(UnitSensitivityWidget)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(UnitSensitivityWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.modBox = QtGui.QComboBox(UnitSensitivityWidget)
        self.modBox.setObjectName(_fromUtf8("modBox"))
        self.gridLayout.addWidget(self.modBox, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(UnitSensitivityWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.varBox = QtGui.QComboBox(UnitSensitivityWidget)
        self.varBox.setObjectName(_fromUtf8("varBox"))
        self.gridLayout.addWidget(self.varBox, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(UnitSensitivityWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(UnitSensitivityWidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 277, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(UnitSensitivityWidget)
        QtCore.QMetaObject.connectSlotsByName(UnitSensitivityWidget)

    def retranslateUi(self, UnitSensitivityWidget):
        UnitSensitivityWidget.setWindowTitle(_translate("UnitSensitivityWidget", "Form", None))
        self.label_2.setText(_translate("UnitSensitivityWidget", "Select a variable from a module to vary. The range of values must be supplied using commas to separate them.", None))
        self.label.setText(_translate("UnitSensitivityWidget", "Module: ", None))
        self.label_3.setText(_translate("UnitSensitivityWidget", "Variable: ", None))
        self.label_4.setText(_translate("UnitSensitivityWidget", "Values: ", None))

