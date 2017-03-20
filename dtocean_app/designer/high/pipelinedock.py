# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\high\pipelinedock.ui'
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

class Ui_PipeLineDock(object):
    def setupUi(self, PipeLineDock):
        PipeLineDock.setObjectName(_fromUtf8("PipeLineDock"))
        PipeLineDock.resize(404, 853)
        PipeLineDock.setMinimumSize(QtCore.QSize(404, 299))
        PipeLineDock.setFeatures(QtGui.QDockWidget.DockWidgetClosable|QtGui.QDockWidget.DockWidgetMovable)
        PipeLineDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.dockWidgetContents = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy)
        self.dockWidgetContents.setMinimumSize(QtCore.QSize(400, 0))
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(5, 5, 0, 2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scopeFrame = QtGui.QFrame(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scopeFrame.sizePolicy().hasHeightForWidth())
        self.scopeFrame.setSizePolicy(sizePolicy)
        self.scopeFrame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scopeFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.scopeFrame.setObjectName(_fromUtf8("scopeFrame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.scopeFrame)
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(3, 2, 0, 2)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.scopeLabel = QtGui.QLabel(self.scopeFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scopeLabel.sizePolicy().hasHeightForWidth())
        self.scopeLabel.setSizePolicy(sizePolicy)
        self.scopeLabel.setMinimumSize(QtCore.QSize(175, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.scopeLabel.setFont(font)
        self.scopeLabel.setObjectName(_fromUtf8("scopeLabel"))
        self.horizontalLayout.addWidget(self.scopeLabel)
        self.localRadioButton = QtGui.QRadioButton(self.scopeFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.localRadioButton.sizePolicy().hasHeightForWidth())
        self.localRadioButton.setSizePolicy(sizePolicy)
        self.localRadioButton.setMinimumSize(QtCore.QSize(110, 0))
        self.localRadioButton.setChecked(False)
        self.localRadioButton.setObjectName(_fromUtf8("localRadioButton"))
        self.scopeButtonGroup = QtGui.QButtonGroup(PipeLineDock)
        self.scopeButtonGroup.setObjectName(_fromUtf8("scopeButtonGroup"))
        self.scopeButtonGroup.addButton(self.localRadioButton)
        self.horizontalLayout.addWidget(self.localRadioButton)
        self.globalRadioButton = QtGui.QRadioButton(self.scopeFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.globalRadioButton.sizePolicy().hasHeightForWidth())
        self.globalRadioButton.setSizePolicy(sizePolicy)
        self.globalRadioButton.setChecked(True)
        self.globalRadioButton.setObjectName(_fromUtf8("globalRadioButton"))
        self.scopeButtonGroup.addButton(self.globalRadioButton)
        self.horizontalLayout.addWidget(self.globalRadioButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.scopeFrame)
        self.treeWidget = QtGui.QTreeWidget(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.verticalLayout.addWidget(self.treeWidget)
        PipeLineDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(PipeLineDock)
        QtCore.QMetaObject.connectSlotsByName(PipeLineDock)

    def retranslateUi(self, PipeLineDock):
        PipeLineDock.setWindowTitle(_translate("PipeLineDock", "Pipeline", None))
        self.scopeLabel.setText(_translate("PipeLineDock", "Assessment scope:", None))
        self.localRadioButton.setText(_translate("PipeLineDock", "Module", None))
        self.globalRadioButton.setText(_translate("PipeLineDock", "Global", None))
        self.treeWidget.headerItem().setText(0, _translate("PipeLineDock", "Root:", None))

