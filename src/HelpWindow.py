from PyQt5 import uic
from PyQt5 import QtWidgets

class HelpWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        HELP_WIN_SCR_WIDTH = 630
        HELP_WIN_SCR_HEIGHT = 630

        uic.loadUi('/Users/ciyan/Documents/Audio-Spectrum-Analyzer/ui/HelpWin.ui', self)
        self.setFixedSize(HELP_WIN_SCR_WIDTH, HELP_WIN_SCR_HEIGHT)
