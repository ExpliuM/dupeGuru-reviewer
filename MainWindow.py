#!/usr/bin/python3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget


import defines
import imageWidget
import os
import resultsXML
import subprocess
import sys

from pathlib import Path

# # Load external module
# sys.path.append("modules/dupeguru")

# # from core.scanner import Scanner
# from core import directories
# from core.scanner import Scanner, ScanType

MAC_LEFT_ARROW_KEY = 16777234
MAC_RIGHT_ARROW_KEY = 16777236


class MainWindow(QMainWindow):
    def __init__(self):

        super().__init__()

        if (not os.path.isfile(defines.RESULTS_FULL_FILE_PATH)):
          # wd = os.getcwd()
          # os.chdir('./modules/dupeguru/')
          # print(subprocess.call("ls"))
          # p = subprocess.call('puthon run.py')
          # os.chdir(wd)

          p = subprocess.call('python3 ./modules/dupeguru/run.py')
          p.wait()

        if (os.path.isfile(defines.RESULTS_FULL_FILE_PATH)):
          self.resultsXMLObj = resultsXML.ResultsXML(defines.RESULTS_FULL_FILE_PATH)
          self.groups = self.resultsXMLObj.getGroups()
          self.groupsLen = self.groups.__len__()
          self.groupIndex = 0

          self.paths = self.groups[self.groupIndex].getPaths()
        else:
          # scanner = Scanner()

          # scanner.scan_type = ScanType.FOLDERS
          # dirs = directories.Directories()
          # print(dirs)
          # dirs.add_path(Path('/Users/explium/OneDrive - Technion/Pictures/'))
          # files = list(dirs.get_folders())
          # print(scanner.get_dupe_groups(files))
          
          self.paths = []

        self.previousButton = QPushButton("previous")
        self.previousButton.clicked.connect(self.handlePrevious)

        self.nextButton = QPushButton("Next")
        self.nextButton.clicked.connect(self.handleNext)

        self.horizontalImageWidgetsWidget = QWidget()

        self.createUI()

        self.nextButton.setFocusPolicy(Qt.StrongFocus)
        self.previousButton.setFocusPolicy(Qt.StrongFocus)

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

                print("i", i, "widget1", widget1, "widget2", widget2)

                self.setTabOrder(self.horizontalImageWidgetsLayout.itemAt(
                    i).widget(),  self.horizontalImageWidgetsLayout.itemAt(i+1).widget())

            self.setTabOrder(self.horizontalImageWidgetsLayout.itemAt(
                imageWidgetsCount-1).widget(),  self.previousButton)

        self.setTabOrder(self.previousButton, self.nextButton)

    def keyPressEvent(self, event):
        key = event.key()
        print("keyPressEvent", "key=",
              key)

        super(MainWindow, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        key = event.key()
        print("keyReleaseEvent", "key=",
              key, "Qt.LeftArrow=", Qt.LeftArrow, "Qt.RightArrow", Qt.RightArrow)
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
                imageWidget.ImageWidget(path))

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
                imageWidget.ImageWidget(path))

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


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
