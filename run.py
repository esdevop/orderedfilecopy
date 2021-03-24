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
        self.show()

    def menuBar(self):
        # Settings of the menu bar

        ## 'Exit' option in 'File' menu bar
        extractActionExit = self.actionExit
        extractActionExit.setShortcut("Ctrl+Q")
        extractActionExit.setStatusTip("Leave the app")
        extractActionExit.triggered.connect(self.close_application)

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

def run():
    """
    Runs the application
    """
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()