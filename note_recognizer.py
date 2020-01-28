import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
from os import getcwd, path


class PowerSpectralDenisity(FigureCanvasQTAgg):

    def __init__(self, parent=None, xval=np.zeros(1000), yval=[0] * 1000):
        self.xval = xval
        self.yval = yval
        # create the Figure
        fig = Figure(figsize=(5, 5), dpi=100)   # figsize - in inch
        FigureCanvasQTAgg.__init__(self, fig)
        # create the axes
        self.axes = fig.add_subplot(111)
        self.axes.grid(True)
        self.axes.set_title("Power Spectral Density")
        self.axes.set_ylabel("Power Density")
        self.axes.set_xlabel("Frequency")
        self.axes.set_xlim(left=0)
        self.setParent(parent)
        self.axes.plot(self.xval, self.yval)
        self.draw()



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
        self.width = 500
        self.height = 500
        # setup UI
        self.configureUI()
        self.createWidgets()

    def configureUI(self):
        """Setting general configurations of the application"""
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon("icons//logo_uksw.ico"))
        self.statusBar().showMessage('Ready')

    def createWidgets(self):
        """Creating the widgets of the application"""
        # create the Menubar
        self.addMenuBar()

        # create a waveform
        self.canvas = PowerSpectralDenisity(self)

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

    def closeApplication(self):
        """Close the application."""
        QtWidgets.qApp.quit()

    def getFilename(self):
        """Function gets a file path to extract and save it to file name."""
        #  getcwd() takes a current working directory of a process
        fileName = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open File", getcwd(), "Wave files (*.wav)")
        # get only the file path from fileName tuple
        self.filePath = fileName[0]
        # split dir path and filename
        head_tail = path.split(self.filePath)
        # get the tail from the head_tail tuple
        self.fileName = head_tail[1]
        print(self.fileName)

    def showAbout(self):
        """Show information about project and author."""
        aboutMessage = QtWidgets.QMessageBox()
        aboutMessage.setWindowTitle(self.title)
        aboutMessage.setWindowIcon(QtGui.QIcon("icons//logo_uksw.ico"))
        aboutMessage.setText(self.INFO)
        aboutMessage.setIcon(QtWidgets.QMessageBox.Information)
        aboutMessage.exec_()

    def showVersion(self):
        versionMessage = QtWidgets.QMessageBox()
        versionMessage.setWindowTitle("Version")
        versionMessage.setText("Python 3.7.5 with PyQt5")
        versionMessage.setIcon(QtWidgets.QMessageBox.Information)
        versionMessage.exec_()

    def addPlot(self):
        pass


# Start program
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainApplication()
    window.show()
    app.exec()
