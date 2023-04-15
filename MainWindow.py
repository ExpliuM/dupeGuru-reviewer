#!/usr/bin/python3

from defines import \
    COULD_NOT_FIND_RESULTS_FILE, \
    DEFAULT_RESULTS_FULL_FILE_PATH
from widget import Widget

import faulthandler
import logging
import os
import resultsXML
import sys

from PyQt6.QtCore import Qt, QDir
from PyQt6.QtGui import QKeyEvent, QKeySequence
from PyQt6.QtWidgets import \
    QApplication, \
    QErrorMessage, \
    QFileDialog, \
    QHBoxLayout, \
    QMainWindow, \
    QPushButton, \
    QVBoxLayout, \
    QWidget


faulthandler.enable()

resultsXMLFileFullPath = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initButtons()

        # TODO: separate functionality and data from gui
        self.resultsXMLObj = resultsXML.ResultsXML(
            resultsXMLFileFullPath)
        self.groups = self.resultsXMLObj.getGroups()
        self.groupsLen = self.groups.__len__()
        self.groupIndex = 0

        self.paths = self.groups[self.groupIndex].getPaths()

        self.initWidgets()
        self.initLayouts()

        self.initFocusPolicy()

        self.showMaximized()

    def initWidgets(self):
        self.windowWidget = QWidget()
        self.hButtonWidget = QWidget()
        self.hWidgetsWidget = QWidget()

        self.setCentralWidget(self.windowWidget)

    def initFocusPolicy(self):
        self.nextButton.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.previousButton.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.setWindowTabOrder()
        self.nextButton.setFocus()

    def initButtons(self):
        self.previousButton = QPushButton("previous")
        self.previousButton.clicked.connect(self.handlePrevious)

        self.nextButton = QPushButton("Next")
        self.nextButton.clicked.connect(self.handleNext)

    def setWindowTabOrder(self):
        widgetsCount = self.hWidgetsLayout.count()
        if (widgetsCount > 0):
            self.hWidgetsLayout.itemAt(0).widget()

            self.setTabOrder(
                self.nextButton, self.hWidgetsLayout.itemAt(0).widget())

            for i in reversed(range(self.hWidgetsLayout.count()-1)):
                self.hWidgetsLayout.itemAt(i).widget()
                self.hWidgetsLayout.itemAt(
                    i+1).widget()

                self.setTabOrder(self.hWidgetsLayout.itemAt(
                    i).widget(),  self.hWidgetsLayout.itemAt(i+1).widget())

            self.setTabOrder(self.hWidgetsLayout.itemAt(
                widgetsCount-1).widget(),  self.previousButton)

        self.setTabOrder(self.previousButton, self.nextButton)

    def keyPressEvent(self, event: QKeyEvent):
        if (event.matches(QKeySequence.StandardKey.Quit)
                or event.matches(QKeySequence.StandardKey.Close)):
            self.close()

        super(MainWindow, self).keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent):
        key = event.key()

        if key == Qt.Key.Key_Escape:
            self.close()

        if key == Qt.Key.Key_Right:
            self.handleNext()
            self.nextButton.setFocus()
            return

        elif key == Qt.Key.Key_Left:
            self.handlePrevious()
            self.previousButton.setFocus()
            return

        super(MainWindow, self).keyReleaseEvent(event)

    def initLayouts(self):
        self.hWidgetsLayout = QHBoxLayout()

        for path in self.paths:
            self.hWidgetsLayout.addWidget(
                Widget(path))

        self.hWidgetsWidget.setLayout(
            self.hWidgetsLayout)

        self.hButtonBoxLayout = QHBoxLayout()
        self.hButtonBoxLayout.addWidget(self.previousButton)
        self.hButtonBoxLayout.addWidget(self.nextButton)
        self.hButtonWidget.setLayout(self.hButtonBoxLayout)

        self.centralWidgetLayout = QVBoxLayout()
        self.centralWidgetLayout.addWidget(self.hWidgetsWidget)
        self.centralWidgetLayout.addWidget(self.hButtonWidget)
        self.windowWidget.setLayout(self.centralWidgetLayout)

    # TODO: to rename
    def updateUI(self):
        for i in reversed(range(self.hWidgetsLayout.count())):
            self.hWidgetsLayout.itemAt(
                i).widget().setParent(None)

        for path in self.paths:
            self.hWidgetsLayout.addWidget(
                Widget(path))

        self.setWindowTabOrder()

    def handleNext(self):
        if (self.groupIndex < self.groupsLen):
            self.groupIndex += 1
            self.paths = self.groups[self.groupIndex].getPaths()
            self.updateUI()

    def handlePrevious(self):
        if (self.groupIndex):
            self.groupIndex -= 1
            self.paths = self.groups[self.groupIndex].getPaths()
            self.updateUI()


def openResultsFile(app):
    global resultsXMLFileFullPath
    # If the file exists in the default location we just load this file
    if (os.path.isfile(DEFAULT_RESULTS_FULL_FILE_PATH)):
        resultsXMLFileFullPath = DEFAULT_RESULTS_FULL_FILE_PATH

    else:
        # Otherwise we start dialog in order to let the user
        # select the relevant 'results.dupeguru' file
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        fileDialog.setFilter(QDir.Filter.Files)
        fileDialog.setNameFilter("dupGguru (*.dupeguru)")
        # fileDialog.set
        openFileUrl = fileDialog.getOpenFileUrl()
        logging.debug("MainWindow init openFileUrl=%s",
                      openFileUrl)

        # in case that the user haven't picked a proper file
        if (openFileUrl[0].isLocalFile()):
            resultsXMLFileFullPath = openFileUrl[0].toLocalFile()
            return

        errorMessage = QErrorMessage()
        errorMessage.showMessage(
            COULD_NOT_FIND_RESULTS_FILE)

        sys.exit()


def main():
    logging.basicConfig(filename='logs/debugs.log',
                        encoding='utf-8', level=logging.DEBUG)

    app = QApplication(sys.argv)
    openResultsFile(app)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

# TODO: To compile this to linux(deb), mac(dmg), window(exe) files
