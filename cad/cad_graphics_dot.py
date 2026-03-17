from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QDMGraphicsDot(QGraphicsItem):
    def __init__(self, dot, uuid, parent=None):
        super().__init__(parent)
        self.dot = dot
        print(dot._x, dot._y)

        self.uuid = uuid

        self.width = 10
        self.height = 10

        self._pen_default = QPen(QColor("#7F000000"))
        self._brush_default = QBrush(QColor("#FFF2F2F9"))

        self._pen_selected = QPen(QColor("#4EEA00B7"))
        self._brush_selected = QBrush(QColor("#FFFFA637"))

        self.setPos(self.dot._x, self.dot._y)
        self.initUI()

    def boundingRect(self):
        # return QRectF(0, 0, self.width, self.height).normalized
        return QRectF(-self.width/2, -self.height/2, self.width, self.height).normalized()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    # возможно стоит перенести эту логику в node_dot
    @property 
    def x(self): return self.dot._x

    @x.setter
    def x(self, value):
        self.dot._x = value

    @property 
    def y(self): return self.dot._y

    @y.setter
    def y(self, value):
        self.dot._y = value

    def paint(self, painter, option, widget = ...):

        # paint dot

        path_outline = QPainterPath()
        # path_outline.addRoundedRect(0, 0, self.width, self.height, 1, 1) 
        path_outline.addEllipse(-self.width/2, -self.height/2, self.width, self.height)
        # path_outline.addEllipse(0, 0, self.width, self.height)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(self._brush_default if not self.isSelected() else self._brush_selected)
        painter.drawPath(path_outline.simplified())

        # return super().paint(painter, option, widget)