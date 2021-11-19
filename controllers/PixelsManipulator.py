from PIL import Image
from time import sleep
from controllers.Workspace import Workspace as WorkspaceManager
import os
from PyQt5 import QtCore


class PixelsManipulator(QtCore.QThread):

    image = None
    image_original_path = ''
    image_width = 0
    image_height = 0
    image_extension = ''
    pixels = []
    dark = (0, 0, 0, 255)
    red = (255, 0, 0, 255)
    already_shown = []
    color_found = QtCore.pyqtSignal(tuple)
    preview_saved = QtCore.pyqtSignal(str)
    version_changed = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal()

    def __init__(self, image):
        super().__init__()
        self.image_original_path = image
        self.load_image()

    def run(self):
        self.check_colors()

    def load_image(self):
        self.image = Image.open(self.image_original_path)
        self.pixels = self.image.load()
        self.image_width, self.image_height = self.image.size
        self.image_extension = self.image_original_path.split('.')[-1]

    def change_color(self, pixel_coordinates, color_to_replace, replace_by, new_change):
        for x in range(self.image_width):
            for y in range(self.image_height):
                p = self.pixels[x, y]
                if p == color_to_replace:
                    self.pixels[x, y] = replace_by

        if new_change:
            change = {
                        'pixel_x': pixel_coordinates['x'],
                        'pixel_y': pixel_coordinates['y'],
                        'old': list(color_to_replace),
                        'new': list(replace_by)
                      }

            preview_path = WorkspaceManager.save_preview(self.image, self.image_extension, change)
            self.preview_saved.emit(preview_path)
        else:
            preview_path = WorkspaceManager.undo(self.image_extension)
            self.preview_saved.emit(preview_path)

        self.version_changed.emit(WorkspaceManager.get_last_preview())

    def check_colors(self):
        for x in range(self.image_width):
            for y in range(self.image_height):
                p = self.pixels[x, y]
                if p not in self.already_shown:
                    self.already_shown.append(p)
                    self.color_found.emit(p)
                    sleep(0.005)
        self.finished.emit()



