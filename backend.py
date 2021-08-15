from PIL import Image
from time import sleep
from os import listdir, replace
from PyQt5 import QtCore

class PhotoEditorBackEnd(QtCore.QThread):

    image = ''
    path = "."
    nullPixel = (0, 0, 0, 0)
    dark = (0, 0, 0, 255)
    red = (255, 0, 0, 255)
    alreadyShown = []
    allowed = ['jpg', 'png']
    colorFound = QtCore.pyqtSignal(tuple)
    finished = QtCore.pyqtSignal()

    def __init__(self, image):
        super(PhotoEditorBackEnd, self).__init__()
        self.image = image

    def run(self):
        self.checkColors(self.image)


    def loadImage(self, imagePath):
        imagepath = imagePath
        image = Image.open(imagepath)
        pixels = image.load()
        width, height = image.size

        return {'pixels': pixels, 'width': width, 'height': height}


    def changeColor(self):
        for x in range(self.width):
            for y in range(self.height):
                p = self.pixels[x,y]
                if p != self.nullPixel:
                    if p == self.dark:
                        self.pixels[x,y] = self.red
        self.image.save(self.imagepath)

    def checkColors(self, image):
        data = self.loadImage(image)
        for x in range(data['width']):
            for y in range(data['height']):
                p = data['pixels'][x,y]
                if p not in self.alreadyShown:
                    self.alreadyShown.append(p)
                    self.colorFound.emit(p)
                print('')
            print('')
        self.finished.emit()

    def IsImage(self, im):
        extensionIndex = -1;

        for i in range(len(im)):
            if im[i] == '.':
                extensionIndex = i
        
        extension = im[int(extensionIndex):int(len(im))].replace('.', '')

        if extension in self.allowed:
            return True
        else:
            return False

    def showFiles(self):
        self.files = []

        for file in listdir(self.path):
            if self.IsImage(self, file):
                self.files.append(file)
        return self.files

