#!/usr/bin/python3
'''compare file'''

import logging
import os
import tempfile

from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (QImage, QPalette, QPixmap)
from PyQt6.QtWidgets import (QApplication,
                             QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPlainTextEdit,
                             QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from src.defines import APP_NAME, TEMP_FOLDER_NAME
from src.fileType import TYPES, getFileType
from src.metaData import MetaData
from src.widgets.videoPlayer import VideoPlayer

# TODO: To consider renaming this ()


class Compare(QWidget):
    '''Compare class'''

    def __init__(self, fileFullPath, parent=None):
        super(Compare, self).__init__(parent)
        self.fileFullPath = fileFullPath
        self.fileBaseName = os.path.basename(self.fileFullPath)

        tempDir = tempfile.gettempdir()
        self.tmpFileFullPath = Path(
            tempDir, APP_NAME, TEMP_FOLDER_NAME, self.fileBaseName)

        self.initWidgets()
        self.configWidgets(fileFullPath, '')

        self.initLayout()
        self.updateLayout()
        self.updateButtons()

        self.loadData()
        self.fillData()

        self.setTabOrder(self.deleteButton, self.undoButton)

    def initWidgets(self):
        '''Compare initWidgets'''
        self.copyButton = QPushButton("Copy")
        self.deleteButton = QPushButton("Delete")
        self.hSourceBox = QWidget()
        self.label = QLabel()
        self.lineEdit = QLineEdit()
        self.metaData = MetaData("")
        self.plainTextEdit = QPlainTextEdit()
        self.undoButton = QPushButton("Undo")
        self.videoPlayer = VideoPlayer()
        self.fileType = TYPES.OTHER

    def configWidgets(self, lineEditText, plainTextEditText):
        '''Compare configWidgets'''
        self.label.adjustSize()
        self.label.setBackgroundRole(QPalette.ColorRole.Base)
        self.label.setSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.label.setScaledContents(True)

        self.lineEdit.setText(lineEditText)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.copyButton.clicked.connect(self.handleCopy)
        self.copyButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.hSourceBox.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.plainTextEdit.setPlainText(plainTextEditText)
        self.plainTextEdit.setFixedHeight(300)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.deleteButton.clicked.connect(self.handleDelete)
        # self.deleteButton.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.undoButton.clicked.connect(self.handleUndo)
        # self.undoButton.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def initLayout(self):
        '''Compare initLayout'''
        self.hSourceBoxLayout = QHBoxLayout()
        self.hSourceBox.setLayout(self.hSourceBoxLayout)

        self.vBoxLayout = QVBoxLayout()
        self.setLayout(self.vBoxLayout)

    def updateLayout(self):
        '''Compare updateLayout'''
        self.hSourceBoxLayout.addWidget(
            self.lineEdit)
        self.hSourceBoxLayout.addWidget(
            self.copyButton)

        self.vBoxLayout.addWidget(
            self.label, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addWidget(
            self.videoPlayer, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addWidget(
            self.hSourceBox, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addWidget(
            self.plainTextEdit, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addWidget(
            self.deleteButton, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addWidget(
            self.undoButton, Qt.AlignmentFlag.AlignCenter)

    def updateButtons(self):
        '''Compare updateButtons method'''
        if os.path.exists(self.fileFullPath):
            self.deleteButton.setEnabled(True)
            self.deleteButton.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

            self.undoButton.setDisabled(True)
            self.undoButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        else:
            self.deleteButton.setDisabled(True)
            self.deleteButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            self.undoButton.setEnabled(True)
            self.undoButton.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def fillData(self):
        '''Compare fillData method'''
        self.plainTextEdit.setPlainText(self.metaData.getMetaData())

        if self.fileType is TYPES.IMAGE:
            self.pixmap = QPixmap.fromImage(self.image)
            self.label.setPixmap(self.pixmap)
            self.label.resize(self.pixmap.size())
            self.label.adjustSize()
            self.label.setVisible(True)
            self.videoPlayer.setVisible(False)

        elif self.fileType is TYPES.VIDEO:
            self.label.setVisible(False)
            self.videoPlayer.setVisible(True)

    def loadData(self):
        '''Compare loadData method'''
        file = False
        if os.path.exists(self.tmpFileFullPath):
            file = self.tmpFileFullPath

        if os.path.exists(self.fileFullPath):
            file = self.fileFullPath

        if file:
            self.fileType = getFileType(file)

            if self.fileType is TYPES.IMAGE:
                self.image = QImage(Path(file).as_posix())

                if self.image.isNull():
                    QMessageBox.information(
                        self, "Image Viewer", f"Cannot load ${file}")
                    return
                self.metaData = MetaData(file)

            elif self.fileType is TYPES.VIDEO:
                self.videoPlayer.openFile(file)
                self.videoPlayer.play()

                self.metaData = MetaData(file)
                self.plainTextEdit.setPlainText(self.metaData.getMetaData())
            else:
                logging.warning(
                    "files other than images or videos are not supported")

    def handleCopy(self):
        '''Compare handleCopy method'''
        clipboard = QApplication.clipboard()
        clipboard.setText(self.lineEdit.text())

    def handleDelete(self):
        '''Compare handleDelete method'''
        if os.path.exists(self.fileFullPath):
            os.rename(self.fileFullPath, self.tmpFileFullPath)
        else:
            logging.warning(
                "The file %s does not exist", self.fileFullPath)

        self.updateButtons()

    def handleUndo(self):
        '''Compare handleUndo method'''
        if os.path.exists(self.tmpFileFullPath):
            os.rename(self.tmpFileFullPath, self.fileFullPath)
        else:
            logging.warning(
                "The file %s does not exist", self.tmpFileFullPath)

        self.updateButtons()
