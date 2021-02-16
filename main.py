from PyQt5 import QtWidgets, QtGui
from mainframe import MainFrame
import sys


def main():

    app = QtWidgets.QApplication(sys.argv)
    winapp = MainFrame()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
