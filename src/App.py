import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from Table import *
from SAButtonWidget import *


class AppWindow(QMainWindow):

    def __init__(self):
        super(AppWindow, self).__init__()
        # initialize Window
        self.initMainWindow()
        self.createPopupMenu()
        self.initMainMenu()

        # setup widgets
        self.initTableWidget()
        self.initButtonWidget()

        # initialize gui
        self.initUi()

    def initMainWindow(self):
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Main Window")
        self.resize(1200, 800)
        #centers window
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))

    def initMainMenu(self):
        mBar = self.menuBar()
        self.fileMenu = mBar.addMenu("File")  # Menu
        self.fileMenu.addAction("New")  # Item of Submenu File
        self.fileMenu.addAction("Open")  # Item of Submenu File
        self.fileMenu.addAction("Export")  # Item of Submenu File
        self.fileMenu.addAction("Quit")  # Item of Submenu File

        self.editMenu = mBar.addMenu("Edit")  # Menu
        self.editMenu.addAction("Cut")  # Item of Submenu Edit
        self.editMenu.addAction("Copy")  # Item of Submenu Edit
        self.editMenu.addAction("Paste")  # Item of Submenu Edit

        self.viewMenu = mBar.addMenu("View")  # Menu
        self.viewMenu.addAction("Semi-Auto")  # Item of Submenu View
        self.viewMenu.addAction("Auto")  # Item of Submenu View

        self.helpMenu = mBar.addMenu("Help")  # Menu
        self.helpMenu.addAction("About")  # Item of Submenu Help

        # set Bindings from QActions to relevant functions
        self.viewMenu.triggered[QAction].connect(self.toggleButtonWidget)


    # debug function for bindings
    def fileTrigger(self, q):
        print(" is triggered")

    # Initalize/show ui components here
    def initUi(self):
        self.show()

    # handles TableWidget stuff
    def initTableWidget(self):
        self.mTable = Table()
        self.setCentralWidget(self.mTable)

    # debug for widget toggle
    def toggleButtonWidget(self):
        if self.mButton.isVisible():
            self.mButton.hide()
        else:
            self.mButton.show()

    def initButtonWidget(self):
        self.mButton = SAButtonWidget()

    # def handleVisionWidget(self):
