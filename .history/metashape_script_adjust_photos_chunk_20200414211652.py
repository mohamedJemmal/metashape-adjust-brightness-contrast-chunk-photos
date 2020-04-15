import Metashape
from PySide2 import QtGui, QtCore, QtWidgets, QtPrintSupport


from PySide2.QtCore import QDir, Qt
from PySide2.QtGui import QImage, QPainter, QPalette, QPixmap
from PySide2.QtWidgets import (QAction, QApplication, QFileDialog, QLabel,
                               QMainWindow, QMenu, QMessageBox, QScrollArea, QSizePolicy)
from PySide2.QtPrintSupport import QPrintDialog, QPrinter


import datetime
import shapefile
import os
import shutil

from PIL import Image, ImageEnhance
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
# Checking compatibility
compatible_major_version = "1.6"
found_major_version = ".".join(Metashape.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
    raise Exception("Incompatible Metashape version: {} != {}".format(
        found_major_version, compatible_major_version))


class CopyChunkPhotosDlg(QtWidgets.QDialog):
    # path = ''
    # image = Image

    def __init__(self, parent):

        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle(
            "ADJUST PHOTOS BRIGHTNESS , CMG (MAROC)")
        self.setMinimumWidth(800)
        self.setMinimumHeight(400)
        # self.resize(1100, 850)
        self.adjustSize()

        self.createParamsGridLayout()
        self.createButtonsGridLayout()
        self.createImageViewerLayout()

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.groupBoxParams)
        vbox.addWidget(self.groupBoxViewer)
        vbox.addWidget(self.groupBoxButtons)

        self.setLayout(vbox)

        self.exec()

    def createImageViewerLayout(self):

        self.groupBoxViewer = QtWidgets.QGroupBox()

        gridViewerLayout = QtWidgets.QGridLayout()

        self.imageLabel = QtWidgets.QLabel(self)
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        path = "D:/copy/1/dji_0021"
        self.image = QtGui.QPixmap(path)
        self.imageLabel.setPixmap(self.image)

        gridViewerLayout.addWidget(self.imageLabel, 0, 0)

        self.groupBoxViewer.setLayout(gridViewerLayout)

    def createButtonsGridLayout(self):

        self.groupBoxButtons = QtWidgets.QGroupBox()

        gridBtnLayout = QtWidgets.QGridLayout()

        self.btnQuit = QtWidgets.QPushButton("Cancel")
        self.btnQuit.setFixedSize(150, 23)

        self.btnSubmit = QtWidgets.QPushButton("OK")
        self.btnSubmit.setFixedSize(150, 23)

        gridBtnLayout.addWidget(self.btnSubmit, 0, 0)
        gridBtnLayout.addWidget(self.btnQuit, 0, 1)

        QtCore.QObject.connect(self.btnQuit, QtCore.SIGNAL(
            "clicked()"), self, QtCore.SLOT("reject()"))

        self.groupBoxButtons.setLayout(gridBtnLayout)

    def createParamsGridLayout(self):
        self.groupBoxParams = QtWidgets.QGroupBox('Adjustment parameters')

        gridParamsLayout = QtWidgets.QGridLayout()
        gridParamsLayout.setHorizontalSpacing(50)
        self.label_chunk = QtWidgets.QLabel('Chunk : ')

        self.chunksBox = QtWidgets.QComboBox()
        self.chunksBox.resize(200, 23)

        chunks = self.getChunks()
        for chunk in chunks:
            self.chunksBox.addItem(chunk.label, chunk.key)

        self.label_brightness = QtWidgets.QLabel('Image brightness (%): ')
        self.brightness = QtWidgets.QSpinBox()
        self.brightness.setMaximum(500)
        self.brightness.setSingleStep(10)
        self.brightness.setMinimum(0)
        self.brightness.setValue(100)

        self.label_contrast = QtWidgets.QLabel('Image contrast (%): ')
        self.contrast = QtWidgets.QSpinBox()
        self.contrast.setMaximum(500)
        self.contrast.setSingleStep(10)
        self.contrast.setMinimum(0)
        self.contrast.setValue(100)

        self.label_folder = QtWidgets.QLabel('Select folder  : ')
        self.btn_select_folder = QtWidgets.QPushButton("Select...")
        self.btn_select_folder.setFixedSize(150, 23)
        self.path_label = QtWidgets.QLabel('Selected Path : ...')

        self.space = QtWidgets.QLabel('         ')

        self.chunk_create_label = QtWidgets.QLabel("Create new Chunk")

        self.chkCreateChunk = QtWidgets.QCheckBox()
        # adding widget
        gridParamsLayout.addWidget(self.label_chunk, 0, 0)
        gridParamsLayout.addWidget(self.chunksBox, 0, 1)
        gridParamsLayout.addWidget(self.label_folder, 0, 2)
        gridParamsLayout.addWidget(self.btn_select_folder, 0, 3)

        gridParamsLayout.addWidget(self.label_brightness, 1, 0)
        gridParamsLayout.addWidget(self.brightness, 1, 1)
        gridParamsLayout.addWidget(self.path_label, 1, 2)

        gridParamsLayout.addWidget(self.label_contrast, 2, 0)
        gridParamsLayout.addWidget(self.contrast, 2, 1)

        gridParamsLayout.addWidget(self.chunk_create_label, 2, 2)
        gridParamsLayout.addWidget(self.chkCreateChunk, 2, 3)
        QtCore.QObject.connect(
            self.btn_select_folder, QtCore.SIGNAL("clicked()"), self.selectFolder)

        # gridLayout.addWidget(self.btnZoomIn, 7, 1)
        # gridLayout.addWidget(self.btnZoomOut, 7, 2)

        # gridLayout.addWidget(self.btnP1, 8, 1)
        # gridLayout.addWidget(self.btnQuit, 8, 2)

        self.groupBoxParams.setLayout(gridParamsLayout)

    def getChunks(self):
        return Metashape.app.document.chunks

    def selectFolder(self):

        directoryPath = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Directory")
        dossier = directoryPath.split('/')[-1]
        path = 'Selected Path : {}'.format(directoryPath)
        self.path_label.setText(path)
        self.btnSubmit.setEnabled(True)
        self.path_folder = directoryPath


def copyChnukPhotos():
    global doc

    doc = Metashape.app.document

    app = QtWidgets.QApplication.instance()
    parent = app.activeWindow()

    dlg = CopyChunkPhotosDlg(parent)


label = "Custom menu/Adjust brightness photos"
Metashape.app.addMenuItem(label, copyChnukPhotos)
print("To execute this script press {}".format(label))
