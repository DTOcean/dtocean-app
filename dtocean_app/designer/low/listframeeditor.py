# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\low\listframeeditor.ui'
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

class Ui_ListFrameEditor(object):
    def setupUi(self, ListFrameEditor):
        ListFrameEditor.setObjectName(_fromUtf8("ListFrameEditor"))
        ListFrameEditor.resize(920, 636)
        self.verticalLayout = QtGui.QVBoxLayout(ListFrameEditor)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.topStaticLabel = QtGui.QLabel(ListFrameEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topStaticLabel.sizePolicy().hasHeightForWidth())
        self.topStaticLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.topStaticLabel.setFont(font)
        self.topStaticLabel.setObjectName(_fromUtf8("topStaticLabel"))
        self.horizontalLayout.addWidget(self.topStaticLabel)
        self.topDynamicLabel = QtGui.QLabel(ListFrameEditor)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.topDynamicLabel.setFont(font)
        self.topDynamicLabel.setObjectName(_fromUtf8("topDynamicLabel"))
        self.horizontalLayout.addWidget(self.topDynamicLabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtGui.QFrame(ListFrameEditor)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        spacerItem = QtGui.QSpacerItem(20, 15, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSpacing(20)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.listLabel = QtGui.QLabel(ListFrameEditor)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.listLabel.setFont(font)
        self.listLabel.setObjectName(_fromUtf8("listLabel"))
        self.gridLayout.addWidget(self.listLabel, 0, 0, 1, 1)
        self.mainLabel = QtGui.QLabel(ListFrameEditor)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.mainLabel.setFont(font)
        self.mainLabel.setObjectName(_fromUtf8("mainLabel"))
        self.gridLayout.addWidget(self.mainLabel, 0, 1, 1, 1)
        self.listWidget = QtGui.QListWidget(ListFrameEditor)
        self.listWidget.setMaximumSize(QtCore.QSize(250, 16777215))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 1)
        self.mainFrame = QtGui.QFrame(ListFrameEditor)
        self.mainFrame.setFrameShape(QtGui.QFrame.Panel)
        self.mainFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.mainFrame.setObjectName(_fromUtf8("mainFrame"))
        self.gridLayout.addWidget(self.mainFrame, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 15, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.buttonBox = QtGui.QDialogButtonBox(ListFrameEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ListFrameEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ListFrameEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ListFrameEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(ListFrameEditor)

    def retranslateUi(self, ListFrameEditor):
        ListFrameEditor.setWindowTitle(_translate("ListFrameEditor", "Dialog", None))
        self.topStaticLabel.setText(_translate("ListFrameEditor", "TextLabel", None))
        self.topDynamicLabel.setText(_translate("ListFrameEditor", "TextLabel", None))
        self.listLabel.setText(_translate("ListFrameEditor", "Some text:", None))
        self.mainLabel.setText(_translate("ListFrameEditor", "Some more text:", None))

