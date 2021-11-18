import os


class FileFinder:
    path = '.'
    allowed = ['jpg', 'png']

    @staticmethod
    def is_image(image):
        extension_index = -1;

        for i in range(len(image)):
            if image[i] == '.':
                extension_index = i

        extension = image[int(extension_index):int(len(image))].replace('.', '')

        if extension in FileFinder.allowed:
            return True
        else:
            return False

    @staticmethod
    def show_files():
        files = []

        for file in os.listdir(FileFinder.path):
            if FileFinder.is_image(file):
                files.append(file)

        return files
