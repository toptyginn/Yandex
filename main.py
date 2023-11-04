import Photoshop
import Paint
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


class Main(QMainWindow, Paint, Photoshop):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Photoshop.Photoshop()
    ex.show()
    sys.exit(app.exec())