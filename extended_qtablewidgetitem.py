from PyQt5.QtWidgets import QTableWidgetItem

class Ext_TableItem(QTableWidgetItem):

    def __init__(self, content, id_item=None):
        super(Ext_TableItem, self).__init__(content)
        self.id_item = id_item
