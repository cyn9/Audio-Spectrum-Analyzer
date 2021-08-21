from PyQt5 import uic
from PyQt5 import QtWidgets

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

        self.btn_Close.clicked.connect(lambda: self.close())
