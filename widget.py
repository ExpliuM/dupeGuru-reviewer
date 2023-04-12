#!/usr/bin/python3


from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QImage, QPalette, QPixmap
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import \
    QLabel, \
    QLineEdit, \
    QMessageBox, \
    QPlainTextEdit,\
    QPushButton,\
    QScrollArea,\
    QSizePolicy,\
    QVBoxLayout, \
    QWidget

from fileType import TYPES, getFileType

import metaData
import os

TEMP_FOLDER = './TMP/'


class Widget(QWidget):
    def __init__(self, fileFullPath):
        super().__init__()
        self.fileFullPath = fileFullPath
        self.fileBaseName = os.path.basename(self.fileFullPath)
        self.tmpFileFullPath = TEMP_FOLDER + self.fileBaseName

        self.initGraphics(fileFullPath, '')

        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setVideoOutput(self.video)

        self.loadData()

        self.updateButtons()

        self.setTabOrder(self.deleteButton, self.undoButton)

    def initGraphics(self, LineEditText, plainTextEditText):
        self.label = QLabel()
        self.label.setBackgroundRole(QPalette.ColorRole.Base)
        self.label.setSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.label.setScaledContents(True)

        self.video = QVideoWidget()
        self.video.setVisible(False)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.ColorRole.Dark)
        self.scrollArea.setWidget(self.label)
        self.scrollArea.setVisible(False)

        self.lineEdit = QLineEdit()
        self.lineEdit.setText(LineEditText)
        self.lineEdit.setReadOnly(True)
        # self.lineEdit.setDragEnabled(True)
        # self.lineEdit.setEnabled(True)

        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setPlainText(plainTextEditText)
        self.plainTextEdit.setFixedHeight(300)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.handleDelete)
        self.deleteButton.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.undoButton = QPushButton("Undo")
        self.undoButton.clicked.connect(self.handleUndo)
        self.undoButton.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.verticalBoxLayout = QVBoxLayout()
        self.verticalBoxLayout.addWidget(
            self.label, Qt.AlignmentFlag.AlignCenter)
        self.verticalBoxLayout.addWidget(
            self.video, Qt.AlignmentFlag.AlignCenter)
        self.verticalBoxLayout.addWidget(
            self.lineEdit, Qt.AlignmentFlag.AlignCenter)
        self.verticalBoxLayout.addWidget(
            self.plainTextEdit, Qt.AlignmentFlag.AlignCenter)
        self.verticalBoxLayout.addWidget(
            self.deleteButton, Qt.AlignmentFlag.AlignCenter)
        self.verticalBoxLayout.addWidget(
            self.undoButton, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.verticalBoxLayout)

    def updateButtons(self):
        if os.path.exists(self.fileFullPath):
            self.deleteButton.setEnabled(True)
            self.undoButton.setDisabled(True)
        else:
            self.deleteButton.setDisabled(True)
            self.undoButton.setEnabled(True)

    def loadData(self):
        file = False
        if os.path.exists(self.tmpFileFullPath):
            file = self.tmpFileFullPath

        if os.path.exists(self.fileFullPath):
            file = self.fileFullPath

        if file:
            print("file", file)
            fileType = getFileType(file)
            print("fileType", fileType)
            if fileType is TYPES.IMAGE:
                image = QImage(file)
                if image.isNull():
                    QMessageBox.information(
                        self, "Image Viewer", "Cannot load %s." % file)
                    return

                self.label.setPixmap(QPixmap.fromImage(image))
                self.label.resize(self.label.pixmap().size())
                self.label.adjustSize()

                self.metaData = metaData.metaData(file)
                self.plainTextEdit.setPlainText(self.metaData.getMetaData())

            elif fileType is TYPES.VIDEO:
                self.mediaPlayer.setSource(QUrl.fromLocalFile(file))

                self.label.setVisible(False)
                self.video.setVisible(True)

                self.mediaPlayer.play()

                self.metaData = metaData.metaData(file)
                self.plainTextEdit.setPlainText(self.metaData.getMetaData())
            else:
                print("files other than images or videos are not supported")

    def handleDelete(self):
        print("fileBaseName", self.fileBaseName)
        print("handleDelete: " + self.fileFullPath)

        if os.path.exists(self.fileFullPath):
            os.rename(self.fileFullPath,
                      self.tmpFileFullPath)
        else:
            print("The file " + self.fileFullPath+" does not exist")

        self.updateButtons()

        self.loadData()

    def handleUndo(self):
        if os.path.exists(self.tmpFileFullPath):
            os.rename(self.tmpFileFullPath,
                      self.fileFullPath)
        else:
            print("The file " + self.tmpFileFullPath+" does not exist")

        self.updateButtons()

        self.loadData()
