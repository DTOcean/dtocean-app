# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\high\filemanager.ui'
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

class Ui_FileManagerWidget(object):
    def setupUi(self, FileManagerWidget):
        FileManagerWidget.setObjectName(_fromUtf8("FileManagerWidget"))
        FileManagerWidget.resize(425, 232)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FileManagerWidget.sizePolicy().hasHeightForWidth())
        FileManagerWidget.setSizePolicy(sizePolicy)
        FileManagerWidget.setMinimumSize(QtCore.QSize(425, 0))
        self.verticalLayout = QtGui.QVBoxLayout(FileManagerWidget)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.headingLabel = QtGui.QLabel(FileManagerWidget)
        self.headingLabel.setTextFormat(QtCore.Qt.RichText)
        self.headingLabel.setObjectName(_fromUtf8("headingLabel"))
        self.verticalLayout.addWidget(self.headingLabel)
        self.line = QtGui.QFrame(FileManagerWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(FileManagerWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(85, 0))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.loadButton = QtGui.QRadioButton(FileManagerWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadButton.sizePolicy().hasHeightForWidth())
        self.loadButton.setSizePolicy(sizePolicy)
        self.loadButton.setMinimumSize(QtCore.QSize(80, 0))
        self.loadButton.setObjectName(_fromUtf8("loadButton"))
        self.modeButtonGroup = QtGui.QButtonGroup(FileManagerWidget)
        self.modeButtonGroup.setObjectName(_fromUtf8("modeButtonGroup"))
        self.modeButtonGroup.addButton(self.loadButton)
        self.horizontalLayout.addWidget(self.loadButton)
        self.saveButton = QtGui.QRadioButton(FileManagerWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setMinimumSize(QtCore.QSize(80, 0))
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.modeButtonGroup.addButton(self.saveButton)
        self.horizontalLayout.addWidget(self.saveButton)
        spacerItem = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(FileManagerWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(75, 0))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.extBox = QtGui.QComboBox(FileManagerWidget)
        self.extBox.setMinimumSize(QtCore.QSize(75, 0))
        self.extBox.setObjectName(_fromUtf8("extBox"))
        self.horizontalLayout.addWidget(self.extBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 4, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(FileManagerWidget)
        self.label_2.setMinimumSize(QtCore.QSize(65, 0))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.pathEdit = QtGui.QLineEdit(FileManagerWidget)
        self.pathEdit.setObjectName(_fromUtf8("pathEdit"))
        self.horizontalLayout_2.addWidget(self.pathEdit)
        self.getPathButton = QtGui.QToolButton(FileManagerWidget)
        self.getPathButton.setObjectName(_fromUtf8("getPathButton"))
        self.horizontalLayout_2.addWidget(self.getPathButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtGui.QSpacerItem(20, 80, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.buttonBox = QtGui.QDialogButtonBox(FileManagerWidget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.raise_()
        self.line.raise_()
        self.headingLabel.raise_()

        self.retranslateUi(FileManagerWidget)
        QtCore.QMetaObject.connectSlotsByName(FileManagerWidget)

    def retranslateUi(self, FileManagerWidget):
        FileManagerWidget.setWindowTitle(_translate("FileManagerWidget", "Form", None))
        self.headingLabel.setText(_translate("FileManagerWidget", "<html><head/><body><p><span style=\" font-weight:600;\">Variable File Manager:</span></p></body></html>", None))
        self.label_3.setText(_translate("FileManagerWidget", "File mode: ", None))
        self.loadButton.setText(_translate("FileManagerWidget", "LOAD", None))
        self.saveButton.setText(_translate("FileManagerWidget", "SAVE", None))
        self.label.setText(_translate("FileManagerWidget", "File type: ", None))
        self.label_2.setText(_translate("FileManagerWidget", "File path: ", None))
        self.getPathButton.setText(_translate("FileManagerWidget", "...", None))

