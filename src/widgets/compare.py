#!/usr/bin/python3
'''compare file'''

import logging
import os

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QImage, QPalette, QPixmap
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (
    QLabel, QLineEdit, QMessageBox, QPlainTextEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from src.fileType import TYPES, getFileType
from src.metaData import MetaData
from src.widgets.videoPlayer import VideoPlayer

TEMP_FOLDER = './TMP/'


# TODO: To consider renaming this ()
class Compare(QWidget):
    '''Compare class'''

    def __init__(self, fileFullPath, parent=None):
        super(Compare, self).__init__(parent)
        self.fileFullPath = fileFullPath
        self.fileBaseName = os.path.basename(self.fileFullPath)
        self.tmpFileFullPath = TEMP_FOLDER + self.fileBaseName

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
        self.label = QLabel()
        self.videoPlayer = VideoPlayer()
        self.lineEdit = QLineEdit()
        self.plainTextEdit = QPlainTextEdit()
        self.deleteButton = QPushButton("Delete")
        self.undoButton = QPushButton("Undo")

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

        self.plainTextEdit.setPlainText(plainTextEditText)
        self.plainTextEdit.setFixedHeight(300)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.deleteButton.clicked.connect(self.handleDelete)
        self.deleteButton.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.undoButton.clicked.connect(self.handleUndo)
        self.undoButton.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def initLayout(self):
        '''Compare initLayout'''
        self.vBoxLayout = QVBoxLayout()
        self.setLayout(self.vBoxLayout)

    def updateLayout(self):
        '''Compare updateLayout'''
        self.vBoxLayout.addWidget(
            self.label, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addWidget(
            self.videoPlayer, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addWidget(
            self.lineEdit, Qt.AlignmentFlag.AlignCenter)
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
            self.undoButton.setDisabled(True)
        else:
            self.deleteButton.setDisabled(True)
            self.undoButton.setEnabled(True)

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
                self.image = QImage(file)

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
