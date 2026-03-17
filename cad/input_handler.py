from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from cad_graphics_dot import *
from cad_line import *
# from geometry import *

def handle_input(window=None, event=None, mouse_pos=None, input_type=None, triggered_obj=None, constaints=None):

    if event is not None:
        if event.button() == Qt.RightButton:
            window.reset_buttons_active()
            # window.solver.handle_input(right_button_pressed=True)
            pass
        elif event.button() == Qt.LeftButton:
            coordinates = window.cad.view.mapToScene(event.pos())
            # print(coordinates.x(), coordinates.y())
            # window.solver.handle_input(coordinates=coordinates)

            # print("blood")

    if triggered_obj is not None:
        if triggered_obj == 1:
            to_render = window.solver.handle_input([0, 0], right_button_pressed=False, triggered_obj=1,
                                                   left_button_hold=False, value=None)
            window.setButtonsActive(triggered_obj)
        if triggered_obj == 2:
            window.setButtonsActive(triggered_obj)
            selected = window.cad.scene.grScene.selectedItems()
            if len(selected) != 2:
                # print("you need two objects")
                show_popup(window, "you need two objects")
            else:
                if not isinstance(selected[0], QDMGraphicsDot) or not isinstance(selected[1], QDMGraphicsDot):
                    # print("you need dots")
                    show_popup(window, "you need dots")
                else:
                    # id нормально обрабатывай 
                    dot1 = window.cad.scene.find_dot_by_uuid(selected[0].uuid)
                    dot2 = window.cad.scene.find_dot_by_uuid(selected[1].uuid)
                    # print("tr1")
                    window.solver.handle_input([dot1._x, dot1._y], False, dot1.uuid)
                    window.solver.handle_input([dot2._x, dot2._y], False, dot2.uuid)

                    line = window.solver.handle_input([dot2._x, dot2._y], False, 2)
                    window.create_line_from_coordinates([dot1, dot2], line["CreateSegments"][0][1])
            window.reset_buttons_active()


    

    elif input_type == "selection_changed":
        # print("selection changed")
        pass

    # elif input_type == "add_constraint":
    #     selected = window.cad.scene.grScene.selectedItems()
    #     if len(selected) == 0:
    #         pass
    #     else:
    #         print("whatahell")
    #         window.add_constraint("Distance", selected[0])

    match input_type:
        case "delete_object":
            selected = window.cad.scene.grScene.selectedItems()
            window.cad.scene.removeItems(selected)
            for item in selected:
                print(item.uuid)
                window.solver.handle_delete(item.uuid)
            # window.cad.scene.removeLine(3)

        case "delete_constraint":
            window.solver.handle_delete_constraint(constaints["objects"][0], triggered_obj2=constaints["objects"][1])

        case "add_dot":
            res = window.solver.handle_input([mouse_pos[0], mouse_pos[1]], False, None)
            window.create_dots_from_coordinates([res["CreatePoint"][0][1], res["CreatePoint"][0][2]], res["CreatePoint"][0][0])
            window.reset_buttons_active()

        case "constraint_1":
            selected = window.cad.scene.grScene.selectedItems()
            if len(selected) != 2:
                # print("you need two objects")
                show_popup(window, "you need two objects")
            else:
                if not isinstance(selected[0], QDMGraphicsDot) or not isinstance(selected[1], QDMGraphicsDot):
                    # print("you need dots")
                    show_popup(window, "you need dots")
                else:
                    dot1 = window.cad.scene.find_dot_by_uuid(selected[0].uuid)
                    dot2 = window.cad.scene.find_dot_by_uuid(selected[1].uuid)

                    window.solver.handle_input([dot1._x, dot1._y], False, dot1.uuid)
                    window.solver.handle_input([dot2._x, dot2._y], False, dot2.uuid)

                    res = window.solver.handle_input([dot2._x, dot2._y], False, 3)
                    for dot_move in res["Move"]:
                        dot = window.cad.scene.find_dot_by_uuid(dot_move[0])
                        if dot:
                            dot.setPos(dot_move[1], dot_move[2])

                    window.add_constraint(1, [dot1.uuid, dot2.uuid], "Совпадение двух точек")

        case "constraint_2":
            selected = window.cad.scene.grScene.selectedItems()
            if len(selected) != 2:
                # print("you need two objects")
                show_popup(window, "you need two objects")
            else:
                if not isinstance(selected[0], QDMGraphicsDot) or not isinstance(selected[1], QDMGraphicsDot):
                    # print("you need dots")
                    show_popup(window, "you need dots")
                else:
                    dot1 = window.cad.scene.find_dot_by_uuid(selected[0].uuid)
                    dot2 = window.cad.scene.find_dot_by_uuid(selected[1].uuid)

                    distance, ok = QInputDialog.getInt(
                        window,
                        "Ввод расстояния",
                        "Расстояние",
                        0,
                    )

                    window.solver.handle_input([dot1._x, dot1._y], False, dot1.uuid)
                    window.solver.handle_input([dot2._x, dot2._y], False, dot2.uuid)

                    res = window.solver.handle_input([dot2._x, dot2._y], False, 5, value=distance)
                    for dot_move in res["Move"]:
                        dot = window.cad.scene.find_dot_by_uuid(dot_move[0])
                        if dot:
                            dot.setPos(dot_move[1], dot_move[2])

                    window.add_constraint(2, [dot1.uuid, dot2.uuid], "Расстояние между двумя точками")

        case "constraint_3":
            selected = window.cad.scene.grScene.selectedItems()
            if len(selected) != 2:
                # print("you need two objects")
                show_popup(window, "you need two objects")
            else:
                if not isinstance(selected[0], QDMGraphicsLine) or not isinstance(selected[1], QDMGraphicsLine):
                    # print("you need dots")
                    show_popup(window, "you need lines")
                else:
                    line1 = window.cad.scene.find_line_by_uuid(selected[0].uuid)
                    line2 = window.cad.scene.find_line_by_uuid(selected[1].uuid)

                    window.solver.handle_input([0, 0], False, line1.uuid)
                    window.solver.handle_input([0, 0], False, line2.uuid)

                    res = window.solver.handle_input([0, 0], False, 6)

                    for dot_move in res["Move"]:
                        dot = window.cad.scene.find_dot_by_uuid(dot_move[0])
                        if dot:
                            dot.setPos(dot_move[1], dot_move[2])

                    window.add_constraint(3, [line1.uuid, line2.uuid], "Параллельность двух отрезков")

                    # line1_dot1, line1_dot2 = line1.start_dot, line1.end_dot
                    # line2_dot1, line2_dot2 = line2.start_dot, line2.end_dot

        case "constraint_4":
            selected = window.cad.scene.grScene.selectedItems()
            if len(selected) != 2:
                # print("you need two objects")
                show_popup(window, "you need two objects")
            else:
                if not isinstance(selected[0], QDMGraphicsLine) or not isinstance(selected[1], QDMGraphicsLine):
                    # print("you need dots")
                    show_popup(window, "you need lines")
                else:
                    line1 = window.cad.scene.find_line_by_uuid(selected[0].uuid)
                    line2 = window.cad.scene.find_line_by_uuid(selected[1].uuid)

                    window.solver.handle_input([0, 0], False, line1.uuid)
                    window.solver.handle_input([0, 0], False, line2.uuid)

                    res = window.solver.handle_input([0, 0], False, 7)

                    for dot_move in res["Move"]:
                        dot = window.cad.scene.find_dot_by_uuid(dot_move[0])
                        if dot:
                            dot.setPos(dot_move[1], dot_move[2])

                    window.add_constraint(4, [line1.uuid, line2.uuid], "Перпендикулярность двух отрезков")

        case "constraint_5":
            selected = window.cad.scene.grScene.selectedItems()
            if len(selected) != 1:
                # print("you need two objects")
                show_popup(window, "you need one object")
            else:
                if not isinstance(selected[0], QDMGraphicsLine):
                    # print("you need dots")
                    show_popup(window, "you need line")
                else:
                    line1 = window.cad.scene.find_line_by_uuid(selected[0].uuid)
                    window.solver.handle_input([0, 0], False, line1.uuid)

                    res = window.solver.handle_input([0, 0], False, 8)
                    for dot_move in res["Move"]:
                        dot = window.cad.scene.find_dot_by_uuid(dot_move[0])
                        if dot:
                            dot.setPos(dot_move[1], dot_move[2])

                    window.add_constraint(5, [line1.uuid], "Вертикальность отрезка")

        case "constraint_6":
            selected = window.cad.scene.grScene.selectedItems()
            if len(selected) != 1:
                # print("you need two objects")
                show_popup(window, "you need one object")
            else:
                if not isinstance(selected[0], QDMGraphicsLine):
                    # print("you need dots")
                    show_popup(window, "you need line")
                else:
                    line1 = window.cad.scene.find_line_by_uuid(selected[0].uuid)
                    window.solver.handle_input([0, 0], False, line1.uuid)

                    res = window.solver.handle_input([0, 0], False, 9)
                    for dot_move in res["Move"]:
                        dot = window.cad.scene.find_dot_by_uuid(dot_move[0])
                        if dot:
                            dot.setPos(dot_move[1], dot_move[2])
                    window.add_constraint(6, [line1.uuid], "Горизонтальность отрезка")

        case "constraint_7":
            selected = window.cad.scene.grScene.selectedItems()
            if len(selected) != 2:
                # print("you need two objects")
                show_popup(window, "you need two objects")
            else:
                if not isinstance(selected[0], QDMGraphicsLine) or not isinstance(selected[1], QDMGraphicsLine):
                    # print("you need dots")
                    show_popup(window, "you need lines")
                else:
                    line1 = window.cad.scene.find_line_by_uuid(selected[0].uuid)
                    line2 = window.cad.scene.find_line_by_uuid(selected[1].uuid)

                    angle, ok = QInputDialog.getInt(
                        window,
                        "Ввод угла",
                        "Угол",
                        0,
                        0,
                        360
                    )

                    window.solver.handle_input([0, 0], False, line1.uuid)
                    window.solver.handle_input([0, 0], False, line2.uuid)

                    res = window.solver.handle_input([0, 0], False, 10, value=angle)
                    for dot_move in res["Move"]:
                        dot = window.cad.scene.find_dot_by_uuid(dot_move[0])
                        if dot:
                            dot.setPos(dot_move[1], dot_move[2])

                    window.add_constraint(7, [line1.uuid, line2.uuid], "Угол между двумя отрезками")

        case "constraint_8":
            selected = window.cad.scene.grScene.selectedItems()
            if len(selected) != 2:
                # print("you need two objects")
                show_popup(window, "you need two objects")
            else:
                # NET PROVERKI
                # if not isinstance(selected[0], QDMGraphicsLine, QDMGraphicsDot) or not isinstance(selected[1], QDMGraphicsLine, QDMGraphicsDot):
                #     # print("you need dots")
                #     show_popup(window, "you need dot and line")
                # else:
                    if isinstance(selected[0], QDMGraphicsLine):
                        line = window.cad.scene.find_line_by_uuid(selected[0].uuid)
                        dot = window.cad.scene.find_dot_by_uuid(selected[1].uuid)
                    else:
                        dot = window.cad.scene.find_dot_by_uuid(selected[0].uuid)
                        line = window.cad.scene.find_line_by_uuid(selected[1].uuid)

                    print(dot, line)

                    window.solver.handle_input([0, 0], False, dot.uuid)
                    window.solver.handle_input([0, 0], False, line.uuid)
                    
                    res = window.solver.handle_input([0, 0], False, 11)
                    for dot_move in res["Move"]:
                        dot = window.cad.scene.find_dot_by_uuid(dot_move[0])
                        if dot:
                            dot.setPos(dot_move[1], dot_move[2])

                    window.add_constraint(8, [dot.uuid, line.uuid], "Принадлежность точки прямой")


        case "constraint_9":
            selected = window.cad.scene.grScene.selectedItems()
            if len(selected) != 1:
                # print("you need two objects")
                show_popup(window, "you need one object")
            else:
                if not isinstance(selected[0], QDMGraphicsDot):
                    # print("you need dots")
                    show_popup(window, "you need dot")
                else:
                    dot = window.cad.scene.find_dot_by_uuid(selected[0].uuid)
                    window.solver.handle_input([0, 0], False, dot.uuid)

                    res = window.solver.handle_input([0, 0], False, 12)
                    for dot_move in res["Move"]:
                        dot = window.cad.scene.find_dot_by_uuid(dot_move[0])
                        if dot:
                            dot.setPos(dot_move[1], dot_move[2])

                    window.add_constraint(9, [dot.uuid], "Фиксация точки")

        case "render":
            selected = window.cad.scene.grScene.selectedItems()
            res = window.solver.handle_move([mouse_pos[0], mouse_pos[1]], selected[0].uuid)
            for dot_move in res["Move"]:
                dot = window.cad.scene.find_dot_by_uuid(dot_move[0])
                if dot:
                   dot.setPos(dot_move[1], dot_move[2])
            pass

                    

    
    pass


def show_popup(window, text):
    msg = QMessageBox(window)
    msg.setIcon(QMessageBox.Question)
    msg.setText(text)
    msg.setStandardButtons(QMessageBox.Ok)
    result = msg.exec()