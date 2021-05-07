from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
import sys
from mainframe import MainFrame

class myThread(QThread):

    def run(self):
        import time
        time.sleep(5)

class SplashMain(MainFrame):

    def __init__(self):
        super(SplashMain, self).__init__()
        self.load()


    def load(self):
        splash = QSplashScreen()
        splash.setPixmap(QPixmap('ui/image.jpg'))
        splash.show()

        t = myThread(parent=self)
        t.run()
        t.finished.connect(t.deleteLater)
        t.finished.connect(splash.close)
        t.finished.connect(splash.deleteLater)
        t.start()
        


def main():
    app = QApplication(sys.argv)

    window = SplashMain()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
