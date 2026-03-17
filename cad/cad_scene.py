from cad_graphics_scene import QDMGraphicsScene
from cad_graphics_dot import *
from cad_graphics_line import *

class Scene():

    def __init__(self):
        self.dots = []
        self.lines = []

        self.scene_width = 64000
        self.scene_height = 64000

        self.initUI()

    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def find_dot_by_uuid(self, uuid):
        for dot in self.dots:
            if dot.uuid == uuid:
                return dot
        return None
    
    def find_line_by_uuid(self, uuid):
        for line in self.lines:
            if line.uuid == uuid:
                return line
        return None
    
    # experimental
    # def add_dot(self, dot):
    #     from 

    def addDot(self, dot):
        self.dots.append(dot)
        # print(self.dots)
        # self.grScene.addItem(dot.grNode) # хз правильно ли
        return dot

    def addLine(self, line):
        print("ADDE")
        self.lines.append(line)
        return line

    def removeDot(self, uuid):
        dot = self.find_dot_by_uuid(uuid)
        if self.dotHasLine(dot):
            print("some line own this dot!")
            return
        
        self.dots.remove(dot)
        self.grScene.removeItem(dot.grNode)

    def dotHasLine(self, dot):
        for line in self.lines:
            if line.start_dot == dot or line.end_dot == dot:
                return True
        return False

    def removeLine(self, uuid):
        line = self.find_line_by_uuid(uuid)
        if line is None:
            print("nope")
            return

        self.lines.remove(line)
        self.grScene.removeItem(line.grLine)
        print(self.lines)


    def removeItems(self, items):
        for item in items:
            if isinstance(item, QDMGraphicsDot):
                self.removeDot(item.uuid)
            if isinstance(item, QDMGraphicsLine):
                self.removeLine(item.uuid)