from cad_graphics_dot import QDMGraphicsDot

class Dot():
    def __init__(self, scene, uuid, x, y):
        self.scene = scene
        self.uuid = uuid

        self._x = x
        self._y = y

        self.grNode = QDMGraphicsDot(self, self.uuid)

        # self.scene.addDot(self)
        self.scene.grScene.addItem(self.grNode)

    @property
    def pos(self):
        return self.grNode.pos()    # QPointF ... pos.x(), pos.y()
    
    def setPos(self, x, y):
        self._x = x
        self._y = y
        self.grNode.setPos(x, y)
