#!/usr/bin/python3
'''main module'''

import faulthandler
import logging
import os
import sys
import tempfile

from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QErrorMessage, QFileDialog)
from PyQt6.QtCore import QDir


from src.widgets.mainWindow import MainWindow
from src.defines import (
    APP_NAME, COULD_NOT_FIND_RESULTS_FILE, DEBUG_LOG_FILE_NAME,
    DEFAULT_RESULTS_FULL_FILE_PATH, LOGS_FOLDER_NAME, TEMP_FOLDER_NAME)

# TODO: fix pylint issue with venv modules


faulthandler.enable()


def getResultsXMLFileFullPath():
    '''getResultsXMLFileFullPath function'''
    # If the file exists in the default location we just load this file
    if os.path.isfile(DEFAULT_RESULTS_FULL_FILE_PATH):
        return DEFAULT_RESULTS_FULL_FILE_PATH

    # Otherwise we start dialog in order to let the user
    # select the relevant 'results.dupeguru' file
    fileDialog = QFileDialog()
    fileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    fileDialog.setFilter(QDir.Filter.Files)
    fileDialog.setNameFilter("dupGuru (*.dupeguru)")
    # fileDialog.set
    openFileURL = fileDialog.getOpenFileUrl()
    logging.debug(
        "MainWindow init openFileUrl=%s", openFileURL)

    # in case that the user haven't picked a proper file
    if openFileURL[0].isLocalFile():
        return openFileURL[0].toLocalFile()

    errorMessage = QErrorMessage()
    errorMessage.showMessage(
        COULD_NOT_FIND_RESULTS_FILE)

    sys.exit()


def initTempDir():
    '''initTempDir function'''
    tempDir = tempfile.gettempdir()
    logging.debug("main tempDir=%s", tempDir)

    appTempDirPath = Path(tempDir, APP_NAME)
    if not os.path.isdir(appTempDirPath):
        os.mkdir(appTempDirPath)

    logsTempDirPath = Path(tempDir, APP_NAME, LOGS_FOLDER_NAME)
    if not os.path.isdir(logsTempDirPath):
        os.mkdir(logsTempDirPath)

    tempTempDirPath = Path(tempDir, APP_NAME, TEMP_FOLDER_NAME)
    if not os.path.isdir(tempTempDirPath):
        os.mkdir(tempTempDirPath)

    return tempDir


def main():
    '''main function'''
    tempDir = initTempDir()

    debugLogsFileFullPath = Path('./', LOGS_FOLDER_NAME, DEBUG_LOG_FILE_NAME)
    # debugLogsFileFullPath = Path(
    #     tempDir, APP_NAME, LOGS_FOLDER_NAME, DEBUG_LOG_FILE_NAME)
    print("logfile:", debugLogsFileFullPath)

    logging.basicConfig(filename=debugLogsFileFullPath,
                        encoding='utf-8', level=logging.NOTSET, force=True)
    logger = logging.getLogger(__name__)
    logger.info('init log file')

    app = QApplication(sys.argv)
    mainWindow = MainWindow(getResultsXMLFileFullPath())
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

# TODO: To compile this to linux(deb), mac(dmg), window(exe) files
