import sys
from PySide6 import QtWidgets
from .main_window import MainWindow

def run():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(lang="ru")
    w.resize(1100, 700)
    w.show()
    sys.exit(app.exec())
