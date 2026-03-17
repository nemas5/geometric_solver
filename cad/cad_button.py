from PyQt5.QtWidgets import *

class CADButton(QPushButton):
    def __init__(self, uuid, parent=None):
        super().__init__(parent)
        self.uuid = uuid