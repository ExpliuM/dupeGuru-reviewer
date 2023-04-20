
#!/usr/bin/python3
'''VideoPlayer module'''

import logging

from PyQt6.QtCore import Qt, QTime, QUrl
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (
    QHBoxLayout, QLineEdit, QMessageBox,
    QPushButton, QSlider, QStyle, QVBoxLayout, QWidget)

AUDIO_DEFAULT_VOLUME = 0.0

LABEL_DEFAULT_WIDTH = 70
LABEL_DEFAULT_VALUE = '00:00:00'


class VideoPlayer(QWidget):
    '''VideoPlayer class'''
    # TODO: To tighten it up

    def __init__(self, parent=None):
        # TODO: to split this method to multiple init methods
        super(VideoPlayer, self).__init__(parent)
        # State attributes
        self.fullScreen = False
        self.oldPosition = None
        self.controlLayout = None

        # Widgets
        self.audioOutput = None
        self.endLabel = None
        self.label = None
        self.mediaPlayer = None
        self.playButton = None
        self.video = None

        self.initIcons()
        self.initWidgets()
        self.configWidgets()
        self.initControlLayout()
        self.initLayout()
        self.initConnections()

    # Initializers

    def initConnections(self):
        '''VideoPlayer initConnections method'''
        self.endLabel.selectionChanged.connect(
            lambda: self.endLabel.setSelection(0, 0))
        self.label.selectionChanged.connect(
            lambda: self.label.setSelection(0, 0))
        self.playButton.clicked.connect(self.play)
        self.positionSlider.sliderMoved.connect(self.mediaPlayer.setPosition)
        self.mediaPlayer.playbackStateChanged.connect(
            self.playbackStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.errorChanged.connect(self.errorChanged)

    def initControlLayout(self):
        '''VideoPlayer initControlLayout method'''
        self.controlLayout = QHBoxLayout()
        self.controlLayout.setContentsMargins(5, 0, 5, 0)
        self.controlLayout.addWidget(self.playButton)
        self.controlLayout.addWidget(self.label)
        self.controlLayout.addWidget(self.positionSlider)
        self.controlLayout.addWidget(self.endLabel)

    def initIcons(self):
        '''VideoPlayer initIcons method'''
        self.pauseIcon = QStyle.StandardPixmap.SP_MediaPause
        self.playIcon = QStyle.StandardPixmap.SP_MediaPlay
        self.stopIcon = QStyle.StandardPixmap.SP_MediaStop
        self.volumeIcon = QStyle.StandardPixmap.SP_MediaVolume
        self.volumeMutedIcon = QStyle.StandardPixmap.SP_MediaVolumeMuted

    def initLayout(self):
        '''VideoPlayer initLayout method'''
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.video)
        layout.addLayout(self.controlLayout)

        self.setLayout(layout)

    def initWidgets(self):
        '''VideoPlayer initWidgets method'''
        self.audioOutput = QAudioOutput()
        self.endLabel = QLineEdit(LABEL_DEFAULT_VALUE)
        self.label = QLineEdit(LABEL_DEFAULT_VALUE)
        self.mediaPlayer = QMediaPlayer()
        self.playButton = QPushButton()
        self.positionSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.video = QVideoWidget()

    def configWidgets(self):
        '''VideoPlayer configWidgets method'''
        self.label.setFixedWidth(LABEL_DEFAULT_WIDTH)
        self.label.setReadOnly(True)
        self.label.setUpdatesEnabled(True)

        self.endLabel.setFixedWidth(LABEL_DEFAULT_WIDTH)
        self.endLabel.setReadOnly(True)
        self.endLabel.setUpdatesEnabled(True)

        self.playButton.setEnabled(False)
        self.playButton.setFixedWidth(32)

        self.playButton.setIcon(self.style().standardIcon(self.playIcon))

        self.positionSlider.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.positionSlider.setPageStep(20)
        self.positionSlider.setRange(0, 100)
        self.positionSlider.setSingleStep(2)

        self.audioOutput.setVolume(AUDIO_DEFAULT_VOLUME)

        self.mediaPlayer.setAudioOutput(self.audioOutput)
        self.mediaPlayer.setVideoOutput(self.video)

    # Change handlers
    def durationChanged(self, duration: int):
        '''VideoPlayer durationChanged method'''
        self.positionSlider.setRange(0, duration)
        time = QTime(0, 0, 0, 0)
        time = time.addMSecs(self.mediaPlayer.duration())
        self.endLabel.setText(time.toString())

    def errorChanged(self, errorMessage: str):
        '''VideoPlayer handleError method'''
        self.playButton.setEnabled(False)
        logging.error(errorMessage)
        self.errorbox(errorMessage)

    def playbackStateChanged(self, state: QMediaPlayer.PlaybackState):
        '''VideoPlayer mediaStateChanged method'''
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(self.playIcon))
        else:
            self.playButton.setIcon(self.style().standardIcon(self.pauseIcon))

    def positionChanged(self, position: int):
        '''VideoPlayer positionChanged method'''
        self.positionSlider.setValue(position)
        time = QTime(0, 0, 0, 0)
        time = time.addMSecs(self.mediaPlayer.position())
        self.label.setText(time.toString())

    # Event handlers

    def mousePressEvent(self, event: QMouseEvent):
        '''VideoPlayer mousePressEvent method'''
        super(VideoPlayer, self).mousePressEvent(event)

        self.oldPosition = event.position()

    def mouseMoveEvent(self, event: QMouseEvent):
        '''VideoPlayer mouseMoveEvent method'''
        super(VideoPlayer, self).mouseMoveEvent(event)

        delta = event.position() - self.oldPosition
        self.move(round(self.x() + delta.x()), round(self.y() + delta.y()))
        self.oldPosition = event.position()

    # Methods
    # TODO: To add types to methods
    def errorbox(self, message: str):
        '''VideoPlayer errorbox method'''
        msg = QMessageBox(2, "Error", message, QMessageBox.Ok)
        msg.exec()

    def openFile(self, fileFullPath: str):
        '''VideoPlayer openFile method'''
        fileURL = QUrl.fromLocalFile(fileFullPath)
        if not fileURL.isLocalFile():
            logging.error("")
            return

        self.mediaPlayer.setSource(fileURL)
        self.playButton.setEnabled(True)

    def play(self):
        '''VideoPlayer play method'''
        if self.mediaPlayer.isPlaying():
            self.mediaPlayer.pause()
            return

        self.mediaPlayer.play()
