# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\high\mainwindow.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1087, 618)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/turbine.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QtCore.QSize(28, 28))
        MainWindow.setDockNestingEnabled(True)
        MainWindow.setDockOptions(QtGui.QMainWindow.AllowNestedDocks|QtGui.QMainWindow.AllowTabbedDocks|QtGui.QMainWindow.AnimatedDocks|QtGui.QMainWindow.VerticalTabs)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(2, 4, 2, 2)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.stackedWidget = QtGui.QStackedWidget(self.centralWidget)
        self.stackedWidget.setEnabled(True)
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.verticalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1087, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menuBar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuSimulation = QtGui.QMenu(self.menuBar)
        self.menuSimulation.setObjectName(_fromUtf8("menuSimulation"))
        self.menuData = QtGui.QMenu(self.menuBar)
        self.menuData.setObjectName(_fromUtf8("menuData"))
        self.menuView = QtGui.QMenu(self.menuBar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuTools = QtGui.QMenu(self.menuBar)
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        MainWindow.setMenuBar(self.menuBar)
        self.fileToolBar = QtGui.QToolBar(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileToolBar.sizePolicy().hasHeightForWidth())
        self.fileToolBar.setSizePolicy(sizePolicy)
        self.fileToolBar.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.fileToolBar.setObjectName(_fromUtf8("fileToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.fileToolBar)
        self.scenarioToolBar = QtGui.QToolBar(MainWindow)
        self.scenarioToolBar.setObjectName(_fromUtf8("scenarioToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.scenarioToolBar)
        self.simulationToolBar = QtGui.QToolBar(MainWindow)
        self.simulationToolBar.setObjectName(_fromUtf8("simulationToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.simulationToolBar)
        self.viewToolBar = QtGui.QToolBar(MainWindow)
        self.viewToolBar.setEnabled(True)
        self.viewToolBar.setObjectName(_fromUtf8("viewToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.viewToolBar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.toolBar.setMovable(False)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setEnabled(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/document-new.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon1)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setEnabled(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/document-open.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon2)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionOpen_Recent = QtGui.QAction(MainWindow)
        self.actionOpen_Recent.setCheckable(True)
        self.actionOpen_Recent.setEnabled(False)
        self.actionOpen_Recent.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.actionOpen_Recent.setSoftKeyRole(QtGui.QAction.PositiveSoftKey)
        self.actionOpen_Recent.setObjectName(_fromUtf8("actionOpen_Recent"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/media-floppy.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon3)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave_As = QtGui.QAction(MainWindow)
        self.actionSave_As.setEnabled(False)
        self.actionSave_As.setObjectName(_fromUtf8("actionSave_As"))
        self.actionInitiate_Pipeline = QtGui.QAction(MainWindow)
        self.actionInitiate_Pipeline.setEnabled(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/db_update.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionInitiate_Pipeline.setIcon(icon4)
        self.actionInitiate_Pipeline.setObjectName(_fromUtf8("actionInitiate_Pipeline"))
        self.actionSelect_Database = QtGui.QAction(MainWindow)
        self.actionSelect_Database.setEnabled(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/db_select.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSelect_Database.setIcon(icon5)
        self.actionSelect_Database.setObjectName(_fromUtf8("actionSelect_Database"))
        self.actionAdd_Modules = QtGui.QAction(MainWindow)
        self.actionAdd_Modules.setEnabled(False)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/hardware.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_Modules.setIcon(icon6)
        self.actionAdd_Modules.setObjectName(_fromUtf8("actionAdd_Modules"))
        self.actionAdd_Assessment = QtGui.QAction(MainWindow)
        self.actionAdd_Assessment.setEnabled(False)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/calc.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_Assessment.setIcon(icon7)
        self.actionAdd_Assessment.setObjectName(_fromUtf8("actionAdd_Assessment"))
        self.actionAdd_Strategy = QtGui.QAction(MainWindow)
        self.actionAdd_Strategy.setEnabled(False)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/kwin4.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_Strategy.setIcon(icon8)
        self.actionAdd_Strategy.setObjectName(_fromUtf8("actionAdd_Strategy"))
        self.actionInitiate_Dataflow = QtGui.QAction(MainWindow)
        self.actionInitiate_Dataflow.setEnabled(False)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/pipe.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionInitiate_Dataflow.setIcon(icon9)
        self.actionInitiate_Dataflow.setObjectName(_fromUtf8("actionInitiate_Dataflow"))
        self.actionRun_Strategy = QtGui.QAction(MainWindow)
        self.actionRun_Strategy.setEnabled(False)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/player_end.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRun_Strategy.setIcon(icon10)
        self.actionRun_Strategy.setObjectName(_fromUtf8("actionRun_Strategy"))
        self.actionProperties = QtGui.QAction(MainWindow)
        self.actionProperties.setEnabled(False)
        self.actionProperties.setObjectName(_fromUtf8("actionProperties"))
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setEnabled(False)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/colors-window-close.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClose.setIcon(icon11)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionRun_Current = QtGui.QAction(MainWindow)
        self.actionRun_Current.setEnabled(False)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/player_play.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRun_Current.setIcon(icon12)
        self.actionRun_Current.setObjectName(_fromUtf8("actionRun_Current"))
        self.actionCopy = QtGui.QAction(MainWindow)
        self.actionCopy.setEnabled(False)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/editcopy.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(icon13)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionPaste = QtGui.QAction(MainWindow)
        self.actionPaste.setEnabled(False)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/editpaste.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaste.setIcon(icon14)
        self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
        self.actionUndo = QtGui.QAction(MainWindow)
        self.actionUndo.setEnabled(False)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/undo-128.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUndo.setIcon(icon15)
        self.actionUndo.setObjectName(_fromUtf8("actionUndo"))
        self.actionRedo = QtGui.QAction(MainWindow)
        self.actionRedo.setEnabled(False)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/redo-128.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRedo.setIcon(icon16)
        self.actionRedo.setObjectName(_fromUtf8("actionRedo"))
        self.actionHelp_Index = QtGui.QAction(MainWindow)
        self.actionHelp_Index.setEnabled(True)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/help_index.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHelp_Index.setIcon(icon17)
        self.actionHelp_Index.setObjectName(_fromUtf8("actionHelp_Index"))
        self.actionSystem_Log = QtGui.QAction(MainWindow)
        self.actionSystem_Log.setEnabled(False)
        self.actionSystem_Log.setObjectName(_fromUtf8("actionSystem_Log"))
        self.actionData = QtGui.QAction(MainWindow)
        self.actionData.setCheckable(True)
        self.actionData.setEnabled(False)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/data.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionData.setIcon(icon18)
        self.actionData.setObjectName(_fromUtf8("actionData"))
        self.actionPlots = QtGui.QAction(MainWindow)
        self.actionPlots.setCheckable(True)
        self.actionPlots.setEnabled(False)
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/plots.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlots.setIcon(icon19)
        self.actionPlots.setObjectName(_fromUtf8("actionPlots"))
        self.actionComparison = QtGui.QAction(MainWindow)
        self.actionComparison.setCheckable(True)
        self.actionComparison.setEnabled(False)
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/ruler.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionComparison.setIcon(icon20)
        self.actionComparison.setObjectName(_fromUtf8("actionComparison"))
        self.actionShow_Simulations = QtGui.QAction(MainWindow)
        self.actionShow_Simulations.setEnabled(False)
        self.actionShow_Simulations.setObjectName(_fromUtf8("actionShow_Simulations"))
        self.actionShow_Pipeline = QtGui.QAction(MainWindow)
        self.actionShow_Pipeline.setEnabled(False)
        self.actionShow_Pipeline.setObjectName(_fromUtf8("actionShow_Pipeline"))
        self.actionInitiate_Bathymetry = QtGui.QAction(MainWindow)
        self.actionInitiate_Bathymetry.setEnabled(False)
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/maps.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionInitiate_Bathymetry.setIcon(icon21)
        self.actionInitiate_Bathymetry.setObjectName(_fromUtf8("actionInitiate_Bathymetry"))
        self.actionRun_Themes = QtGui.QAction(MainWindow)
        self.actionRun_Themes.setEnabled(False)
        icon22 = QtGui.QIcon()
        icon22.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/player_calc.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRun_Themes.setIcon(icon22)
        self.actionRun_Themes.setObjectName(_fromUtf8("actionRun_Themes"))
        self.actionWEC_Simulator = QtGui.QAction(MainWindow)
        self.actionWEC_Simulator.setObjectName(_fromUtf8("actionWEC_Simulator"))
        self.actionAbout = QtGui.QAction(MainWindow)
        icon23 = QtGui.QIcon()
        icon23.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/Information_icon.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon23)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionProperties)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionHelp_Index)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuSimulation.addAction(self.actionAdd_Modules)
        self.menuSimulation.addAction(self.actionAdd_Assessment)
        self.menuSimulation.addAction(self.actionAdd_Strategy)
        self.menuSimulation.addSeparator()
        self.menuSimulation.addAction(self.actionRun_Current)
        self.menuSimulation.addAction(self.actionRun_Themes)
        self.menuSimulation.addAction(self.actionRun_Strategy)
        self.menuData.addAction(self.actionSelect_Database)
        self.menuData.addSeparator()
        self.menuData.addAction(self.actionInitiate_Pipeline)
        self.menuData.addAction(self.actionInitiate_Bathymetry)
        self.menuData.addAction(self.actionInitiate_Dataflow)
        self.menuView.addAction(self.actionShow_Simulations)
        self.menuView.addAction(self.actionShow_Pipeline)
        self.menuView.addAction(self.actionSystem_Log)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionData)
        self.menuView.addAction(self.actionPlots)
        self.menuView.addAction(self.actionComparison)
        self.menuTools.addAction(self.actionWEC_Simulator)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuSimulation.menuAction())
        self.menuBar.addAction(self.menuData.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.fileToolBar.addSeparator()
        self.fileToolBar.addAction(self.actionNew)
        self.fileToolBar.addAction(self.actionOpen)
        self.fileToolBar.addAction(self.actionSave)
        self.fileToolBar.addAction(self.actionClose)
        self.scenarioToolBar.addAction(self.actionSelect_Database)
        self.scenarioToolBar.addAction(self.actionInitiate_Pipeline)
        self.scenarioToolBar.addAction(self.actionInitiate_Bathymetry)
        self.scenarioToolBar.addAction(self.actionInitiate_Dataflow)
        self.simulationToolBar.addAction(self.actionAdd_Modules)
        self.simulationToolBar.addAction(self.actionAdd_Assessment)
        self.simulationToolBar.addAction(self.actionAdd_Strategy)
        self.simulationToolBar.addSeparator()
        self.simulationToolBar.addAction(self.actionRun_Current)
        self.simulationToolBar.addAction(self.actionRun_Themes)
        self.simulationToolBar.addAction(self.actionRun_Strategy)
        self.viewToolBar.addAction(self.actionData)
        self.viewToolBar.addAction(self.actionPlots)
        self.viewToolBar.addAction(self.actionComparison)
        self.toolBar.addAction(self.actionHelp_Index)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("activated()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "DTOcean", None))
        self.menuFile.setTitle(_translate("MainWindow", "&File", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.menuSimulation.setTitle(_translate("MainWindow", "Simulation", None))
        self.menuData.setTitle(_translate("MainWindow", "Data", None))
        self.menuView.setTitle(_translate("MainWindow", "View", None))
        self.menuTools.setTitle(_translate("MainWindow", "Tools", None))
        self.scenarioToolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.simulationToolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.viewToolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionNew.setText(_translate("MainWindow", "&New", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionOpen_Recent.setText(_translate("MainWindow", "Open Recent...", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionSave.setToolTip(_translate("MainWindow", "Save", None))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S", None))
        self.actionSave_As.setText(_translate("MainWindow", "Save As...", None))
        self.actionInitiate_Pipeline.setText(_translate("MainWindow", "Initiate Pipeline", None))
        self.actionSelect_Database.setText(_translate("MainWindow", "Select Database...", None))
        self.actionAdd_Modules.setText(_translate("MainWindow", "Add Modules...", None))
        self.actionAdd_Assessment.setText(_translate("MainWindow", "Add Assessment...", None))
        self.actionAdd_Strategy.setText(_translate("MainWindow", "Add Strategy...", None))
        self.actionInitiate_Dataflow.setText(_translate("MainWindow", "Initiate Dataflow", None))
        self.actionRun_Strategy.setText(_translate("MainWindow", "Run Strategy...", None))
        self.actionRun_Strategy.setToolTip(_translate("MainWindow", "Run Strategy", None))
        self.actionProperties.setText(_translate("MainWindow", "Properties...", None))
        self.actionClose.setText(_translate("MainWindow", "Close", None))
        self.actionRun_Current.setText(_translate("MainWindow", "Run Current Module...", None))
        self.actionCopy.setText(_translate("MainWindow", "Copy", None))
        self.actionPaste.setText(_translate("MainWindow", "Paste", None))
        self.actionUndo.setText(_translate("MainWindow", "Undo", None))
        self.actionRedo.setText(_translate("MainWindow", "Redo", None))
        self.actionHelp_Index.setText(_translate("MainWindow", "Index...", None))
        self.actionSystem_Log.setText(_translate("MainWindow", "Show System Log", None))
        self.actionData.setText(_translate("MainWindow", "Data", None))
        self.actionPlots.setText(_translate("MainWindow", "Plots", None))
        self.actionComparison.setText(_translate("MainWindow", "Comparisons", None))
        self.actionShow_Simulations.setText(_translate("MainWindow", "Show Simulations", None))
        self.actionShow_Pipeline.setText(_translate("MainWindow", "Show Pipeline", None))
        self.actionInitiate_Bathymetry.setText(_translate("MainWindow", "Initiate Bathymetry", None))
        self.actionRun_Themes.setText(_translate("MainWindow", "Run Themes...", None))
        self.actionRun_Themes.setToolTip(_translate("MainWindow", "Run Themes", None))
        self.actionWEC_Simulator.setText(_translate("MainWindow", "WEC Simulator", None))
        self.actionAbout.setText(_translate("MainWindow", "About DTOcean...", None))

import resources_mainwindow_rc
