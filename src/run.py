'''
    @ author        cico
    @ version       5.0
    @ date          08/18/21
    @ time          2:53 PM
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

# Argument boolean parse for --no-log-save
# string to boolean conversion: 
def strToBool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1', ' '):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected...") 


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

parser.add_argument('-n', '--no-log-save',
                    type = strToBool,
                    nargs = '?',
                    const = True,
                    default = False,
                    metavar = '',
                    help = 'Do not save log file.')

group = parser.add_mutually_exclusive_group()
group.add_argument('-q', '--quiet', action = 'store_true', help = 'Print quiet.')
group.add_argument('-v', '--verbose', action = 'store_true', help = 'Print verbose.')

cmd_args = parser.parse_args()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    cmd_args_dict = vars(cmd_args)
    arg_quiet = cmd_args_dict['quiet']
    arg_verbose = cmd_args_dict['verbose']
    arg_nologs = cmd_args_dict['no_log_save']
    args_list = [arg_quiet, arg_verbose, arg_nologs]

    main = MainWindow(cmd_args = args_list)
    main.show()

    # Welcome message:
    welcomeMsgStyle = QApplication.style()
    welcomeMsg = QMessageBox()
    welcomeMsg.setWindowTitle("Hi!")
    welcomeMsg.setIcon(QMessageBox.Information)
    welcomeMsg.setText('Welcome to Real-Time Audio Analyzer. Please refer to "Help" section for further information. Press OK to start.')
    welcomeMsg.setWindowIcon(QtGui.QIcon(welcomeMsgStyle.standardIcon(QStyle.SP_DialogApplyButton)))
    welcomeMsg.exec_()

    # Start animation for real-time plotting.
    main.animation()

    # sys.exit(app.exec_())


if __name__ == '__main__':
    if float(sys.version_info[0]) < 3.0:
        raise Exception("Must be using Python 3 or newer.")

    if (len(sys.argv) > 1):
        if cmd_args.quiet:
            cmd_args.quiet = True

        elif cmd_args.verbose:
            cmd_args.verbose = True

        else:
            cmd_args.quiet = True
        
    # No-args, just run the program in 'quiet' as default.
    else:
        cmd_args.quiet = True
    
    main()
