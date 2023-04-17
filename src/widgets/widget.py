#!/usr/bin/python3
'''widget file'''

import logging
import os

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QImage, QPalette, QPixmap
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import \
    QLabel, \
    QLineEdit, \
    QMessageBox, \
    QPlainTextEdit, \
    QPushButton, \
    QSizePolicy, \
    QVBoxLayout, \
    QWidget

from src.fileType import TYPES, getFileType
from src.metaData import MetaData

TEMP_FOLDER = './TMP/'


# TODO: To consider renaming this ()
class Widget(QWidget):
    '''Widget'''

    def __init__(self, fileFullPath):
        super().__init__()
        self.fileFullPath = fileFullPath
        self.fileBaseName = os.path.basename(self.fileFullPath)
        self.tmpFileFullPath = TEMP_FOLDER + self.fileBaseName

        self.initWidgets()
        self.configWidgets(fileFullPath, '')

        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setVideoOutput(self.video)

        self.initLayout()
        self.updateLayout()
        self.updateButtons()

        self.loadData()
        self.fillData()

        self.setTabOrder(self.deleteButton, self.undoButton)

    def initWidgets(self):
        '''initWidgets'''
        self.label = QLabel()
        self.video = QVideoWidget()
        self.lineEdit = QLineEdit()
        self.plainTextEdit = QPlainTextEdit()
        self.deleteButton = QPushButton("Delete")
        self.undoButton = QPushButton("Undo")

    def configWidgets(self, lineEditText, plainTextEditText):
        '''configWidgets'''
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
        '''initLayout'''
        self.vBoxLayout = QVBoxLayout()
        self.setLayout(self.vBoxLayout)

    def updateLayout(self):
        '''updateLayout'''
        self.vBoxLayout.addWidget(
            self.label, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addWidget(
            self.video, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addWidget(
            self.lineEdit, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addWidget(
            self.plainTextEdit, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addWidget(
            self.deleteButton, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addWidget(
            self.undoButton, Qt.AlignmentFlag.AlignCenter)

    def updateButtons(self):
        '''updateButtons'''
        if os.path.exists(self.fileFullPath):
            self.deleteButton.setEnabled(True)
            self.undoButton.setDisabled(True)
        else:
            self.deleteButton.setDisabled(True)
            self.undoButton.setEnabled(True)

    def fillData(self):
        '''fillData'''
        self.plainTextEdit.setPlainText(self.metaData.getMetaData())

        if self.fileType is TYPES.IMAGE:
            self.pixmap = QPixmap.fromImage(self.image)
            self.label.setPixmap(self.pixmap)
            self.label.resize(self.pixmap.size())
            self.label.adjustSize()
            self.label.setVisible(True)
            self.video.setVisible(False)

        elif self.fileType is TYPES.VIDEO:
            self.label.setVisible(False)
            self.video.setVisible(True)

    def loadData(self):
        '''loadData'''
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
                self.mediaPlayer.setSource(QUrl.fromLocalFile(file))

                self.mediaPlayer.play()

                self.metaData = MetaData(file)
                self.plainTextEdit.setPlainText(self.metaData.getMetaData())
            else:
                logging.warning(
                    "files other than images or videos are not supported")

    def handleDelete(self):
        '''handleDelete method'''
        if os.path.exists(self.fileFullPath):
            os.rename(self.fileFullPath,
                      self.tmpFileFullPath)
        else:
            logging.warning(
                "The file %s does not exist", self.fileFullPath)

        self.updateButtons()

    def handleUndo(self):
        '''handleUndo method'''
        if os.path.exists(self.tmpFileFullPath):
            os.rename(self.tmpFileFullPath,
                      self.fileFullPath)
        else:
            logging.warning(
                "The file %s does not exist", self.tmpFileFullPath)

        self.updateButtons()
