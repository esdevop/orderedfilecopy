"""
GUI to copy files from one directory to another

Author:
    Egor Seliunin
"""


import sys
import os
import re
import traceback
import errno
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
        self.pushButtonCopy.clicked.connect(self.copyFilesInOrder)

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

    def checkPaths(self, path_to_dir, name):
        """
        Checks the validity of the 'Load to' and 'Load from' pathes
        """
        message = "Ok"
        if not os.path.isdir(path_to_dir):
            try:
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path_to_dir)
            except FileNotFoundError:
                traceback.print_exc()
                message = "Error in '{}': Directory '{}' is not found".format(name, path_to_dir)
        return message

    def showFileList(self):
        """
        Show the list of files in text browser
        """
        self.setPaths()
        self.textBrowser.clear()
        isfine_message = self.checkPaths(self.path_fromto["LOAD_FROM_PATH"], "Copy from")
        if isfine_message == "Ok":
            file_lst = sorted(copyfiles.get_listdir(self.path_fromto["LOAD_FROM_PATH"]), reverse=False)
            self.textBrowser.append("<html><b>Files will be copied in the following order:<html><b>")
            for name in file_lst:
                self.textBrowser.append(name)
        else:
            self.textBrowser.append('<html><b><p style="color:red;">{}</p><html><b>'.format(isfine_message))

    def copyFilesInOrder(self):
        """
        Copy files from 'Load from' to 'Load to'
        """
        self.showFileList()
        isfine_loadfrom = self.checkPaths(self.path_fromto["LOAD_FROM_PATH"], "Copy from")
        isfine_loadto = self.checkPaths(self.path_fromto["LOAD_TO_PATH"], "Copy to")
        if isfine_loadfrom == "Ok":
            if isfine_loadto == "Ok":
                copyfiles.copyto(self.path_fromto["LOAD_FROM_PATH"], self.path_fromto["LOAD_TO_PATH"])
                self.textBrowser.append("<html><b>Done!<html><b>")
            else:
                self.textBrowser.append('<html><b><p style="color:red;">{}</p><html><b>'.format(isfine_loadto))
        else:
            self.textBrowser.clear()
            self.textBrowser.append('<html><b><p style="color:red;">{}</p><html><b>'.format(isfine_loadfrom))

def run():
    """
    Runs the application
    """
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()