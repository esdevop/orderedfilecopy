"""
GUI to copy files from one directory to another

Author:
    Egor Seliunin
"""


import sys
import os
import re
from PyQt5 import QtWidgets, uic

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('qtdesign/mainwindow.ui', self)

        # main window parameters
        self.setFixedSize(496,620)
        self.setWindowTitle("orderedcopy")
        
        self.menuBar()
        self.mainFrame()
        self.show()

    def menuBar(self):
        # Settings of the menu bar

        ## 'Exit' option in 'File' menu bar
        extractActionExit = self.actionExit
        extractActionExit.setShortcut("Ctrl+Q")
        extractActionExit.setStatusTip("Leave the app")
        extractActionExit.triggered.connect(self.close_application)

    def mainFrame(self):
        # Settings for the main frame
        self.toolButtonPathToSource.clicked.connect(lambda: self.onCopyButtonClicked(self.lineEditPathToSource))
        # Settings for the main frame
        self.toolButtonPathToOutput.clicked.connect(lambda: self.onCopyButtonClicked(self.lineEditPathToOutput))

    def close_application(self):
        """
        Add pop up window on closing event if there is a warning
        """
        choice = QtWidgets.QMessageBox.question(self, 'Exit?',
                                            "Do you want to exit?",
                                            QtWidgets.QMessageBox.Yes |
                                            QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def onCopyButtonClicked(self, lineEdit):
        """
        Handles CopyTo/CopyFrom buttons and leneEdit
        """
        path = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.setLineEdit(lineEdit, path)
    
    def setLineEdit(self, lineEdit, path):
        """
        Set the text in lineEdit
        """
        lineEdit.setText(str(path))

    def setPathCopyTo(self, loadfrom_path):
        """
        Set the text in lineEditPathToSource and self.loadfrom_path
        """
        self.lineEditPathToSource.setText(str(loadfrom_path))
        self.loadfrom_path = str(loadfrom_path)


def run():
    """
    Runs the application
    """
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()