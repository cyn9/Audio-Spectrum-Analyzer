'''
    @ author        cico
    @ version       5.0
    @ date          08/07/21
    @ time          4:52 PM
    @ description   Real-time audio signal analyzer
'''

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QStyle
from PyQt5 import QtWidgets

from pyqtgraph.Qt import QtGui
from AudioAnalyzer import MainWindow

import sys


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    main = MainWindow()
    main.show()

    # Welcome message:
    welcomeMsgStyle = QApplication.style()
    welcomeMsg = QMessageBox()
    welcomeMsg.setWindowTitle("Hi!")
    welcomeMsg.setIcon(QMessageBox.Information)
    welcomeMsg.setText('Welcome to Real-Time Audio Analyzer. Please refer to <br> "Help" section for further information. Press OK to start.')
    welcomeMsg.setWindowIcon(QtGui.QIcon(welcomeMsgStyle.standardIcon(QStyle.SP_DialogApplyButton)))
    welcomeMsg.exec_()

    # Start animation for real-time plotting.
    main.animation()
    
    # sys.exit(app.exec_())


if __name__ == '__main__':      
    main()
