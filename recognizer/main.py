import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from os import getcwd, path
import winsound

from recognizer.plot import SpectralPlot


class MainApplication(QtWidgets.QMainWindow):

    INFO = (
        "Student Final Project with:\n"
        "Digital Processing of Signal\n"
        "Cardinal Stefan Wyszynski University in Warsaw\n\n"
        "Author: Konrad Tarnowski\n"
        "MIT License © 2020"
    )

    def __init__(self):
        super().__init__()
        # setup variables
        self.title = "Music Note Recognizer"
        self.top = 50
        self.left = 50
        self.width = 700
        self.height = 600
        self.iconName = "icons//logo_uksw.ico"
        self.filePath = None
        # setup UI
        self.configureUI()
        self.createWidgets()
        self.setupLayout()

    def configureUI(self):
        """Setting general configurations of the application"""
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon(self.iconName))

    def createWidgets(self):
        """Creating the widgets of the application"""
        # create the Menubar
        self.addMenuBar()
        # create buttons
        self.addButtons()
        # create the waveform
        self.plotCanvas = SpectralPlot(self)
        # create the status bar
        self.addStatusBar()

    def addMenuBar(self):
        # create the Menu Bar from QMainWindow
        menuBar = self.menuBar()

        # create Root Menus
        fileMenu = menuBar.addMenu("&File")
        helpMenu = menuBar.addMenu("&Help")

        # create Actons for menus
        openAction = QtWidgets.QAction("&Open", self)
        openAction.setShortcut("Ctrl+O")

        quitAction = QtWidgets.QAction('&Quit', self)
        quitAction.setShortcut("Ctrl+Q")

        aboutAction = QtWidgets.QAction("&About", self)
        versionAction = QtWidgets.QAction("&Version", self)

        # add actions to Menus
        fileMenu.addAction(openAction)
        fileMenu.addAction(quitAction)

        helpMenu.addAction(aboutAction)
        helpMenu.addAction(versionAction)

        # events
        openAction.triggered.connect(self.getFilename)
        quitAction.triggered.connect(self.closeApplication)
        aboutAction.triggered.connect(self.showAbout)
        versionAction.triggered.connect(self.showVersion)

    def addButtons(self):
        """Creating the buttons on the top bar"""
        # play button
        self.playButton = QtWidgets.QPushButton("Play")
        self.playButton.setIcon(QtGui.QIcon("assets\\play.png"))
        self.playButton.setIconSize(QtCore.QSize(32, 32))

        # stop button
        self.stopButton = QtWidgets.QPushButton("Stop")
        self.stopButton.setIcon(QtGui.QIcon("assets\\stop.png"))
        self.stopButton.setIconSize(QtCore.QSize(32, 32))

        # music note label
        self.resultMusicNote = QtWidgets.QLabel("?")
        self.resultMusicNote.setFont(QtGui.QFont("Arial", 12))
        self.resultMusicNote.setAlignment(QtCore.Qt.AlignCenter)
        self.resultMusicNote.setFrameShape(QtWidgets.QFrame.Panel)
        self.resultMusicNote.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.resultMusicNote.setLineWidth(3)

        # regognize buttton
        self.recognizeButton = QtWidgets.QPushButton("Recognize a Note")
        self.recognizeButton.setMinimumHeight(40)
        self.recognizeButton.setFont(QtGui.QFont("Arial", 10))
        self.recognizeButton.setStyleSheet("background-color: red; font: bold")

        # clear button
        self.clearButton = QtWidgets.QPushButton("Clear")
        self.clearButton.setMinimumHeight(40)

        # events
        self.playButton.clicked.connect(self.playSound)
        self.stopButton.clicked.connect(self.stopSound)
        self.recognizeButton.clicked.connect(self.generatePlot)
        self.clearButton.clicked.connect(self.clearPlot)

    def addStatusBar(self):
        # create a label
        self.status = QtWidgets.QLabel()
        self.status.setText("Ready")
        # set label as
        self.statusBar().addWidget(self.status)

    # ======== Menu Bar function ========
    def getFilename(self):
        """Function gets a file path to extract and save it to file name."""
        #  getcwd() takes a current working directory of a process
        fileName = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open File", getcwd(), "Wave files (*.wav)")
        # if file was choosen
        if fileName[0] != "":
            # get only the file path from fileName tuple
            self.filePath = fileName[0]

            # split dir path and filename
            head_tail = path.split(self.filePath)

            # get the tail from the head_tail tuple
            self.fileName = head_tail[1]

            # change the statusbar
            self.status.setText("Selected File: {}".format(self.fileName))

    def closeApplication(self):
        """Close the application."""
        QtWidgets.qApp.quit()

    def showAbout(self):
        """Show information about project and author."""
        aboutMessage = QtWidgets.QMessageBox()
        aboutMessage.setWindowTitle(self.title)
        aboutMessage.setWindowIcon(QtGui.QIcon(self.iconName))
        aboutMessage.setText(self.INFO)
        aboutMessage.setIcon(QtWidgets.QMessageBox.Information)
        aboutMessage.exec_()

    def showVersion(self):
        versionMessage = QtWidgets.QMessageBox()
        versionMessage.setWindowTitle("Version")
        versionMessage.setText("Python 3.7.5 with PyQt5\nfor Windows")
        versionMessage.setWindowIcon(QtGui.QIcon(self.iconName))
        versionMessage.setIcon(QtWidgets.QMessageBox.Information)
        versionMessage.exec_()

    def setupLayout(self):
        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by defaul
        centralWidget = QtWidgets.QWidget()

        # vertical container will be a main layout
        mainLayout = QtWidgets.QVBoxLayout(centralWidget)

        # setup horizontal container for buttons
        horizontalBox = QtWidgets.QHBoxLayout()
        horizontalBox.setDirection(QtWidgets.QVBoxLayout.LeftToRight)
        horizontalBox.setSpacing(50)
        horizontalBox.addWidget(self.playButton)
        horizontalBox.addWidget(self.stopButton)
        horizontalBox.addWidget(self.resultMusicNote)
        horizontalBox.addWidget(self.recognizeButton)
        horizontalBox.addWidget(self.clearButton)

        mainLayout.addLayout(horizontalBox)
        mainLayout.addWidget(self.plotCanvas)
        self.setCentralWidget(centralWidget)

    # ======== Buttons function ========
    def playSound(self):
        """Function working only for Windows"""
        if self.filePath != None:
            winsound.PlaySound(self.filePath, winsound.SND_ASYNC)
        else:
            errorMessage = QtWidgets.QMessageBox()
            errorMessage.setIcon(QtWidgets.QMessageBox.Critical)
            errorMessage.setWindowIcon(QtGui.QIcon(self.iconName))
            errorMessage.setWindowTitle("File path is wrong")
            errorMessage.setText("Please choose a WAV file.")
            errorMessage.exec_()

    def stopSound(self):
        winsound.PlaySound(None, winsound.SND_FILENAME)

    def generatePlot(self):
        """Load a file and generate plots."""
        if self.filePath != None:
            # open a WAV file
            self.plotCanvas.open(self.filePath)

            # plot and draw a function
            self.plotCanvas.plot()

            # change status bar
            self.status.setText("Loaded File: {}".format(self.fileName))

        else:
            errorMessage = QtWidgets.QMessageBox()
            errorMessage.setIcon(QtWidgets.QMessageBox.Critical)
            errorMessage.setWindowIcon(QtGui.QIcon(self.iconName))
            errorMessage.setWindowTitle("File not found")
            errorMessage.setText("Please choose a WAV file and try again.")
            errorMessage.exec_()

    def clearPlot(self):
        self.plotCanvas.cleanAxes()
        self.filePath = None
        self.fileName = None
        self.status.setText("Ready")


def main():
    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    app = QtWidgets.QApplication(sys.argv)
    window = MainApplication()
    # IMPORTANT!!!!! Windows are hidden by default.
    window.show()
    # Start the event loop.
    app.exec()

    # Your application won't reach here until you exit and the event
    # loop has stopped.
