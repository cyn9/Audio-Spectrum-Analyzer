from datetime import datetime

import os


def saveLog(statusText, fname):
    date = datetime.now()

    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Check if filename is None or passed by user in the command
    # line. If not passed explicitly, set filename to timestamp.
    # The extension is text file (.txt).
    if fname is None:
        filename_log = date.strftime('logs/%Y-%m-%d_%H-%M-%S-Log.txt')
    else:
        filename_log = 'logs/' + fname + '.txt'

    f = open(filename_log, "x")
    f.write(statusText.toPlainText())

    print(f"Log file written.")
    f.close()
