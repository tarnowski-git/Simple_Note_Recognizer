from PyQt5 import QtWidgets, QtCore, QtGui
import sys


class MainApplication(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        # setup variables
        self.title = "Music Note Recognizer"
        self.top = 50
        self.left = 50
        self.width = 400
        self.height = 400
        # setup UI
        self.configureUI()

    def configureUI(self):
        """Setting general configurations of the application"""
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon("icons//logo_uksw.ico"))
        self.statusBar().showMessage('Ready')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainApplication()
    window.show()
    app.exec()
