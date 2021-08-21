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
    """
    Converts string to a boolean value.

    Parameters
    ----------
        v : str
            String input to be converted to a boolean.
        
    Returns
    -------
        Returns boolean value based on the string provided.
    """
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
                    required = False,
                    metavar = '',
                    help = 'Do not save log file.')

parser.add_argument('-r', '--rate',
                    type = int,
                    choices = [8000, 16000, 32000, 44100, 48000],
                    default = 44100,
                    required = False,
                    help = 'Sample rate of audio input.')

parser.add_argument('-f', '--log-filename',
                    type = str,
                    default = None,
                    required = False,
                    help = 'File name of the log output.')

group = parser.add_mutually_exclusive_group()
group.add_argument('-q', '--quiet', action = 'store_true', help = 'Quiet mode.')
group.add_argument('-v', '--verbose', action = 'store_true', help = 'Verbose mode.')

cmd_args = parser.parse_args()


def main():
    """
    Main function of the application.

    Parameters
    ----------
        None

    Returns
    -------
        None
    """
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    cmd_args_dict = vars(cmd_args)
    arg_quiet     = cmd_args_dict['quiet']
    arg_verbose   = cmd_args_dict['verbose']
    arg_nologs    = cmd_args_dict['no_log_save']
    arg_rate      = cmd_args_dict['rate']
    arg_filename  = cmd_args_dict['log_filename']
    
    # List of arguments to be passed to main window:
    args_list = [arg_quiet, arg_verbose, arg_nologs, arg_rate, arg_filename]

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
