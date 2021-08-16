'''
    @ author        cico
    @ version       5.0
    @ date          08/16/21
    @ time          1:32 PM
    @ description   Real-time audio signal analyzer
'''

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QStyle
from PyQt5 import QtWidgets

from pyqtgraph.Qt import QtGui
from AudioAnalyzer import MainWindow

import sys
import argparse
import textwrap

parserDescription = textwrap.dedent('''\
-----------------------------
Audio Signal Analyzer:
-----------------------------
   This program analyzes
 microphone input sound and
 outputs the raw signal and
 its frequency spectrum in
 real-time.
-----------------------------
''')

parser = argparse.ArgumentParser(prog = 'Audio Analyzer',
                                 formatter_class = argparse.RawDescriptionHelpFormatter,
                                 description = parserDescription)

group = parser.add_mutually_exclusive_group()
group.add_argument('-q', '--quiet', action = 'store_true', help = 'Print quiet.')
group.add_argument('-v', '--verbose', action = 'store_true', help = 'Print verbose.')

cmd_args = parser.parse_args()

def main(argmode):
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    cmd_args_dict = vars(cmd_args)
    arg_quiet = cmd_args_dict['quiet']
    arg_verbose = cmd_args_dict['verbose']
    args_list = [arg_quiet, arg_verbose]
    # print(args_list)

    main = MainWindow(cmd_args = args_list)
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
    if (len(sys.argv) > 1):
        if cmd_args.quiet:
            argmode = 'quiet'
            print("Quiet is selected.")

        elif cmd_args.verbose:
            argmode = 'verbose'
            print("Verbose is selected.")

        else:
            argmode = 'quiet'
            print("Nothing is selected.")
            cmd_args.quiet = True
        
        main(argmode)

    # No-args, just run the program in 'quiet' as default.
    else:
        argmode = 'quiet'
        print("Quiet is selected.")
        main(argmode)
        cmd_args.quiet = True
