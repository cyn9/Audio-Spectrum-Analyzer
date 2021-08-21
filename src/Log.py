from datetime import datetime

import os


def saveLog(statusText, fname):
    """
    Saves a log file to "logs" folder. Log file is filled with the
    content of the status panel.

    Parameters
    ----------
        statusText : QTextBrowser
            Takes status text object as reference for readout.
        
        fname : str
            File name passed in the command-line by the user. If not
            specified, the default logfile name is created and based
            upon the current time instance when the file is being saved.
    
    Returns
    -------
        None
    """
    date = datetime.now()

    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Check if filename is None or passed by user in the command
    # line. If not passed explicitly, set filename to timestamp.
    # The extension is text file (.txt).
    if fname is None:
        filename_log = date.strftime('logs/%Y-%m-%d_%H-%M-%S-Log.txt')
    else:
        # First check if the user has specified the file extension
        # if yes, do not add "".txt"
        file_extension = '.txt'
        filename_log = 'logs/' + fname

        if not file_extension in fname:
            filename_log += file_extension
            print(filename_log)


    f = open(filename_log, "x")
    f.write(statusText.toPlainText())

    print(f"Log file written to {filename_log}.")
    f.close()
