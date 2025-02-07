# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost when recompiling the ui file!

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
    QLabel, QSlider, QStyle, QSizePolicy, QFileDialog, QPlainTextEdit, QGroupBox
)
from PyQt6.QtGui import QShortcut  # <-- Import QShortcut from QtGui
import vtk
# Use the PyQt6 VTK interactor import – ensure you have vtk>=9 installed.
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor as qvtk
from vtk.util import numpy_support # type: ignore
from trakstar_interface import TrakSTARInterface


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # Use the new enum for window modality
        MainWindow.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        MainWindow.resize(804, 586)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet("background:rgb(91,90,90)")
        MainWindow.setDocumentMode(True)
        # Use the new enum for tab shape
        MainWindow.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        MainWindow.setDockNestingEnabled(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabw = QtWidgets.QTabWidget(self.centralwidget)
        self.tabw.setAutoFillBackground(False)
        self.tabw.setStyleSheet("background:rgb(91,90,90)")
        self.tabw.setObjectName("tabw")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(240, 10, 261, 31))
        self.label.setObjectName("label")
        self.sr_iso_box = QtWidgets.QGroupBox(self.tab)
        self.sr_iso_box.setGeometry(QtCore.QRect(430, 180, 301, 101))
        self.sr_iso_box.setStyleSheet("QGroupBox{\n"
                                      "    border:1px solid rgb(51,51,51);    \n"
                                      "    border-radius:4px;\n"
                                      "    color:white;\n"
                                      "    background:rgb(91,90,90);\n"
                                      "}")
        self.sr_iso_box.setObjectName("sr_iso_box")
        self.sr_iso_tbox = QtWidgets.QPlainTextEdit(self.sr_iso_box)
        self.sr_iso_tbox.setGeometry(QtCore.QRect(10, 40, 71, 31))
        self.sr_iso_tbox.setStyleSheet("background-color: rgb(255, 250, 226);\n"
                                       "font: 75 8pt \"Orbitron\";")
        self.sr_iso_tbox.setObjectName("sr_iso_tbox")
        self.sr_iso_slider = QtWidgets.QSlider(self.sr_iso_box)
        self.sr_iso_slider.setGeometry(QtCore.QRect(90, 40, 201, 31))
        self.sr_iso_slider.setStyleSheet("QSlider::groove:horizontal {\n"
                                         "        height:5px;\n"
                                         "        background: rgb(51,51,51);\n"
                                         "}\n"
                                         "\n"
                                         "QSlider::handle:horizontal {\n"
                                         "        background:rgb(0,143,170);\n"
                                         "        width: 10px;\n"
                                         "    margin:-8px 0\n"
                                         "}\n"
                                         "\n"
                                         "QSlider::add-page:horizondal {\n"
                                         "        background:rgb(51,51,51);\n"
                                         "}\n"
                                         "\n"
                                         "QSlider::sub-page:horizondal {\n"
                                         "        background:rgb(51,51,51);\n"
                                         "}")
        # Use PyQt6 enum for orientation:
        self.sr_iso_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.sr_iso_slider.setObjectName("sr_iso_slider")
        self.sr_import_box = QtWidgets.QGroupBox(self.tab)
        self.sr_import_box.setGeometry(QtCore.QRect(430, 60, 301, 101))
        self.sr_import_box.setStyleSheet("QGroupBox{\n"
                                         "    border:1px solid rgb(51,51,51);    \n"
                                         "    border-radius:4px;\n"
                                         "    color:white;\n"
                                         "    background:rgb(91,90,90);\n"
                                         "}")
        self.sr_import_box.setObjectName("sr_import_box")
        self.sr_browse = QtWidgets.QPushButton(self.sr_import_box)
        self.sr_browse.setGeometry(QtCore.QRect(210, 40, 75, 31))
        self.sr_browse.setStyleSheet("QPushButton {\n"
                                     "    border: 2px solid rgb(51,51,51);\n"
                                     "    border-radius: 5px;    \n"
                                     "    color:rgb(255,255,255);\n"
                                     "    background-color: rgb(51,51,51);\n"
                                     "}\n"
                                     "QPushButton:hover {\n"
                                     "    border: 2px solid rgb(0,143,150);\n"
                                     "    background-color: rgb(0,143,150);\n"
                                     "}\n"
                                     "QPushButton:pressed {    \n"
                                     "    border: 2px solid rgb(0,143,150);\n"
                                     "    background-color: rgb(51,51,51);\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:disabled {    \n"
                                     "    border-radius: 5px;    \n"
                                     "    border: 2px solid rgb(112,112,112);\n"
                                     "    background-color: rgb(112,112,112);\n"
                                     "}")
        self.sr_browse.setObjectName("sr_browse")
        self.sr_import_tb = QtWidgets.QPlainTextEdit(self.sr_import_box)
        self.sr_import_tb.setGeometry(QtCore.QRect(10, 40, 191, 31))
        self.sr_import_tb.setStyleSheet("background-color: rgb(255, 250, 226);\n"
                                        "font: 75 8pt \"Orbitron\";")
        self.sr_import_tb.setObjectName("sr_import_tb")
        self.sr_rgb_box = QtWidgets.QGroupBox(self.tab)
        self.sr_rgb_box.setGeometry(QtCore.QRect(430, 310, 301, 171))
        self.sr_rgb_box.setStyleSheet("QGroupBox{\n"
                                      "    border:1px solid rgb(51,51,51);    \n"
                                      "    border-radius:4px;\n"
                                      "    color:white;\n"
                                      "    background:rgb(91,90,90);\n"
                                      "}")
        self.sr_rgb_box.setObjectName("sr_rgb_box")
        self.sr_red_slider = QtWidgets.QSlider(self.sr_rgb_box)
        self.sr_red_slider.setGeometry(QtCore.QRect(90, 30, 201, 31))
        self.sr_red_slider.setStyleSheet("QSlider::groove:horizontal {\n"
                                         "        height:5px;\n"
                                         "        background: rgb(51,51,51);\n"
                                         "}\n"
                                         "\n"
                                         "QSlider::handle:horizontal {\n"
                                         "        background:rgb(0,143,170);\n"
                                         "        width: 10px;\n"
                                         "    margin:-8px 0\n"
                                         "}\n"
                                         "\n"
                                         "QSlider::add-page:horizondal {\n"
                                         "        background:rgb(51,51,51);\n"
                                         "}\n"
                                         "\n"
                                         "QSlider::sub-page:horizondal {\n"
                                         "        background:rgb(51,51,51);\n"
                                         "}")
        self.sr_red_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.sr_red_slider.setObjectName("sr_red_slider")
        self.sr_green_slider = QtWidgets.QSlider(self.sr_rgb_box)
        self.sr_green_slider.setGeometry(QtCore.QRect(90, 70, 201, 31))
        self.sr_green_slider.setStyleSheet("QSlider::groove:horizontal {\n"
                                           "        height:5px;\n"
                                           "        background: rgb(51,51,51);\n"
                                           "}\n"
                                           "\n"
                                           "QSlider::handle:horizontal {\n"
                                           "        background:rgb(0,143,170);\n"
                                           "        width: 10px;\n"
                                           "    margin:-8px 0\n"
                                           "}\n"
                                           "\n"
                                           "QSlider::add-page:horizondal {\n"
                                           "        background:rgb(51,51,51);\n"
                                           "}\n"
                                           "\n"
                                           "QSlider::sub-page:horizondal {\n"
                                           "        background:rgb(51,51,51);\n"
                                           "}")
        self.sr_green_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.sr_green_slider.setObjectName("sr_green_slider")
        self.sr_blue_slider = QtWidgets.QSlider(self.sr_rgb_box)
        self.sr_blue_slider.setGeometry(QtCore.QRect(90, 110, 201, 31))
        self.sr_blue_slider.setStyleSheet("QSlider::groove:horizontal {\n"
                                          "        height:5px;\n"
                                          "        background: rgb(51,51,51);\n"
                                          "}\n"
                                          "\n"
                                          "QSlider::handle:horizontal {\n"
                                          "        background:rgb(0,143,170);\n"
                                          "        width: 10px;\n"
                                          "    margin:-8px 0\n"
                                          "}\n"
                                          "\n"
                                          "QSlider::add-page:horizondal {\n"
                                          "        background:rgb(51,51,51);\n"
                                          "}\n"
                                          "\n"
                                          "QSlider::sub-page:horizondal {\n"
                                          "        background:rgb(51,51,51);\n"
                                          "}")
        self.sr_blue_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.sr_blue_slider.setObjectName("sr_blue_slider")
        self.sr_red = QtWidgets.QLabel(self.sr_rgb_box)
        self.sr_red.setGeometry(QtCore.QRect(16, 30, 51, 31))
        self.sr_red.setObjectName("sr_red")
        self.sr_blue = QtWidgets.QLabel(self.sr_rgb_box)
        self.sr_blue.setGeometry(QtCore.QRect(16, 110, 51, 31))
        self.sr_blue.setObjectName("sr_blue")
        self.sr_green = QtWidgets.QLabel(self.sr_rgb_box)
        self.sr_green.setGeometry(QtCore.QRect(10, 70, 61, 31))
        self.sr_green.setObjectName("sr_green")
        self.sr_window_box = QtWidgets.QGroupBox(self.tab)
        self.sr_window_box.setGeometry(QtCore.QRect(10, 60, 411, 451))
        self.sr_window_box.setObjectName("sr_window_box")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.sr_window_box)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 20, 391, 421))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.sr_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.sr_layout.setContentsMargins(0, 0, 0, 0)
        self.sr_layout.setObjectName("sr_layout")
        self.tabw.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.rc_iso_box = QtWidgets.QGroupBox(self.tab_2)
        self.rc_iso_box.setGeometry(QtCore.QRect(430, 179, 301, 101))
        self.rc_iso_box.setStyleSheet("QGroupBox{\n"
                                      "    border:1px solid rgb(51,51,51);    \n"
                                      "    border-radius:4px;\n"
                                      "    color:white;\n"
                                      "    background:rgb(91,90,90);\n"
                                      "\n"
                                      "}")
        self.rc_iso_box.setObjectName("rc_iso_box")
        self.rc_iso_slider = QtWidgets.QSlider(self.rc_iso_box)
        self.rc_iso_slider.setGeometry(QtCore.QRect(90, 40, 201, 31))
        self.rc_iso_slider.setStyleSheet("QSlider::groove:horizontal {\n"
                                         "        height:5px;\n"
                                         "        background: rgb(51,51,51);\n"
                                         "}\n"
                                         "\n"
                                         "QSlider::handle:horizontal {\n"
                                         "        background:rgb(0,143,170);\n"
                                         "        width: 10px;\n"
                                         "    margin:-8px 0\n"
                                         "}\n"
                                         "\n"
                                         "QSlider::add-page:horizondal {\n"
                                         "        background:rgb(51,51,51);\n"
                                         "}\n"
                                         "\n"
                                         "QSlider::sub-page:horizondal {\n"
                                         "        background:rgb(51,51,51);\n"
                                         "}")
        self.rc_iso_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.rc_iso_slider.setObjectName("rc_iso_slider")
        self.rc_iso_comboBox = QtWidgets.QComboBox(self.rc_iso_box)
        self.rc_iso_comboBox.setGeometry(QtCore.QRect(10, 40, 71, 31))
        self.rc_iso_comboBox.setStyleSheet("QComboBox {\n"
                                           "    border: 2px solid rgb(51,51,51);\n"
                                           "    border-radius: 5px;    \n"
                                           "    color:rgb(255,255,255);\n"
                                           "    background-color: rgb(51,51,51);\n"
                                           "}\n"
                                           "\n"
                                           "QComboBox:hover {\n"
                                           "    border: 2px solid rgb(0,143,170);\n"
                                           "    border-radius: 5px;    \n"
                                           "    color:rgb(255,255,255);\n"
                                           "    background-color: rgb(0,143,170);\n"
                                           "}\n"
                                           "\n"
                                           "QComboBox:!editable, QComboBox::drop-down:editable {\n"
                                           "    background: rgb(51,51,51);\n"
                                           "}\n"
                                           "\n"
                                           "QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
                                           "        background:rgb(51,51,51);\n"
                                           "}\n"
                                           "\n"
                                           "QComboBox:on { /* shift the text when the popup opens */\n"
                                           "        padding-top: 3px;\n"
                                           "        padding-left: 4px;\n"
                                           "}\n"
                                           "\n"
                                           "QComboBox::drop-down {\n"
                                           "        subcontrol-origin: padding;\n"
                                           "        subcontrol-position: top right;\n"
                                           "        width: 15px;\n"
                                           "\n"
                                           "        border-left-width: 1px;\n"
                                           "        border-left-color: darkgray;\n"
                                           "        border-left-style: solid; /* just a single line */\n"
                                           "        border-top-right-radius: 5px; /* same radius as the QComboBox */\n"
                                           "        border-bottom-right-radius: 5px;\n"
                                           "}\n"
                                           "\n"
                                           "\n"
                                           "QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
                                           "        top: 1px;\n"
                                           "        left: 1px;\n"
                                           "}\n"
                                           "\n"
                                           "QComboBox::drop-down {\n"
                                           "        background:rgb(51,51,51);\n"
                                           "}")
        self.rc_iso_comboBox.setObjectName("rc_iso_comboBox")
        self.rc_iso_comboBox.addItem("skin1")
        self.rc_iso_comboBox.addItem("skin2")
        self.rc_iso_comboBox.addItem("tissue")
        self.rc_iso_comboBox.addItem("bones")
        self.rc_iso_comboBox.addItem("dense bones")
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(249, 9, 261, 31))
        self.label_5.setObjectName("label_5")
        self.rc_import_box = QtWidgets.QGroupBox(self.tab_2)
        self.rc_import_box.setGeometry(QtCore.QRect(430, 59, 301, 101))
        self.rc_import_box.setStyleSheet("QGroupBox{\n"
                                         "    border:1px solid rgb(51,51,51);    \n"
                                         "    border-radius:4px;\n"
                                         "    color:white;\n"
                                         "    background:rgb(91,90,90);\n"
                                         "}")
        self.rc_import_box.setObjectName("rc_import_box")
        self.rc_browse = QtWidgets.QPushButton(self.rc_import_box)
        self.rc_browse.setGeometry(QtCore.QRect(210, 40, 75, 31))
        self.rc_browse.setStyleSheet("QPushButton {\n"
                                     "    border: 2px solid rgb(51,51,51);\n"
                                     "    border-radius: 5px;    \n"
                                     "    color:rgb(255,255,255);\n"
                                     "    background-color: rgb(51,51,51);\n"
                                     "}\n"
                                     "QPushButton:hover {\n"
                                     "    border: 2px solid rgb(0,143,150);\n"
                                     "    background-color: rgb(0,143,150);\n"
                                     "}\n"
                                     "QPushButton:pressed {    \n"
                                     "    border: 2px solid rgb(0,143,150);\n"
                                     "    background-color: rgb(51,51,51);\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:disabled {    \n"
                                     "    border-radius: 5px;    \n"
                                     "    border: 2px solid rgb(112,112,112);\n"
                                     "    background-color: rgb(112,112,112);\n"
                                     "}")
        self.rc_browse.setObjectName("rc_browse")
        self.rc_import_tb = QtWidgets.QPlainTextEdit(self.rc_import_box)
        self.rc_import_tb.setGeometry(QtCore.QRect(10, 40, 191, 31))
        self.rc_import_tb.setStyleSheet("background-color: rgb(255, 250, 226);\n"
                                        "font: 75 8pt \"Orbitron\";")
        self.rc_import_tb.setObjectName("rc_import_tb")
        self.rc_rgb_box = QtWidgets.QGroupBox(self.tab_2)
        self.rc_rgb_box.setGeometry(QtCore.QRect(430, 309, 301, 171))
        self.rc_rgb_box.setStyleSheet("QGroupBox{\n"
                                      "    border:1px solid rgb(51,51,51);    \n"
                                      "    border-radius:4px;\n"
                                      "    color:white;\n"
                                      "    background:rgb(91,90,90);\n"
                                      "}")
        self.rc_rgb_box.setObjectName("rc_rgb_box")
        self.rc_red_slider = QtWidgets.QSlider(self.rc_rgb_box)
        self.rc_red_slider.setGeometry(QtCore.QRect(90, 30, 201, 31))
        self.rc_red_slider.setStyleSheet("QSlider::groove:horizontal {\n"
                                         "        height:5px;\n"
                                         "        background: rgb(51,51,51);\n"
                                         "}\n"
                                         "\n"
                                         "QSlider::handle:horizontal {\n"
                                         "        background:rgb(0,143,170);\n"
                                         "        width: 10px;\n"
                                         "    margin:-8px 0\n"
                                         "}\n"
                                         "\n"
                                         "QSlider::add-page:horizondal {\n"
                                         "        background:rgb(51,51,51);\n"
                                         "}\n"
                                         "\n"
                                         "QSlider::sub-page:horizondal {\n"
                                         "        background:rgb(51,51,51);\n"
                                         "}")
        self.rc_red_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.rc_red_slider.setObjectName("rc_red_slider")
        self.rc_green_slider = QtWidgets.QSlider(self.rc_rgb_box)
        self.rc_green_slider.setGeometry(QtCore.QRect(90, 70, 201, 31))
        self.rc_green_slider.setStyleSheet("QSlider::groove:horizontal {\n"
                                           "        height:5px;\n"
                                           "        background: rgb(51,51,51);\n"
                                           "}\n"
                                           "\n"
                                           "QSlider::handle:horizontal {\n"
                                           "        background:rgb(0,143,170);\n"
                                           "        width: 10px;\n"
                                           "    margin:-8px 0\n"
                                           "}\n"
                                           "\n"
                                           "QSlider::add-page:horizondal {\n"
                                           "        background:rgb(51,51,51);\n"
                                           "}\n"
                                           "\n"
                                           "QSlider::sub-page:horizondal {\n"
                                           "        background:rgb(51,51,51);\n"
                                           "}")
        self.rc_green_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.rc_green_slider.setObjectName("rc_green_slider")
        self.rc_blue_slider = QtWidgets.QSlider(self.rc_rgb_box)
        self.rc_blue_slider.setGeometry(QtCore.QRect(90, 110, 201, 31))
        self.rc_blue_slider.setStyleSheet("QSlider::groove:horizontal {\n"
                                          "        height:5px;\n"
                                          "        background: rgb(51,51,51);\n"
                                          "}\n"
                                          "\n"
                                          "QSlider::handle:horizontal {\n"
                                          "        background:rgb(0,143,170);\n"
                                          "        width: 10px;\n"
                                          "    margin:-8px 0\n"
                                          "}\n"
                                          "\n"
                                          "QSlider::add-page:horizondal {\n"
                                          "        background:rgb(51,51,51);\n"
                                          "}\n"
                                          "\n"
                                          "QSlider::sub-page:horizondal {\n"
                                          "        background:rgb(51,51,51);\n"
                                          "}")
        self.rc_blue_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.rc_blue_slider.setObjectName("rc_blue_slider")
        self.rc_red = QtWidgets.QLabel(self.rc_rgb_box)
        self.rc_red.setGeometry(QtCore.QRect(16, 30, 51, 31))
        self.rc_red.setObjectName("rc_red")
        self.rc_blue = QtWidgets.QLabel(self.rc_rgb_box)
        self.rc_blue.setGeometry(QtCore.QRect(16, 110, 51, 31))
        self.rc_blue.setObjectName("rc_blue")
        self.rc_green = QtWidgets.QLabel(self.rc_rgb_box)
        self.rc_green.setGeometry(QtCore.QRect(10, 70, 61, 31))
        self.rc_green.setObjectName("rc_green")
        self.rc_window_box = QtWidgets.QGroupBox(self.tab_2)
        self.rc_window_box.setGeometry(QtCore.QRect(10, 60, 411, 451))
        self.rc_window_box.setObjectName("rc_window_box")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.rc_window_box)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 391, 421))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.rc_window_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.rc_window_layout.setContentsMargins(0, 0, 0, 0)
        self.rc_window_layout.setObjectName("rc_window_layout")
        self.tabw.addTab(self.tab_2, "")
        self.horizontalLayout_2.addWidget(self.tabw)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.sr_browse.clicked.connect(lambda: self.get_file(0))
        self.rc_browse.clicked.connect(lambda: self.get_file(1))
        self.sro_vtk = ""
        sr_RGB_sliders = [self.sr_red_slider, self.sr_green_slider, self.sr_blue_slider]
        for s in sr_RGB_sliders:
            self.setting_slider(s, 1)
        rc_RGB_sliders = [self.rc_iso_slider, self.rc_red_slider, self.rc_green_slider, self.rc_blue_slider]
        for s in rc_RGB_sliders:
            self.setting_slider(s, 1)
        self.setting_slider(self.sr_iso_slider, 0)
        self.sr_iso_slider.valueChanged.connect(self.sr_value_changer)
        self.sr_red_slider.valueChanged.connect(self.sr_value_changer)
        self.sr_green_slider.valueChanged.connect(self.sr_value_changer)
        self.sr_blue_slider.valueChanged.connect(self.sr_value_changer)

        self.rc_iso_slider.valueChanged.connect(self.rc_value_changer)
        self.rc_red_slider.valueChanged.connect(self.rc_value_changer)
        self.rc_green_slider.valueChanged.connect(self.rc_value_changer)
        self.rc_blue_slider.valueChanged.connect(self.rc_value_changer)

        self.denisty_dic = {'skin1': 1, 'skin2': 100, 'tissue': 500, 'bones': 1000, 'dense bones': 1500}

        self.retranslateUi(MainWindow)
        self.tabw.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def get_file(self, typee):
        if typee == 0:
            print("Starting get_file with type 0...", flush=True)  # Debug print
            for i in reversed(range(self.sr_layout.count())):
                self.sr_layout.itemAt(i).widget().deleteLater()
            file = QFileDialog.getExistingDirectory()
            self.sr_import_tb.setPlainText(file)
            
            print("Creating VTK objects...", flush=True)  # Debug print
            self.sro_vtk = vtk_W(file)
            self.sro_vtk.surface_rendering()
            self.sro_vtk.add_trackstar_ball()

            self.sr_layout.addWidget(self.sro_vtk.frame)
            
            print("About to schedule TrackSTAR initialization...", flush=True)  # Debug print
            # Defer TrackSTAR initialization until after the current event cycle:
            QtCore.QTimer.singleShot(0, self.initialize_trackstar)
            print("TrackSTAR initialization has been scheduled.", flush=True)  # Debug print

        if typee == 1:
            for i in reversed(range(self.rc_window_layout.count())):
                self.rc_window_layout.itemAt(i).widget().deleteLater()
            file = QFileDialog.getExistingDirectory()
            self.rc_import_tb.setPlainText(file)
            self.rc_vtk = vtk_W(file)
            
            # First do ray casting setup
            self.rc_vtk.ray_casting()
            
            # Convert VTK data to NumPy array
            dims = self.rc_vtk.imageData.GetDimensions()
            vtk_array = self.rc_vtk.imageData.GetPointData().GetScalars()
            numpy_data = numpy_support.vtk_to_numpy(vtk_array)
            numpy_data = numpy_data.reshape(dims, order='F')
            
            # Call find_center_and_spawn_dot which now handles both dots
            initial_position = find_center_and_spawn_dot(numpy_data, self.rc_vtk.ren, self.rc_vtk)
            
            # Add widget to layout
            self.rc_window_layout.addWidget(self.rc_vtk.frame)
            
            print("About to schedule TrackSTAR initialization for ray casting...", flush=True)
            # Initialize TrackSTAR for ray casting
            QtCore.QTimer.singleShot(0, self.initialize_trackstar)
            print("TrackSTAR initialization has been scheduled for ray casting.", flush=True)

    def rc_value_changer(self):
        self.rc_vtk.volumeScalarOpacity.AddPoint(self.denisty_dic.get(self.rc_iso_comboBox.currentText()),
                                                  self.rc_iso_slider.value() / 10)
        self.rc_vtk.volumeColor.AddRGBPoint(self.denisty_dic.get(self.rc_iso_comboBox.currentText()),
                                            self.rc_red_slider.value() / 10,
                                            self.rc_green_slider.value() / 10,
                                            self.rc_blue_slider.value() / 10)
        self.rc_vtk.renWin.update()

    def sr_value_changer(self):
        self.sro_vtk.contour.SetValue(0, self.sr_iso_slider.value())
        self.sr_iso_tbox.setPlainText(str(self.sr_iso_slider.value()))
        self.sro_vtk.actor.GetProperty().SetColor(self.sr_red_slider.value() / 10,
                                                  self.sr_green_slider.value() / 10,
                                                  self.sr_blue_slider.value() / 10)
        self.sro_vtk.renWin.update()

    def setting_slider(self, set_slider, type):
        # For QSlider enums, use QSlider.TickPosition and QtCore.Qt.Orientation
        if type == 0:
            set_slider.setTickPosition(QSlider.TickPosition.TicksRight)
            set_slider.setTickInterval(1)
            set_slider.setSingleStep(1)
            set_slider.setValue(1500)
            set_slider.setMinimum(0)
            set_slider.setMaximum(1500)
        if type == 1:
            set_slider.setTickPosition(QSlider.TickPosition.TicksRight)
            set_slider.setTickInterval(100)
            set_slider.setSingleStep(100)
            set_slider.setValue(10)
            set_slider.setMinimum(0)
            set_slider.setMaximum(10)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DICOM Reader"))
        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; text-decoration: underline; color:#ffffff;\">Surface Rendering</span></p></body></html>"))
        self.sr_iso_box.setTitle(_translate("MainWindow", "Iso Value"))
        self.sr_import_box.setTitle(_translate("MainWindow", "Import DICOM files "))
        self.sr_browse.setText(_translate("MainWindow", "Browse"))
        self.sr_rgb_box.setTitle(_translate("MainWindow", "RGB Transfer function"))
        self.sr_red.setText(_translate("MainWindow",
                                       "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#ff0000;\">RED</span></p></body></html>"))
        self.sr_blue.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600; color:#00007f;\">BLUE</span></p></body></html>"))
        self.sr_green.setText(_translate("MainWindow",
                                         "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600; color:#00aa00;\">GREEN</span></p></body></html>"))
        self.sr_window_box.setTitle(_translate("MainWindow", "window"))
        self.tabw.setTabText(self.tabw.indexOf(self.tab), _translate("MainWindow", "Surface Rendering"))
        self.rc_iso_box.setTitle(_translate("MainWindow", "Iso Value"))
        self.rc_iso_comboBox.setItemText(0, _translate("MainWindow", "skin1"))
        self.rc_iso_comboBox.setItemText(1, _translate("MainWindow", "skin2"))
        self.rc_iso_comboBox.setItemText(2, _translate("MainWindow", "tissue"))
        self.rc_iso_comboBox.setItemText(3, _translate("MainWindow", "bones"))
        self.rc_iso_comboBox.setItemText(4, _translate("MainWindow", "dense bones"))
        self.label_5.setText(_translate("MainWindow",
                                         "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; text-decoration: underline; color:#ffffff;\">Ray Casting Rendering</span></p></body></html>"))
        self.rc_import_box.setTitle(_translate("MainWindow", "Import DICOM files "))
        self.rc_browse.setText(_translate("MainWindow", "Browse"))
        self.rc_rgb_box.setTitle(_translate("MainWindow", "RGB Transfer function"))
        self.rc_red.setText(_translate("MainWindow",
                                       "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#ff0000;\">RED</span></p></body></html>"))
        self.rc_blue.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600; color:#00007f;\">BLUE</span></p></body></html>"))
        self.rc_green.setText(_translate("MainWindow",
                                         "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600; color:#00aa00;\">GREEN</span></p></body></html>"))
        self.rc_window_box.setTitle(_translate("MainWindow", "window"))
        self.tabw.setTabText(self.tabw.indexOf(self.tab_2), _translate("MainWindow", "Ray Casting Rendering"))

    def update_trackstar_position(self):
        data = self.trakstar.get_synchronous_data_dict(write_data_file=False)
        x, y, z = data[1][:3]
        
        # Check which rendering mode we're in and update the appropriate VTK object
        if hasattr(self, 'rc_vtk'):
            self.rc_vtk.update_trackstar_position((x, y, z))
        elif hasattr(self, 'sro_vtk'):
            self.sro_vtk.update_trackstar_position((x, y, z))

    def initialize_trackstar(self):
        print("Initializing TrackSTAR interface now...", flush=True)
        try:
            self.trakstar = TrakSTARInterface()
            self.trakstar.initialize()
            print("TrackSTAR interface initialized successfully!", flush=True)  # Success print
            
            self.trackstar_timer = QtCore.QTimer()
            self.trackstar_timer.timeout.connect(self.update_trackstar_position)
            self.trackstar_timer.start(50)
            print("TrackSTAR update timer started.", flush=True)  # Timer started print
        except Exception as e:
            print(f"Error initializing TrackSTAR: {str(e)}", flush=True)  # Error print

