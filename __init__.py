from PyQt5 import QtWidgets
import sys
import views.FilePicker as FilePicker

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = FilePicker.Ui_FilePicker()
ui.setup_ui(MainWindow)
MainWindow.show()
sys.exit(app.exec_())