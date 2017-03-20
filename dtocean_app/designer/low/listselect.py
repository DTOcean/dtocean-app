# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\low\listselect.ui'
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

class Ui_ListSelect(object):
    def setupUi(self, ListSelect):
        ListSelect.setObjectName(_fromUtf8("ListSelect"))
        ListSelect.resize(745, 211)
        self.verticalLayout = QtGui.QVBoxLayout(ListSelect)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.questionLabel = QtGui.QLabel(ListSelect)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.questionLabel.sizePolicy().hasHeightForWidth())
        self.questionLabel.setSizePolicy(sizePolicy)
        self.questionLabel.setMinimumSize(QtCore.QSize(200, 0))
        self.questionLabel.setScaledContents(False)
        self.questionLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.questionLabel.setWordWrap(True)
        self.questionLabel.setObjectName(_fromUtf8("questionLabel"))
        self.gridLayout.addWidget(self.questionLabel, 1, 0, 1, 2)
        self.comboBox = QtGui.QComboBox(ListSelect)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 1, 2, 1, 1)
        self.valueLabel = QtGui.QLabel(ListSelect)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.valueLabel.sizePolicy().hasHeightForWidth())
        self.valueLabel.setSizePolicy(sizePolicy)
        self.valueLabel.setObjectName(_fromUtf8("valueLabel"))
        self.gridLayout.addWidget(self.valueLabel, 0, 2, 1, 1)
        self.staticLabel = QtGui.QLabel(ListSelect)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.staticLabel.sizePolicy().hasHeightForWidth())
        self.staticLabel.setSizePolicy(sizePolicy)
        self.staticLabel.setMinimumSize(QtCore.QSize(200, 0))
        self.staticLabel.setObjectName(_fromUtf8("staticLabel"))
        self.gridLayout.addWidget(self.staticLabel, 0, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 97, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(ListSelect)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ListSelect)
        QtCore.QMetaObject.connectSlotsByName(ListSelect)

    def retranslateUi(self, ListSelect):
        ListSelect.setWindowTitle(_translate("ListSelect", "Form", None))
        self.questionLabel.setText(_translate("ListSelect", "Select a new value from the list:", None))
        self.valueLabel.setText(_translate("ListSelect", "None", None))
        self.staticLabel.setText(_translate("ListSelect", "Current value:", None))

