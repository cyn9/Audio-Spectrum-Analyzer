from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QStyle
from PyQt5 import uic
from PyQt5 import QtWidgets

from pyqtgraph.Qt import QtGui

import pyperclip

class HelpWindow(QtWidgets.QMainWindow):
    def __init__(self):
        """
        Constructs all the necessary attributes for HelpWindow object for
        getting the help window up-and-running.

        Parameters
        ----------
            None
        
        Returns
        -------
            None
        """
        super().__init__()
        HELP_WIN_SCR_WIDTH = 630
        HELP_WIN_SCR_HEIGHT = 664

        uic.loadUi('/Users/ciyan/Documents/Audio-Spectrum-Analyzer/ui/HelpWin.ui', self)
        self.setFixedSize(HELP_WIN_SCR_WIDTH, HELP_WIN_SCR_HEIGHT)

        # Button onClick event for close
        self.btn_Close.clicked.connect(lambda: self.close())

        # Button onClick event for copy
        self.btn_Copy.clicked.connect(self.copy)


    def copy(self):
        """
        Copies the text on the help window to the clipboard.

        Parameters
        ----------
            None
        
        Returns
        -------
            None
        """
        helpText = self.txtHelp.toPlainText()

        pyperclip.copy(helpText)

        # "Copied" message info box:
        copiedStyle = QApplication.style()
        copiedText = 'Copied help text to clipboard.'
        copiedMsg = QMessageBox()
        copiedMsg.setWindowTitle("Hi!")
        copiedMsg.setIcon(QMessageBox.Information)
        copiedMsg.setText(copiedText)
        copiedMsg.setWindowIcon(QtGui.QIcon(copiedStyle.standardIcon(QStyle.SP_DialogApplyButton)))
        copiedMsg.exec_()

