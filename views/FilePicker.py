# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import controllers.FileFinder as Finder
import views.Editor as Editor
from controllers.Workspace import Workspace as WorkspaceManager


class Ui_FilePicker(object):
    this_window = None

    def selected_image(self, item):
        image_path = WorkspaceManager.copy_image_to_workspace(item.text())

        self.editor_window = QtWidgets.QMainWindow()
        self.ui_editor = Editor.Ui_EditorWindow()
        self.editor_window.show()
        self.this_window.close()
        self.ui_editor.setup_ui(self.editor_window, image_path)

    def set_files_list(self) :
        files = Finder.FileFinder.show_files()

        for f in files:
            self.filesList.addItem(f)

        self.filesList.itemClicked.connect(self.selected_image)

    def setup_ui(self, MainWindow):
        self.this_window = MainWindow

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 70, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.filesList = QtWidgets.QListWidget(self.centralwidget)
        self.filesList.setGeometry(QtCore.QRect(30, 131, 751, 401))
        self.filesList.setObjectName("filesList")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.set_files_list()

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Select a file"))

