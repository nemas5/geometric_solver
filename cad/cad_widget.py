from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from cad_scene import Scene
from cad_dot import Dot
from cad_line import Line
from cad_graphics_view import QDMGraphicsView


class CadWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # create graphics scene
        self.scene = Scene()
        # self.grScene = self.scene.grScene

        # self.cad_window.add_constraint("Расстояние", dot1, dot2)
       
        # create graphics view
        self.view = QDMGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("AutoAD")
        self.show()

        # self.addDebugContent()

    def addConstraint(self, uuid):
        dot = self.scene.find_dot_by_uuid(uuid)
        self.window().add_constraint("Distance", dot)


    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)

        rect = self.grScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        # text = self.grScene.addText("This is text", QFont("Ubuntu"))
        # text.setFlag(QGraphicsItem.ItemIsSelectable)
    
        widget = QPushButton("Hello World")
        proxy1 = self.grScene.addWidget(widget)

        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 30)

        line = self.grScene.addLine(-200, -100, 400, 200, outlinePen)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)


