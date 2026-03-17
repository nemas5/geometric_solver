from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from cad_widget import *
from cad_button import CADButton
from input_handler import handle_input
from cad_graphics_dot import *
from cad_graphics_line import *
from geometry import *

class CADWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cad = None
        self.active_button = None
        self.coordinates_list = []
        self.constraints = []
        self.solver = Solver()

        self.initUI()

        self.set_background_palette("#2c3e50")

        # self.add_constraint("Расстояние", "Point_1", "Point_2")


    def initUI(self):

        self.load_styles()

        menubar = self.menuBar()

        # СОЗДАНИЕ ДОКА С ОГРАНИЧЕНИЯМИ
        constraints_dock = QDockWidget("Constraints", self)
        self.addDockWidget(Qt.RightDockWidgetArea, constraints_dock)

        constraints_container = QWidget()
        constraints_layout = QVBoxLayout(constraints_container)
        constraints_layout.setContentsMargins(4, 4, 4, 4)
        constraints_layout.setSpacing(4)

        # кнопка удаления ограничений
        self.clear_constraints_btn = QPushButton("🗑️ Удалить выделенное")
        self.clear_constraints_btn.clicked.connect(self.delete_selected_constraints)

        
        self.constraints_list = QListWidget()
        self.constraints_list.setAlternatingRowColors(True)
        self.constraints_list.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.constraints_list.customContextMenuRequested.connect(self.show_context_menu)


        constraints_layout.addWidget(self.clear_constraints_btn)
        constraints_layout.addWidget(self.constraints_list, 1)

        constraints_dock.setWidget(constraints_container)


        # СОЗДАНИЕ ДОКА С КНОПКАМИ
        buttons_dock = QDockWidget("buttons", self)
        self.addDockWidget(Qt.TopDockWidgetArea, buttons_dock)

        title_widget = QWidget()
        layout = QHBoxLayout(title_widget)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(4)

        # СОЗДАНИЕ ТОЧЕК И ПРЯМЫХ
        self.btn1 = QPushButton("Add dot")
        self.btn1.setIcon(QIcon('icons/dot.png'))
        self.btn1.setIconSize(QSize(24, 24))

        # self.btn1.setProperty("class", "inactive")
        self.btn2 = QPushButton("Add line")
        self.btn2.setIcon(QIcon('icons/line.png'))
        self.btn2.setIconSize(QSize(24, 24))

        # ОГРАНИЧЕНИЯ
        # совпадение двух точек
        self.btn3 = QPushButton()
        self.btn3.setIcon(QIcon('icons/1.png'))
        self.btn3.setIconSize(QSize(24, 24))

        # расстояние между двумя точками
        self.btn5 = QPushButton()
        self.btn5.setIcon(QIcon('icons/2.png'))
        self.btn5.setIconSize(QSize(24, 24))

        # параллельность двух отрезков
        self.btn6 = QPushButton()
        self.btn6.setIcon(QIcon('icons/3.png'))
        self.btn6.setIconSize(QSize(24, 24))

        # перпендикулярность двух отрезков
        self.btn7 = QPushButton()
        self.btn7.setIcon(QIcon('icons/4.png'))
        self.btn7.setIconSize(QSize(24, 24))

        # вертикальность отрезка
        self.btn8 = QPushButton()
        self.btn8.setIcon(QIcon('icons/5.png'))
        self.btn8.setIconSize(QSize(24, 24))

        # горизонтальность отрезка
        self.btn9 = QPushButton()
        self.btn9.setIcon(QIcon('icons/6.png'))
        self.btn9.setIconSize(QSize(24, 24))

        # угол между отрезками
        self.btn10 = QPushButton()
        self.btn10.setIcon(QIcon('icons/7.png'))
        self.btn10.setIconSize(QSize(24, 24))

        # принадлежность точки прямой
        self.btn11 = QPushButton()
        self.btn11.setIcon(QIcon('icons/8.png'))
        self.btn11.setIconSize(QSize(24, 24))

        # фиксация точки
        self.btn12 = QPushButton()
        self.btn12.setIcon(QIcon('icons/9.png'))
        self.btn12.setIconSize(QSize(24, 24))

        # УДАЛЕНИЕ ОБЬЕКТОВ
        self.btn4 = QPushButton("DELETE")
        self.btn4.setIcon(QIcon('icons/delete.png'))
        self.btn4.setIconSize(QSize(24, 24))

        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)

        layout.addWidget(self.btn3)
        layout.addWidget(self.btn5)
        layout.addWidget(self.btn6)
        layout.addWidget(self.btn7)
        layout.addWidget(self.btn8)
        layout.addWidget(self.btn9)
        layout.addWidget(self.btn10)
        layout.addWidget(self.btn11)
        layout.addWidget(self.btn12)

        layout.addWidget(self.btn4)
        
        layout.addStretch()

        buttons_dock.setTitleBarWidget(title_widget)

        # подключение кнопок
        self.btn1.clicked.connect(self.onButton1Clicked)
        self.btn2.clicked.connect(self.onButton2Clicked)
        self.btn3.clicked.connect(self.onButton3Clicked)
        self.btn4.clicked.connect(self.onButton4Clicked)
        self.btn5.clicked.connect(self.onButton5Clicked)
        self.btn6.clicked.connect(self.onButton6Clicked)
        self.btn7.clicked.connect(self.onButton7Clicked)
        self.btn8.clicked.connect(self.onButton8Clicked)
        self.btn9.clicked.connect(self.onButton9Clicked)
        self.btn10.clicked.connect(self.onButton10Clicked)
        self.btn11.clicked.connect(self.onButton11Clicked)
        self.btn12.clicked.connect(self.onButton12Clicked)


        fileMenu = menubar.addMenu('Построение эскиза')
        act = QAction('New', self)
        act.setShortcut('Ctrl+N')
        act.setToolTip("Monster Energy")
        act.triggered.connect(self.onFuckNew)
        fileMenu.addAction(act)

        
        self.cad = CadWidget(self.cad)
        self.setCentralWidget(self.cad)

        # status bar
        # self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.status_mouse_pos.setStyleSheet("color: white;") 
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        self.cad.view.scenePosChanged.connect(self.onScenePosChanged)


        self.setGeometry(200, 200, 1000, 600)
        self.setWindowTitle("AutoAD")
        self.show()

    def set_background_palette(self, color_name):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color_name))
        # palette.setBrush(QPalette.Window, QBrush(Qt.white, Qt.DiagCrossPattern))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def load_styles(self):
        """Загружает стили из файла"""
        try:
            with open('qss/style.qss', 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
                print("read")
        except FileNotFoundError:
            print("styles.qss не найден")


    def onFuckNew(self):
        print("Mmmhhhmhm...")

    def onScenePosChanged(self, x, y):
        self.status_mouse_pos.setText("Scene Pos: [%d, %d]" % (x, y))

    # CONSTRAINTS LOGIC
    def add_constraint(self, type, objects, desc=None):

        constraint_text = f"{type}, {desc}: {objects}"
        list_item = QListWidgetItem(constraint_text)
        list_item.setData(Qt.UserRole, len(self.constraints))
        self.constraints_list.addItem(list_item)
        self.constraints.append({
            'type': type,
            'objects': objects
        })

    def delete_selected_constraints(self):
        selected_items = self.constraints_list.selectedItems()
        if not selected_items:
            return
        
        rows = sorted(
            [self.constraints_list.row(item) for item in selected_items],
            reverse=True
        )

        for row in rows: # main logic here
            if 0 <= row < len(self.constraints):
                # del self.constraints[row]
                print(self.constraints[row])
                handle_input(self, input_type="delete_constraint", constaints=self.constraints[row])

        for row in rows:
            item = self.constraints_list.takeItem(row)
            # del item

        handle_input(self, input_type="udalenie contraint")
                
        print(selected_items)



    # BUTTONS ACTIONS
    def onButton1Clicked(self):
        handle_input(self, triggered_obj=1)

    def onButton2Clicked(self):
        handle_input(self, triggered_obj=2)

    def onButton3Clicked(self):
        handle_input(self, input_type="constraint_1")

    def onButton5Clicked(self):
        handle_input(self, input_type="constraint_2")

    def onButton6Clicked(self):
        handle_input(self, input_type="constraint_3")

    def onButton7Clicked(self):
        handle_input(self, input_type="constraint_4")

    def onButton8Clicked(self):
        handle_input(self, input_type="constraint_5")

    def onButton9Clicked(self):
        handle_input(self, input_type="constraint_6")

    def onButton10Clicked(self):
        handle_input(self, input_type="constraint_7")

    def onButton11Clicked(self):
        handle_input(self, input_type="constraint_8")

    def onButton12Clicked(self):
        handle_input(self, input_type="constraint_9")

    def onButton4Clicked(self):
        handle_input(self, input_type="delete_object")

   


    # TEST FUNCTIONAL

    # def test_handle_input(self, triggered_obj):
    #     if triggered_obj:
    #         print(f"Button {triggered_obj} is active")
    #         return (triggered_obj, )
        
    #     # ЗАХАРДКОЖЕНО!!!
    #     if self.coordinates_list:
    #         print(f"Sending {len(self.coordinates_list)} coordinates for drawing")
    #         points_data = [(coord, len(self.coordinates_list) + i) for i, coord in enumerate(self.coordinates_list)]
    #         # coords = self.coordinates_list.copy()
    #         self.coordinates_list.clear()
    #         return (points_data, )
        
    #     return None
        


    # def process_handle_result(self, result):
    #     if not result:
    #         return
        
    #     data = result[0]

    #     if isinstance(data, int):
    #         self.setButtonsActive(data)

    #     elif isinstance(data, list):
    #         self.create_dots_from_coordinates(data)
    #         self.reset_buttons_active()

    #     return
    
    
    def create_dots_from_coordinates(self, coord, uuid):
        if self.cad and self.cad.scene:
                
                x, y = coord[0], coord[1]

                dot = self.cad.scene.find_dot_by_uuid(uuid)
                # тут возможно стоит делать set pos просто
                if dot:
                    # dot.x = x
                    # dot.y = y
                    # self.cad.scene.update_dot_graphics(dot)
                    dot.setPos(x, y)
                    print(f"dot has been updated")
                else:
                    new_dot = self.cad.scene.addDot(Dot(self.cad.scene, uuid=uuid, x=x, y=y))
                    print(f"Created new dot with uuid={uuid}")


    def create_line_from_coordinates(self, dots, uuid):
        if self.cad and self.cad.scene:
            dot1 = dots[0]
            dot2 = dots[1]
            line = self.cad.scene.find_line_by_uuid(uuid)

            if line:
                print("already exits")
            else:
                new_line = self.cad.scene.addLine(Line(self.cad.scene, uuid, dot1, dot2))

    
    def reset_buttons_active(self):
        # self.btn1.setProperty("class", "inactive")
        self.btn1.setStyleSheet("background-color: #CCCCCC;")
        self.btn2.setStyleSheet("background-color: #CCCCCC;")
        self.btn3.setStyleSheet("background-color: #CCCCCC;")
        self.btn1.setEnabled(True)
        self.btn2.setEnabled(True)
        self.btn3.setEnabled(True)
        self.active_button = None
    

    def setButtonsActive(self, button_id):
        """Закрашивает активную кнопку, остальные - серые"""
        # Все кнопки серые
        # self.btn1.setStyleSheet("background-color: #CCCCCC;")
        # self.btn2.setStyleSheet("background-color: #CCCCCC;")
        # self.btn3.setStyleSheet("background-color: #CCCCCC;")

        # print(f"setting button active %d", button_id)

        self.reset_buttons_active()

        self.btn1.setEnabled(False)
        self.btn2.setEnabled(False)
        self.btn3.setEnabled(False)

        if button_id == 1:
            # self.btn1.setProperty("class", "active")
            self.btn1.setEnabled(True)
            self.btn1.setStyleSheet("background-color: #4EEA00; color: white;")
        if button_id == 2:
            self.btn2.setEnabled(True)
            self.btn2.setStyleSheet("background-color: #4EEA00; color: white;")
        if button_id == 3:
            self.btn3.setEnabled(True)
            self.btn3.setStyleSheet("background-color: #4EEA00; color: white;")

        self.active_button = button_id        
        # Активная кнопка зеленая
        # active_button.setStyleSheet("background-color: #4EEA00; color: white;")


