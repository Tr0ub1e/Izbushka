from PyQt5 import QtWidgets
from count_parts import Ui_Dialog


class Count_Parts(QtWidgets.QDialog):

    def __init__(self, max_v):
        super(Count_Parts, self).__init__()

        self.dial_ui = Ui_Dialog()

        self.dial_ui.setupUi(self)
        self.dial_ui.retranslateUi(self)

        self.fill_data(max_v)

        self.dial_ui.pushButton.clicked.connect(self.get_number)
        self.value = 0

        self.exec_()

    def fill_data(self, digit):
        self.dial_ui.countParts.setMaximum(int(digit))

    def get_number(self):

        self.value = self.dial_ui.countParts.value()
        self.close()
