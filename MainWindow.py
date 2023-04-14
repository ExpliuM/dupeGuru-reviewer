#!/usr/bin/python3

# from pathlib import Path
import resultsXML
from widget import Widget
from defines import \
    COULD_NOT_FIND_RESULTS_FILE, \
    DEFAULT_RESULTS_FULL_FILE_PATH
import sys
import os
import logging
import faulthandler
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QFileDialog
from PyQt6.QtGui import QKeyEvent, QKeySequence
from PyQt6.QtWidgets import \
    QErrorMessage, \
    QHBoxLayout, \
    QMainWindow, \
    QPushButton, \
    QVBoxLayout, \
    QWidget

faulthandler.enable()

MAC_LEFT_ARROW_KEY = 16777234
MAC_RIGHT_ARROW_KEY = 16777236

resultsXMLFileFullPath = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resultsXMLObj = resultsXML.ResultsXML(
            resultsXMLFileFullPath)
        self.groups = self.resultsXMLObj.getGroups()
        self.groupsLen = self.groups.__len__()
        self.groupIndex = 0

        self.paths = self.groups[self.groupIndex].getPaths()

        self.previousButton = QPushButton("previous")
        self.previousButton.clicked.connect(self.handlePrevious)

        self.nextButton = QPushButton("Next")
        self.nextButton.clicked.connect(self.handleNext)

        self.horizontalImageWidgetsWidget = QWidget()

        self.createUI()

        self.nextButton.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.previousButton.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.setWindowTabOrder()
        self.nextButton.setFocus()

    def setWindowTabOrder(self):
        imageWidgetsCount = self.horizontalImageWidgetsLayout.count()
        if (imageWidgetsCount > 0):
            widget1 = self.horizontalImageWidgetsLayout.itemAt(0).widget()

            self.setTabOrder(
                self.nextButton, self.horizontalImageWidgetsLayout.itemAt(0).widget())

            for i in reversed(range(self.horizontalImageWidgetsLayout.count()-1)):
                widget1 = self.horizontalImageWidgetsLayout.itemAt(i).widget()
                widget2 = self.horizontalImageWidgetsLayout.itemAt(
                    i+1).widget()

                self.setTabOrder(self.horizontalImageWidgetsLayout.itemAt(
                    i).widget(),  self.horizontalImageWidgetsLayout.itemAt(i+1).widget())

            self.setTabOrder(self.horizontalImageWidgetsLayout.itemAt(
                imageWidgetsCount-1).widget(),  self.previousButton)

        self.setTabOrder(self.previousButton, self.nextButton)

    def keyPressEvent(self, event: QKeyEvent):
        if (event.matches(QKeySequence.StandardKey.Quit)
                or event.matches(QKeySequence.StandardKey.Close)):
            self.close()

        super(MainWindow, self).keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent):
        key = event.key()
        if key == MAC_RIGHT_ARROW_KEY:
            self.handleNext()
            self.nextButton.setFocus()

        elif key == MAC_LEFT_ARROW_KEY:
            self.handlePrevious()
            self.previousButton.setFocus()

        super(MainWindow, self).keyReleaseEvent(event)

    def createUI(self):
        self.horizontalImageWidgetsLayout = QHBoxLayout()

        for path in self.paths:
            self.horizontalImageWidgetsLayout.addWidget(
                Widget(path))

        self.horizontalImageWidgetsWidget.setLayout(
            self.horizontalImageWidgetsLayout)

        self.horizontalButtonWidget = QWidget()

        self.horizontalButtonBoxLayout = QHBoxLayout()
        self.horizontalButtonBoxLayout.addWidget(self.previousButton)
        self.horizontalButtonBoxLayout.addWidget(self.nextButton)
        self.horizontalButtonWidget.setLayout(self.horizontalButtonBoxLayout)

        self.centralWidget = QWidget()

        self.centralWidgetLayout = QVBoxLayout()
        self.centralWidgetLayout.addWidget(self.horizontalImageWidgetsWidget)
        self.centralWidgetLayout.addWidget(self.horizontalButtonWidget)
        self.centralWidget.setLayout(self.centralWidgetLayout)
        self.setCentralWidget(self.centralWidget)

        self.showMaximized()

    def updateUI(self):
        for i in reversed(range(self.horizontalImageWidgetsLayout.count())):
            self.horizontalImageWidgetsLayout.itemAt(
                i).widget().setParent(None)

        for path in self.paths:
            self.horizontalImageWidgetsLayout.addWidget(
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


def openResultsFile():
    global resultsXMLFileFullPath
    # If the file exists in the default location we just load this file
    if (os.path.isfile(DEFAULT_RESULTS_FULL_FILE_PATH)):
        resultsXMLFileFullPath = DEFAULT_RESULTS_FULL_FILE_PATH

    else:
        # Otherwise we start dialog in order to let the user
        # select the relevant 'results.dupeguru' file
        fileDialog = QFileDialog()
        # fileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        # fileDialog.setFilter(QDir.Filter.Files)
        fileDialog.setNameFilter("*.dupeguru1")
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

    openResultsFile()

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

# TODO: To compile this to linux(deb), mac(dmg), window(exe) files