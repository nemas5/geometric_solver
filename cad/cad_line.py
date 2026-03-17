from cad_graphics_line import QDMGraphicsLine

class Line():
    def __init__(self, scene, uuid, dot1, dot2):

        self.scene = scene
        self.uuid = uuid

        self.start_dot = dot1
        self.end_dot = dot2

        self.grLine = QDMGraphicsLine(self, uuid)

        # self.scene.addLine(self)
        self.scene.grScene.addItem(self.grLine)