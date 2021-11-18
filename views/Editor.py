# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editorBrowser.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from functools import partial
from controllers.Workspace import Workspace as WorkspaceManager
import views.SetColorDialog as NewColorDialog
import controllers.PixelsManipulator as PM


class Ui_EditorWindow(object):
    this_window = None
    image = ''
    all_colors_loaded = False
    colorFounder = None
    x_interator = 0
    y_interator = 0
    max_pixels_per_row = 10

    def clear_pixels(self, layout):
        self.x_interator = 0
        self.y_interator = 0

        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clear_pixels(child.layout())

    def change_pixel_color(self, frame_changed, old_color, new_color):
        self.colorFounder.change_color(old_color, new_color)
        frame_changed.setStyleSheet(f'background-color: rgba{new_color}; border: None;')

    def finished_scan(self):
        self.all_colors_loaded = True
        self.colorsFound.setStyleSheet('border: 3px solid rgb(0, 255, 0)')

    def set_color(self, color):
        color_code = str(color)

        frame = QtWidgets.QWidget()
        frame.color_code = color
        frame.place_on = {'x': self.x_interator, 'y': self.y_interator}
        frame.setFixedSize(15, 15)

        frame.mousePressEvent = partial(self.open_dialog, frame)

        if len(color) == 4:
            frame.setStyleSheet("background-color: rgba" + color_code + "; border: 1px solid black")
        else:
            frame.setStyleSheet("background-color: rgb" + color_code + "; border: 1px solid black")

        frame.setToolTip(color_code)

        self.pixels_view_layout.addWidget(frame, self.x_interator, self.y_interator)

        if self.y_interator == self.max_pixels_per_row:
            self.x_interator += 1
            self.y_interator = 0
        else:
            self.y_interator += 1

    def show_preview(self, preview_path):
        self.image = preview_path
        self.config_image_view()

    def config_image_view(self):
        scene = QtWidgets.QGraphicsScene()
        pixmap = QPixmap(self.image)
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        scene.addItem(item)
        self.selectedImage.setScene(scene)

    def discover_all_colors(self):
        self.colorsFound.setStyleSheet('border: 3px solid rgb(255, 0, 0)')

        self.colorFounder = PM.PixelsManipulator(self.image)
        self.colorFounder.color_found.connect(self.set_color)
        self.colorFounder.preview_saved.connect(self.show_preview)
        self.colorFounder.finished.connect(self.finished_scan)
        self.colorFounder.start()

    def open_dialog(self, frame, event):
        if not self.all_colors_loaded:
            QtWidgets.QMessageBox.warning(self.this_window, 'Espere', 'Aguarde o fim da leitura da imagem!')
            return

        self.Dialog = QtWidgets.QDialog()
        self.ui = NewColorDialog.Ui_Dialog()
        self.ui.setup_ui(self, self.Dialog, frame)
        self.Dialog.show()

    def on_close_window(self, event):
        WorkspaceManager.clear_work_space()
        event.accept()

    def setup_ui(self, EditorWindow, image_path):
        self.this_window = EditorWindow
        self.image = image_path

        EditorWindow.setObjectName("EditorWindow")
        EditorWindow.resize(911, 600)
        EditorWindow.closeEvent = partial(self.on_close_window)
        self.centralwidget = QtWidgets.QWidget(EditorWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.selectedImage = QtWidgets.QGraphicsView(self.centralwidget)
        self.selectedImage.setGeometry(QtCore.QRect(10, 10, 501, 581))
        self.selectedImage.setObjectName("selectedImage")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(540, 10, 361, 571))
        self.scrollArea.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.scrollArea.setObjectName("scrollArea")
        self.colorsFound = QtWidgets.QFrame()
        self.colorsFound.setGeometry(QtCore.QRect(0, 0, 359, 569))
        self.colorsFound.setObjectName("colorsFound")
        self.pixels_view_layout = QtWidgets.QGridLayout(self.colorsFound)
        self.scrollArea.setWidget(self.colorsFound)

        EditorWindow.setCentralWidget(self.centralwidget)

        self.retranslate_ui(EditorWindow)
        QtCore.QMetaObject.connectSlotsByName(EditorWindow)

        self.config_image_view()
        self.discover_all_colors()

    def retranslate_ui(self, EditorWindow):
        _translate = QtCore.QCoreApplication.translate
        EditorWindow.setWindowTitle(_translate("EditorWindow", "EditorWindow"))