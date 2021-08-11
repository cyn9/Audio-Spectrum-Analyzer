from datetime import datetime

import os


def saveLog(statusText):
    date = datetime.now()

    if not os.path.exists('logs'):
        os.makedirs('logs')

    filename_log = date.strftime('logs/%Y-%m-%d_%H-%M-%S-Log.txt')

    f = open(filename_log, "x")
    f.write(statusText.toPlainText())

    print(f"Log file written.")
    f.close()
