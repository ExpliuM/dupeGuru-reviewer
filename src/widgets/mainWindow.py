#!/usr/bin/python3
'''mainWindow module'''

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent, QKeySequence
from PyQt6.QtWidgets import (
    QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget)

from src.objects.resultsXML import resultsXML
from src.widgets.compare import Compare


class MainWindow(QMainWindow):
    '''MainWindow class'''

    def __init__(self, resultsXMLFileFullPath):
        super().__init__()

        self.nextButton = None
        self.previousButton = None

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
        '''initwidgets method'''
        self.hButtonWidget = QWidget()
        self.hWidgetsWidget = QWidget()
        self.windowWidget = QWidget()

        self.setCentralWidget(self.windowWidget)

    def initFocusPolicy(self):
        '''initfocuspolicy method'''
        self.nextButton.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.previousButton.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.setWindowTabOrder()
        self.nextButton.setFocus()

    def initButtons(self):
        '''initButtons method'''
        self.previousButton = QPushButton("previous")
        self.previousButton.clicked.connect(self.handlePrevious)

        self.nextButton = QPushButton("Next")
        self.nextButton.clicked.connect(self.handleNext)

    def setWindowTabOrder(self):
        '''setWindowTabOrder method'''
        widgetsCount = self.hWidgetsLayout.count()
        if widgetsCount > 0:
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
        '''keyPressEvent method'''
        if (event.matches(QKeySequence.StandardKey.Quit)
                or event.matches(QKeySequence.StandardKey.Close)):
            self.close()

        super(MainWindow, self).keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent):
        '''keyReleaseEvent method'''
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
        '''initLayouts method'''
        self.hWidgetsLayout = QHBoxLayout()

        for path in self.paths:
            self.hWidgetsLayout.addWidget(
                Compare(path))

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
        '''updateUI'''
        for i in reversed(range(self.hWidgetsLayout.count())):
            self.hWidgetsLayout.itemAt(
                i).widget().setParent(None)

        for path in self.paths:
            self.hWidgetsLayout.addWidget(
                Compare(path))

        self.setWindowTabOrder()

    def handleNext(self):
        '''handleNext method'''

        if self.groupIndex < self.groupsLen:
            self.groupIndex += 1
            self.paths = self.groups[self.groupIndex].getPaths()
            self.updateUI()

    def handlePrevious(self):
        '''handlePrevious method'''
        if self.groupIndex:
            self.groupIndex -= 1
            self.paths = self.groups[self.groupIndex].getPaths()
            self.updateUI()
