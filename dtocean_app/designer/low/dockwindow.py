# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\low\dockwindow.ui'
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

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName(_fromUtf8("DockWidget"))
        DockWidget.resize(800, 538)
        self.dockContents = QtGui.QWidget()
        self.dockContents.setObjectName(_fromUtf8("dockContents"))
        self.container_screen = QtGui.QFrame(self.dockContents)
        self.container_screen.setGeometry(QtCore.QRect(0, 0, 800, 513))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.container_screen.sizePolicy().hasHeightForWidth())
        self.container_screen.setSizePolicy(sizePolicy)
        self.container_screen.setMinimumSize(QtCore.QSize(750, 450))
        self.container_screen.setFrameShape(QtGui.QFrame.NoFrame)
        self.container_screen.setFrameShadow(QtGui.QFrame.Sunken)
        self.container_screen.setLineWidth(2)
        self.container_screen.setObjectName(_fromUtf8("container_screen"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.container_screen)
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout.setMargin(3)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame_left = QtGui.QFrame(self.container_screen)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_left.sizePolicy().hasHeightForWidth())
        self.frame_left.setSizePolicy(sizePolicy)
        self.frame_left.setMinimumSize(QtCore.QSize(350, 400))
        self.frame_left.setMaximumSize(QtCore.QSize(400, 16777215))
        self.frame_left.setFrameShape(QtGui.QFrame.Box)
        self.frame_left.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_left.setLineWidth(2)
        self.frame_left.setObjectName(_fromUtf8("frame_left"))
        self.verticalLayoutLeft = QtGui.QVBoxLayout(self.frame_left)
        self.verticalLayoutLeft.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.verticalLayoutLeft.setMargin(9)
        self.verticalLayoutLeft.setSpacing(6)
        self.verticalLayoutLeft.setObjectName(_fromUtf8("verticalLayoutLeft"))
        self.horizontalLayout.addWidget(self.frame_left)
        self.frame_right = QtGui.QFrame(self.container_screen)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_right.sizePolicy().hasHeightForWidth())
        self.frame_right.setSizePolicy(sizePolicy)
        self.frame_right.setMinimumSize(QtCore.QSize(400, 400))
        self.frame_right.setFrameShape(QtGui.QFrame.Box)
        self.frame_right.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_right.setLineWidth(2)
        self.frame_right.setObjectName(_fromUtf8("frame_right"))
        self.verticalLayoutRight = QtGui.QVBoxLayout(self.frame_right)
        self.verticalLayoutRight.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayoutRight.setMargin(9)
        self.verticalLayoutRight.setSpacing(6)
        self.verticalLayoutRight.setObjectName(_fromUtf8("verticalLayoutRight"))
        self.horizontalLayout.addWidget(self.frame_right)
        DockWidget.setWidget(self.dockContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "DockWidget", None))

