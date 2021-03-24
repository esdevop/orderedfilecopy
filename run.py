"""
GUI to copy files from one directory to another

Author:
    Egor Seliunin
"""


import sys
import os
import re
from PyQt5 import QtWidgets, uic

import copyfiles

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('qtdesign/mainwindow.ui', self)

        # main window parameters
        self.setFixedSize(496,620)
        self.setWindowTitle("orderedcopy")

        # containers for variables
        self.path_fromto = {
            "LOAD_FROM_PATH": None,
            "LOAD_TO_PATH": None
        }
        
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
        self.toolButtonPathToOutput.clicked.connect(lambda: self.onCopyButtonClicked(self.lineEditPathToOutput))

        self.lineEditPathToSource.returnPressed.connect(self.setPaths)
        self.lineEditPathToOutput.returnPressed.connect(self.setPaths)

        self.pushButtonShowList.clicked.connect(self.showFileList)

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

    def setPaths(self):
        """
        Set the variables loadfrom_path and loadto_path from the values in lineEdit
        """
        self.path_fromto["LOAD_FROM_PATH"] = str(self.lineEditPathToSource.text())
        self.path_fromto["LOAD_TO_PATH"] = str(self.lineEditPathToOutput.text())
        for key in self.path_fromto:
            print("{} set to: {}".format(key, self.path_fromto[key]))

    def showFileList(self):
        """
        Show the list of files in text browser
        """
        self.setPaths()
        self.textBrowser.clear()
        file_lst = sorted(copyfiles.get_listdir(self.path_fromto["LOAD_FROM_PATH"]), reverse=False)
        self.textBrowser.append("<html><b>Files will be copied in the following order:<html><b>")
        for name in file_lst:
            self.textBrowser.append(name)





    


def run():
    """
    Runs the application
    """
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()