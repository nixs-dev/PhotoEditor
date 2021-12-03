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
    all_pixels = []
    color_found = QtCore.pyqtSignal(tuple)
    preview_saved = QtCore.pyqtSignal(str)
    version_changed = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal()

    def __init__(self, image):
        super().__init__()
        self.image_original_path = image
        self.load_image()

    def run(self):
        self.show_all_collors()

    def load_image(self):
        self.image = Image.open(self.image_original_path)
        self.all_pixels = self.image.load()
        self.image_width, self.image_height = self.image.size
        self.image_extension = self.image_original_path.split('.')[-1]

    def change_color(self, pixel_coordinates, color_to_replace, replace_by, new_change):
        for x in range(self.image_width):
            for y in range(self.image_height):
                p = self.all_pixels[x, y]
                if p == color_to_replace:
                    self.all_pixels[x, y] = replace_by

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

    def show_all_collors(self):
        pixels = {}

        for x in range(self.image_width):
            for y in range(self.image_height):
                p = self.all_pixels[x, y]
                if p not in pixels:
                    pixels[p] = 1
                else:
                    pixels[p] += 1

        pixels = sorted(pixels, key=lambda i: pixels[i], reverse=True)

        for pixel in pixels:
            self.color_found.emit(pixel)
            sleep(0.0001)
        self.finished.emit()
