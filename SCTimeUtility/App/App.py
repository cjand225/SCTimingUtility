'''
    Module: App.py
    Purpose: Controller for entire application, used to periodically update project with data to and from the
             model.
    Depends On:

'''
# standard lib imports
import sys, os

# dependency imports
from PyQt5.QtWidgets import QApplication

# package imports
from SCTimeUtility.App import mainUIPath, quitDialogUIPath, helpDialogUIPath, aboutDialogUIPath, userManPath, \
    aboutManPath, adminManPath
from SCTimeUtility.App.AppWindow import AppWindow
from SCTimeUtility.Table.Table import Table
from SCTimeUtility.Video.Video import Video
from SCTimeUtility.Graph.Graph import Graph
from SCTimeUtility.LeaderBoard.LeaderBoard import LeaderBoard
from SCTimeUtility.Log.Log import getLog
from SCTimeUtility.Log.LogWidget import LogWidget
from SCTimeUtility.System.FileSystem import exportCSV, importCSV


class App(QApplication):

    def __init__(self):
        super(App, self).__init__(sys.argv)
        self.mainWindow = None
        self.running = False

        # Forward Module Declaration
        self.logger = getLog()

        self.ModuleList = []

        self.table = None
        self.semiAuto = None
        self.vision = None
        self.graph = None
        self.logWidget = None
        self.leaderBoard = None

        # Initializing everything
        self.initApplication()

    ''' 

        Function: initApplication(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the QApplication, required for running and maintaing program.

    '''

    def initApplication(self):
        self.initMainWindow()
        self.initLog()
        self.initTable()
        self.initVision()
        self.initGraph()
        self.initLeaderBoard()

        # adding and connecting essential components to user interface
        self.addComponents()
        self.connectActionsMainWindow()

    ''' 

        Function: initMainWindow(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes AppWindow in the mainWindow Variable attached to App Class as well as
                 Initializing any functions related to the AppWindow Class

    '''

    def initMainWindow(self):
        self.mainWindow = AppWindow(mainUIPath)
        self.mainWindow.initCloseDialog(quitDialogUIPath)

        self.mainWindow.actionAdminMan.triggered.connect(
            lambda l: self.mainWindow.createBrowserDialog(helpDialogUIPath, adminManPath))
        self.mainWindow.actionAbout.triggered.connect(
            lambda l: self.mainWindow.createBrowserDialog(aboutDialogUIPath, aboutManPath))
        self.mainWindow.actionUserMan.triggered.connect(
            lambda l: self.mainWindow.createBrowserDialog(helpDialogUIPath, userManPath))

    ''' 

        Function: initTableview(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the Table Class (w/ a path to the view's UI), that is its own controller for handling 
                 both its internal model and View class (however view class is passed to AppWindow to handle afterwards)

    '''

    def initTable(self):
        self.table = Table()
        if self.table is not None:
            self.logger.debug('[' + __name__ + ']' + ' Table Initialized')
        else:
            self.logger.debug('[' + __name__ + ']' + ' Table failed to initialize')

    ''' 

        Function: initVision(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the Vision Class (w/ a path to the View's UI), that handled camera interfacing, image
                 processing, and OCR related tasks, which then can interface with the Table Class in order to update
                 Various Cars with Laptime Information

    '''

    def initVision(self):
        self.vision = Video()
        if self.vision is not None:
            getLog().debug('[' + __name__ + '] ' + 'Video module Initialized')
        else:
            getLog().debug('[' + __name__ + '] ' + 'Video module failed to initialize')

    ''' 

        Function: initLog(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the Log Class (w/ a path to the View's UI and Writing directory), that handles
                 file writes to a specified file when the Log Class is invoked.

    '''

    def initLog(self):
        self.logWidget = LogWidget()
        if self.logWidget is not None:
            getLog().debug('[' + __name__ + '] ' + 'Log module initialized')
        else:
            getLog().debug('[' + __name__ + '] ' + 'Log module failed to initialize')

    ''' 

        Function: initGraph(self)
        Parameters: self
        Return Value: N/A
        Purpose: initializes the Graphing Module (w/ a path to the View's UI), which then when given information
                 in the form of lists and user specified information, can create Graphs via its own VieW

    '''

    def initGraph(self):
        self.graph = Graph()
        if self.graph is not None:
            getLog().debug('[' + __name__ + '] ' + 'Graph module initialized')
        else:
            getLog().debug('[' + __name__ + '] ' + 'Graph module failed to initialize')

    ''' 

        Function: initLeaderBoard(self)
        Parameters: self
        Return Value: N/A
        Purpose: initializes the LeaderBoard Module (w/ a path to the View's UI), which then when given information
                 in the form of lists of information based on racing data can create a visual list from its view for user.

    '''

    def initLeaderBoard(self):
        self.leaderBoard = LeaderBoard(self.table.CarStoreList)
        if self.leaderBoard is not None:
            getLog().debug('[' + __name__ + '] ' + 'LeaderBoard module initialized')
        else:
            getLog().debug('[' + __name__ + '] ' + 'LeaderBoard module failed to initialize')

    ''' 

        Function: addComponents(self)
        Parameters: self
        Return Value: N/A
        Purpose: Adds widgets from each module to mainWindow(AppWindow) to be handled as a sub component
                 of the overall View of the program.

    '''

    def addComponents(self):
        getLog().debug('[' + __name__ + '] ' + 'Adding components to Main Window')

        if self.logWidget is not None:
            self.mainWindow.addLog(self.logWidget)
        if self.table is not None:
            self.mainWindow.addTable(self.table.getTableWidget())
        if self.table.getSemiAuto() is not None:
            self.mainWindow.addSemiAuto(self.table.getSemiAuto())
        if self.vision is not None:
            self.mainWindow.addVision(self.vision.getWidget())
        if self.graph is not None:
            self.mainWindow.addGraph(self.graph)
        if self.leaderBoard is not None:
            self.mainWindow.addLeaderBoard(self.leaderBoard.getWidget())

        self.mainWindow.connectComponents()

    ''' 

        Function: connectActionsMainWindow(self)
        Parameters: self
        Return Value: N/A
        Purpose: connects Actions relating to the QMainWindow(AppWindow) that require a higher level scope
                 than what is normally allowed to AppWindow such as newfile, openfile, savefile, saveAs.

    '''

    def connectActionsMainWindow(self):
        getLog().debug('[' + __name__ + '] ' + 'Binding listeners to Main Window')
        self.mainWindow.actionNewSess.triggered.connect(self.newSession)
        self.mainWindow.actionOpenDir.triggered.connect(self.importDataFromFile)
        self.mainWindow.actionExportData.triggered.connect(self.exportDataToFile)
        self.table.Widget.saveShortcut.activated.connect(self.exportDataToFile)
        self.table.CarStoreList.dataModified.connect(self.graphUpdate)

    ''' 
    
        Function: run(self)
        Parameters: self
        Return Value: N/A
        Purpose: Runs entire Program until Application returns from executing, which then closes with a 
                 proper exit code.

    '''

    def run(self):
        self.running = True
        sys.exit(self.exec_())

    ''' 

        Function: SaveAsFile(self)
        Parameters: self
        Return Value: N/A
        Purpose: Saves the current session of data from TableModel to the writeFile chosen by the user,
                 if the user doesn't choose a filename, it'll assume a default file name to save as under
                 the current working directory.

    '''

    def exportDataToFile(self):
        writePath = os.path.join(self.mainWindow.openDirDialog())
        if os.path.exists(writePath):
            exportCSV(self.table.CarStoreList, writePath)
            self.logger.debug('[' + __name__ + '] ' + 'Data saved to: ' + writePath)
        else:
            self.logger.debug('[' + __name__ + '] ' + 'Could not save data to: ' + str(writePath))

    ''' 

        Function: importDataFromFile(self)
        Parameters: self
        Return Value: N/A
        Purpose: opens a directory chosen by user, then proceeds to read and parse CSVs that have relevant tokens
                 and data. 

    '''

    # TODO: Rework so that addcar passes in Table module data
    def importDataFromFile(self):
        readDir = os.path.join(self.mainWindow.openDirDialog())
        if os.path.exists(readDir):
            importCSV(readDir)
        else:
            pass

    ''' 

        Function: newSession(self)
        Parameters: self
        Return Value: N/A
        Purpose: Clears any currently existing Table module, allowing for application to essentially restart.

    '''

    def newSession(self):
        if not self.table.CarStoreList:
            self.logger.debug('[' + __name__ + '] ' + 'Started new session requested by user: ')
        else:
            self.logger.debug('[' + __name__ + '] ' + 'Failed to create new session.')

    '''
        Function: graphUpdate
        Parameters: self
        Return Value: N/A
        Purpose: Binds an update function to pass a copy of carStorage to the graph if the table is ever updated with
                 new information (based on qt signals emitted by cars).
    
    '''

    def graphUpdate(self):
        self.graph.handleUpdate(self.table.getCarStorage())

    '''
        Function: graphUpdate
        Parameters: self
        Return Value: N/A
        Purpose: Binds an update function to pass a copy of carStorage to the leaderboard if the table is ever updated 
                 with new information (based on qt signals emitted by cars).

    '''

    def leaderBoardUpdate(self):
        self.leaderBoard.updateData(self.table.getCarStorage())
