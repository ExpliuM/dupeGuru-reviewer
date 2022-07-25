#!/usr/bin/python3


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPalette
from PyQt5.QtWidgets import QApplication, QClipboard
from PyQt5.QtWidgets import QWidget, QLabel, QSizePolicy, QMessageBox, QPushButton, QVBoxLayout, QScrollArea, QPlainTextEdit, QLineEdit

import imageMetaData
import os
import sys

TEMP_FOLDER = './TMP/'


class ImageWidget(QWidget):
    def __init__(self, fileFullPath):
        super().__init__()
        self.fileFullPath = fileFullPath
        self.fileBaseName = os.path.basename(self.fileFullPath)
        self.tmpFileFullPath = TEMP_FOLDER + self.fileBaseName

        self.initGraphics(fileFullPath, '')

        self.loadImage()

        self.updateButtons()

        self.setTabOrder(self.deleteButton, self.undoButton)

    def initGraphics(self, LineEditText, plainTextEditText):
        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(False)

        self.lineEdit = QLineEdit()
        self.lineEdit.setText(LineEditText)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setEnabled(False)

        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setPlainText(plainTextEditText)
        self.plainTextEdit.setFixedHeight(300)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setFocusPolicy(Qt.NoFocus)

        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.handleDelete)
        self.deleteButton.setFocusPolicy(Qt.StrongFocus)

        self.undoButton = QPushButton("Undo")
        self.undoButton.clicked.connect(self.handleUndo)
        self.undoButton.setFocusPolicy(Qt.StrongFocus)

        self.verticalBoxLayout = QVBoxLayout()
        self.verticalBoxLayout.addWidget(self.imageLabel, Qt.AlignCenter)
        self.verticalBoxLayout.addWidget(self.lineEdit, Qt.AlignCenter)
        self.verticalBoxLayout.addWidget(self.plainTextEdit, Qt.AlignCenter)
        self.verticalBoxLayout.addWidget(self.deleteButton, Qt.AlignCenter)
        self.verticalBoxLayout.addWidget(self.undoButton, Qt.AlignCenter)
        self.setLayout(self.verticalBoxLayout)

    def updateButtons(self):
        if os.path.exists(self.fileFullPath):
            self.deleteButton.setEnabled(True)
            self.undoButton.setDisabled(True)
        else:
            self.deleteButton.setDisabled(True)
            self.undoButton.setEnabled(True)

    def loadImage(self):
        file = False
        if os.path.exists(self.tmpFileFullPath):
            file = self.tmpFileFullPath

        if os.path.exists(self.fileFullPath):
            file = self.fileFullPath

        if file:
            image = QImage(file)
            if image.isNull():
                QMessageBox.information(
                    self, "Image Viewer", "Cannot load %s." % file)
                return

            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            self.imageLabel.resize(self.imageLabel.pixmap().size())
            self.imageLabel.adjustSize()

            self.imageMetaData = imageMetaData.ImageMetaData(file)
            self.plainTextEdit.setPlainText(self.imageMetaData.getMetaData())

    def handleDelete(self):
        print("fileBaseName", self.fileBaseName)
        print("handleDelete: " + self.fileFullPath)

        if os.path.exists(self.fileFullPath):
            os.rename(self.fileFullPath,
                      self.tmpFileFullPath)
        else:
            print("The file " + self.fileFullPath+" does not exist")

        self.updateButtons()

        self.loadImage()

    def handleUndo(self):
        if os.path.exists(self.tmpFileFullPath):
            os.rename(self.tmpFileFullPath,
                      self.fileFullPath)
        else:
            print("The file " + self.tmpFileFullPath+" does not exist")

        self.updateButtons()

        self.loadImage()


def main():
    app = QApplication(sys.argv)
    imageWidget = ImageWidget(
        '/Users/explium/OneDrive - Technion/Pictures/Miscellaneous/Mom/01/(01).JPG')
    imageWidget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
