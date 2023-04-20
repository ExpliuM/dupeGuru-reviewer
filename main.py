#!/usr/bin/python3
'''main module'''

import faulthandler
import logging
import os
import sys

from PyQt6.QtWidgets import (
    QApplication,QErrorMessage,QFileDialog)
from PyQt6.QtCore import QDir


from src.widgets.mainWindow import MainWindow
from src.defines import (
    COULD_NOT_FIND_RESULTS_FILE, DEFAULT_RESULTS_FULL_FILE_PATH)

# TODO: fix pylint issue with venv modules


faulthandler.enable()


def getResultsFile():
    '''getresultsfile function'''
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


def main():
    '''main function'''
    logging.basicConfig(
        filename='logs/debugs.log', encoding='utf-8', level=logging.DEBUG)

    app = QApplication(sys.argv)
    mainWindow = MainWindow(getResultsFile())
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

# TODO: To compile this to linux(deb), mac(dmg), window(exe) files
