from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from input_handler import *

class QDMGraphicsView(QGraphicsView):
    scenePosChanged = pyqtSignal(int, int)

    def __init__(self, grScene, window=None, parent=None):
        super().__init__(parent)
        self.grScene = grScene

        self.initUI()
        self.setScene(self.grScene)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.on_timeout)
        self.hold_ticks = 0
        self.hold_fired = False

        # self.render_timer = QTimer(self)
        # self.timer.setInterval(1000)
        # self.timer.timeout.connect(self.render_on_timeout)


        # self.window = window

        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 15] # min and max zoom
        self.last_scene_mouse_position = QPoint(0,0)

        # HANDLE INPUT
        self.grScene.selectionChanged.connect(self.on_selection_changed)

        # self.timer = QTimer(self)
        
    def start_single_shot(self):
        QTimer.singleShot(2000, self.on_timeout)

    def on_timeout(self):
        self.timer.start()
        selected = self.grScene.selectedItems()
        if len(selected) == 0:
            print("простое зажатие")
            return
        if len(selected) > 1 or not isinstance(selected[0], QDMGraphicsDot):
            print("простое зажатие")
            return

        print("зажали кнопку", selected[0].x, selected[0].y)
        current_pos = self.mapToScene(self.mapFromGlobal(QCursor.pos()))
        print(current_pos)
        handle_input(self.window(), input_type="render", mouse_pos=[current_pos.x(), current_pos.y()])
        pass


    def render_on_timeout(self):
        print("пересчитываем")
        

    def on_selection_changed(self):
        handle_input(self.window(), input_type="selection_changed")


    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)


    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        
        # print(self.window().active_button is not None)
        # print(event.button() == Qt.LeftButton)
        # отладка

        scenepos = self.mapToScene(event.pos())
        self.last_scene_mouse_position = scenepos
        self.scenePosChanged.emit(int(self.last_scene_mouse_position.x()), int(self.last_scene_mouse_position.y()))

        

        super().mouseMoveEvent(event)

    
    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                   Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())

        super().mousePressEvent(fakeEvent)


    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                   Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)


    # TEST TEST TEST
    def leftMouseButtonPress(self, event):
        # self.hold_ticks = 0
        # self.hold_fired = False
        self.timer.start()

        handle_input(window=self.window(), event=event)
        scenepos = self.mapToScene(event.pos())
        if event.button() == Qt.LeftButton and self.window().active_button == 1:
            # result = self.window().test_handle_input(triggered_obj=None)
            coord = [scenepos.x(), scenepos.y()]
            self.window().coordinates_list.append(coord)
            handle_input(window=self.window(), event=event, mouse_pos=coord, input_type="add_dot")
            # result = self.window().test_handle_input(triggered_obj=None)
            # self.window().process_handle_result(result)
        if event.button() == Qt.LeftButton and self.window().active_button == 2:
            selected = self.grScene.selectedItems()
            if len(selected) < 2:
                print("you need two dots bastard!")
        return super().mousePressEvent(event)
    

    def leftMouseButtonRelease(self, event):
        self.timer.stop()
        # selected = self.grScene.selectedItems()
        # if len(selected) == 0:
        #     print("простое зажатие")
        #     return
        # if len(selected) > 1 or not isinstance(selected[0], QDMGraphicsDot):
        #     print("простое зажатие")
        #     return

        # print("зажали кнопку", selected[0].x, selected[0].y)
        # current_pos = self.mapToScene(self.mapFromGlobal(QCursor.pos()))
        # print(current_pos)
        # handle_input(self.window(), input_type="render", mouse_pos=[current_pos.x(), current_pos.y()])

        return super().mouseReleaseEvent(event)
    

    def rightMouseButtonPress(self, event):
        # self.start_single_shot()
        # print(self.grScene.selectedItems())
        handle_input(self.window(), event=event)
        return super().mousePressEvent(event)
    
    def rightMouseButtonRelease(self, event):
        return super().mouseReleaseEvent(event)
    

    def wheelEvent(self, event):
        # calculate zoom factor
        zoomOutFactor = 1 / self.zoomInFactor

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)


