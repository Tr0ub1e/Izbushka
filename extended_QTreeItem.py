from PyQt5.QtWidgets import QTreeWidgetItem

class Ext_Item(QTreeWidgetItem):

    def __init__(self, parent, id_item=None):
        super(Ext_Item, self).__init__(parent)
        self.id_item = id_item
