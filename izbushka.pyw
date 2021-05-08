from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
import sys
from mainframe import MainFrame


def main():
    app = QApplication(sys.argv)

    splash = QSplashScreen()
    splash.setPixmap(QPixmap('ui/image.jpg'))
    splash.show()

    window = MainFrame()
    window.show()
    splash.finish(window)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