def find_center_and_spawn_dot(vtk_data, renderer, vtk_obj):
    print("Starting find_center_and_spawn_dot")
    dims = vtk_data.shape
    print(f"Data dimensions: {dims}")
    center_x = dims[0] // 4
    center_y = dims[1] // 4
    print(f"Center coordinates (x,y): ({center_x}, {center_y})")


    for z in reversed(range(dims[2])):
        if vtk_data[center_x, center_y, z] >= 1:
            print(f"Spawning dot at: {center_x}, {center_y}, {z}")
            spawn_yellow_dot(center_x, center_y, 15, renderer)
            # Add TrackSTAR ball at the same position
            vtk_obj.add_trackstar_ball(center_x, center_y, 15)
            # Return the position where we found our spot
            return (center_x, center_y, z)  
    return None

def spawn_yellow_dot(x, y, z, renderer):
    sphere = vtk.vtkSphereSource()
    sphere.SetCenter(x, y, z)
    sphere.SetRadius(1)  # Make it very large for testing
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(sphere.GetOutputPort())
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1.0, 1.0, 0.0)  # Yellow color
    
    renderer.AddActor(actor)
    print(f"Added yellow dot actor at position ({x}, {y}, {z})")

class vtk_W:
    def __init__(self, direc_path):
        self.dirc = direc_path
        self.frame = QtWidgets.QFrame()
        self.ren = vtk.vtkRenderer()  # Initialize the renderer here
        self.load_data()
        self.renWin = 0

    def load_data(self):
        self.reader = vtk.vtkDICOMImageReader()
        self.reader.SetDirectoryName(self.dirc)
        self.reader.Update()
        self.imageData = self.reader.GetOutput()

    def surface_rendering(self):
        self.contour = vtk.vtkContourFilter()
        self.contour.SetValue(0, 1500)  # 0.5*(minVal + maxVal))
        self.contour.SetInputData(self.imageData)
        surfaceNormals = vtk.vtkPolyDataNormals()
        surfaceNormals.SetInputConnection(self.contour.GetOutputPort())
        surfaceNormals.SetFeatureAngle(90.0)
        mapper = vtk.vtkPolyDataMapper()
        mapper.ScalarVisibilityOff()
        mapper.SetInputConnection(surfaceNormals.GetOutputPort())
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetColor(222 / 256., 184 / 256., 135 / 256.)
        self.sr_rendering()

    def ray_casting(self):
        self.volumeMapper = vtk.vtkSmartVolumeMapper()
        self.volumeMapper.SetInputData(self.imageData)
        self.volumeColor = vtk.vtkColorTransferFunction()
        self.volumeColor.AddRGBPoint(0, 0.00, 0.000, 0.00)
        self.volumeColor.AddRGBPoint(1, 0.00, 0.000, 0.00)
        self.volumeColor.AddRGBPoint(100, 1.00, 0.000, 0.00)
        self.volumeColor.AddRGBPoint(500, 1.0, 1.00, 1.00)
        self.volumeColor.AddRGBPoint(1000, 1.00, 1.00, 1.00)
        self.volumeColor.AddRGBPoint(1500, 1.0, 1.0, 1.0)
        self.volumeColor.AddRGBPoint(2000, 0, 0, 0)

        self.volumeScalarOpacity = vtk.vtkPiecewiseFunction()

        self.volumeScalarOpacity.AddPoint(0, 0.00)
        self.volumeScalarOpacity.AddPoint(1, 0.00)
        self.volumeScalarOpacity.AddPoint(100, 1.00)
        self.volumeScalarOpacity.AddPoint(500, 1.0000)
        self.volumeScalarOpacity.AddPoint(1000, 1.000)
        self.volumeScalarOpacity.AddPoint(1500, 1.0)
        self.volumeScalarOpacity.AddPoint(2000, 0.00)

        volumeGradientOpacity = vtk.vtkPiecewiseFunction()

        volumeGradientOpacity.AddPoint(0, 1.0)
        volumeGradientOpacity.AddPoint(1, 1.0)
        volumeGradientOpacity.AddPoint(100, 1.0)
        volumeGradientOpacity.AddPoint(100, 1.0)
        volumeGradientOpacity.AddPoint(500, 1.0)
        volumeGradientOpacity.AddPoint(1000, 1.0)
        volumeGradientOpacity.AddPoint(1500, 1.0)

        volumeProperty = vtk.vtkVolumeProperty()
        volumeProperty.SetColor(self.volumeColor)
        volumeProperty.SetScalarOpacity(self.volumeScalarOpacity)
        volumeProperty.SetGradientOpacity(volumeGradientOpacity)
        volumeProperty.SetInterpolationTypeToLinear()
        volumeProperty.ShadeOn()

        self.volume = vtk.vtkVolume()
        self.volume.SetMapper(self.volumeMapper)
        self.volume.SetProperty(volumeProperty)
        self.rc_rendering()
        

    def sr_rendering(self):
        self.renWin = qvtk(self.frame)
        self.ren = vtk.vtkRenderer()
        self.ren.AddActor(self.actor)
        self.ren.SetBackground(0, 0, 0)
        self.renWin.GetRenderWindow().AddRenderer(self.ren)
        self.renWin.SetSize(411, 411)

        self.iren = self.renWin.GetRenderWindow().GetInteractor()

        self.iren.Initialize()
        self.renWin.Render()

    def rc_rendering(self):
        self.renWin = qvtk(self.frame)
        # Remove the line that creates a new renderer
        # self.ren = vtk.vtkRenderer()  # Remove this line
        
        camera = self.ren.GetActiveCamera()
        c = self.volume.GetCenter()
        camera.SetFocalPoint(c[0], c[1], c[2])
        camera.SetPosition(c[0] + 400, c[1], c[2])
        camera.SetViewUp(0, 0, -1)
        self.renWin.SetSize(640, 480)
        self.ren.AddViewProp(self.volume)
        self.renWin.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.renWin.GetRenderWindow().GetInteractor()
        self.iren.Initialize()
        self.renWin.Render()
        self.iren.Start()

    def add_trackstar_ball(self, x, y, z):
        # 1. Create the sphere
        self.trackstar_ball_source = vtk.vtkSphereSource()
        self.trackstar_ball_source.SetCenter(x, y, z)  # Set center on the source, not the actor
        self.trackstar_ball_source.SetRadius(2.0)  # Size of the sphere
        self.trackstar_ball_source.SetThetaResolution(32)  # Smoothness of the sphere
        self.trackstar_ball_source.SetPhiResolution(32)    # Smoothness of the sphere

        # 2. Create the mapper (converts geometry into something that can be drawn)
        trackstar_mapper = vtk.vtkPolyDataMapper()
        trackstar_mapper.SetInputConnection(self.trackstar_ball_source.GetOutputPort())

        # 3. Create the actor (represents the sphere in the 3D scene)
        self.trackstar_actor = vtk.vtkActor()
        self.trackstar_actor.SetMapper(trackstar_mapper)
        self.trackstar_actor.GetProperty().SetColor(1.0, 1.0, 0.0)  # RGB for yellow

        # 4. Add to the scene
        self.ren.AddActor(self.trackstar_actor)
        print(f"TrackSTAR ball initialized at position ({x}, {y}, {z})")

    def update_trackstar_position(self, pos):
        # pos is expected to be a tuple (x, y, z)
        self.trackstar_actor.SetPosition(*pos)
        # Force the render window to update so the movement is visible
        self.renWin.GetRenderWindow().Render()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DICOM = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(DICOM)
    DICOM.show()
    # In PyQt6, use exec() instead of exec_()
    sys.exit(app.exec())
    
    