from datetime import datetime

import os


def saveLog(statusText):
    date = datetime.now()

    if not os.path.exists('logfiles'):
        os.makedirs('logfiles')

    filename_log = date.strftime('logfiles/%Y-%m-%d_%H-%M-%S-Log.txt')

    f = open(filename_log, "x")
    f.write(statusText.toPlainText())

    print(f"Log file written.")
    f.close()
