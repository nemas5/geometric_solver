from uuid import uuid4, UUID
from typing import List, Dict
from collections import deque
import math

import numpy as np


class Point:
    def __init__(self, x: float, y: float):
        self.coordinates = [x, y]
        self.id = uuid4()

    def get_id(self):
        return self.id

    def get_x(self):
        return self.coordinates[0]

    def get_y(self):
        return self.coordinates[1]

    def update_coordinates(self, x: float, y: float):
        self.coordinates = [self.coordinates[0] + x, self.coordinates[1] + y]

    def new_coordinates(self, xy):
        self.coordinates = xy


class Segment:
    def __init__(self, point_1: Point, point_2: Point):
        self.points = [point_1, point_2]
        self.id = uuid4()

    def get_id(self):
        return self.id

    def get_points(self):
        return self.points


# Для каждого ограничения возвращается матрица (или две) и словарь
# В словаре указаны uuid элементов, к которым относятся строки
# Расположение в порядке x1-y1-x2-y2-...-lambda
def constraint_1(point1: Point, point2: Point,
                 delta_x1: float, delta_y1: float,
                 delta_x2: float, delta_y2: float,
                 lmb_x: float, lmb_y: float):
    local_matrix = [
        [0,   0,   0,   0,  -1,   0],
        [0,   0,   0,   0,   0,  -1],
        [0,   0,   0,   0,   1,   0],
        [0,   0,   0,   0,   0,   1],
        [-1,  0,   1,   0,   0,   0] ,
        [0,  -1,   0,   1,   0,   0]
    ]

    local_vector = [
        -lmb_x,
        -lmb_y,
        lmb_x,
        lmb_y,
        (point2.get_x() + delta_x2) - (point1.get_x() + delta_x1),
        (point2.get_y() + delta_y2) - (point1.get_y() + delta_y1)
    ]

    return [local_matrix, local_vector, {0: point1.get_id(), 1: point2.get_id()}]


def constraint_2(point1: Point, point2: Point,
                 delta_x1: float, delta_y1: float,
                 delta_x2: float, delta_y2: float,
                 lmb: float, d: float):
    a = (point2.get_x() + delta_x2) - (point1.get_x() + delta_x1)
    b = (point2.get_y() + delta_y2) - (point1.get_y() + delta_y1)
    local_matrix = [
        [2*lmb,  0,            -2*lmb, 0,             -2*a],
        [0,             2*lmb,  0,            -2*lmb, -2*b],
        [-2*lmb, 0,             2*lmb, 0,              2*a],
        [0,            -2*lmb,  0,             2*lmb,  2*b],
        [-2*a,         -2*b,           2*a,           2*b,             0]
    ]
    local_vector = [-2 * lmb * a, -2 * lmb * b, 2 * lmb * a, 2 * lmb * b, a * a + b * b - d * d]
    return [local_matrix, local_vector, {0: point1.get_id(), 1: point2.get_id()}]


def constraint_3(segment1: Segment, segment2: Segment,
                 dx1: float, dy1: float,
                 dx2: float, dy2: float,
                 dx3: float, dy3: float,
                 dx4: float, dy4: float,
                 lmb: float):
    p1, p2 = segment1.get_points()
    p3, p4 = segment2.get_points()

    x1, y1 = p1.get_x() + dx1, p1.get_y() + dy1
    x2, y2 = p2.get_x() + dx2, p2.get_y() + dy2
    x3, y3 = p3.get_x() + dx3, p3.get_y() + dy3
    x4, y4 = p4.get_x() + dx4, p4.get_y() + dy4

    u = x2 - x1
    v = y2 - y1
    p = x4 - x3
    q = y4 - y3

    local_matrix = [
        [0,    0,  0,   0, 0, -lmb,  0,  lmb, -q],
        [0,    0,  0,   0, 0,  0,    0,  0,    p],
        [0,    0,  0,   0, 0,  lmb,  0, -lmb,  q],
        [0,    0,  0,   0, 0,  0,    0,  0,   -p],
        [0,    0,  0,   0, 0,  0,    0,  0,    v],
        [-lmb, 0,  lmb, 0, 0,  0,    0,  0,   -u],
        [0,    0,  0,   0, 0,  0,    0,  0,   -v],
        [lmb,  0, -lmb, 0, 0,  0,    0,  0,    u],
        [-q,   p,  q,  -p, v, -u,   -v,  u,    0]
    ]

    local_vector = [
        -lmb * q,
         lmb * p,
         lmb * q,
        -lmb * p,
         lmb * v,
        -lmb * u,
        -lmb * v,
         lmb * u,
         u * q - v * p
    ]
    return [local_matrix, local_vector, {0: p1.get_id(), 1: p2.get_id(), 2: p3.get_id(), 3: p4.get_id()}]


def constraint_4(segment1: Segment, segment2: Segment,
                 dx1: float, dy1: float,
                 dx2: float, dy2: float,
                 dx3: float, dy3: float,
                 dx4: float, dy4: float,
                 lmb: float):
    p1, p2 = segment1.get_points()
    p3, p4 = segment2.get_points()

    x1, y1 = p1.get_x() + dx1, p1.get_y() + dy1
    x2, y2 = p2.get_x() + dx2, p2.get_y() + dy2
    x3, y3 = p3.get_x() + dx3, p3.get_y() + dy3
    x4, y4 = p4.get_x() + dx4, p4.get_y() + dy4


    u = x2 - x1
    v = y2 - y1
    p = x4 - x3
    q = y4 - y3

    local_matrix = [
        [0, 0, 0, 0, lmb, 0, -lmb, 0, -p],
        [0, 0, 0, 0, 0, lmb, 0, -lmb, -q],
        [0, 0, 0, 0, -lmb, 0, lmb, 0, p],
        [0, 0, 0, 0, 0, -lmb, 0, lmb, q],
        [lmb, 0, -lmb, 0, 0, 0, 0, 0, -u],
        [0, lmb, 0, -lmb, 0, 0, 0, 0, -v],
        [-lmb, 0, lmb, 0, 0, 0, 0, 0, u],
        [0, -lmb, 0, lmb, 0, 0, 0, 0, v],
        [-p, -q, p, q, -u, -v, u, v, 0]
    ]

    local_vector = [
        -lmb * p,
        -lmb * q,
        lmb * p,
        lmb * q,
        -lmb * u,
        -lmb * v,
        lmb * u,
        lmb * v,
        u * p + v * q
    ]
    return [local_matrix, local_vector, {0: p1.get_id(), 1: p2.get_id(), 2: p3.get_id(), 3: p4.get_id()}]


def constraint_5(segment1: Segment,
                 dx1: float, dy1: float,
                 dx2: float, dy2: float,
                 lmb: float):
    p1, p2 = segment1.get_points()

    g = (p2.get_x() + dx2) - (p1.get_x() + dx1)

    local_matrix = [
        [0, 0, 0, 0, -1],
        [0, 0, 0, 0,  0],
        [0, 0, 0, 0,  1],
        [0, 0, 0, 0,  0],
        [-1, 0, 1, 0, 0]
    ]

    local_vector = [
        lmb * (-1),
        lmb * (0),
        lmb * (1),
        lmb * (0),
        g
    ]

    return [local_matrix, local_vector, {0: p1.get_id(), 1: p2.get_id()}]


def constraint_6(segment1: Segment,
                 dx1: float, dy1: float,
                 dx2: float, dy2: float,
                 lmb: float):

    p1, p2 = segment1.get_points()

    g = (p2.get_y() + dy2) - (p1.get_y() + dy1)


    local_matrix = [
        [0, 0, 0, 0,  0],
        [0, 0, 0, 0, -1],
        [0, 0, 0, 0,  0],
        [0, 0, 0, 0,  1],
        [0, -1, 0, 1, 0]
    ]

    local_vector = [
        lmb * (0),
        lmb * (-1),
        lmb * (0),
        lmb * (1),
        g
    ]

    return [local_matrix, local_vector, {0: p1.get_id(), 1: p2.get_id()}]


def constraint_7(segment1: Segment, segment2: Segment,
                 dx1: float, dy1: float,
                 dx2: float, dy2: float,
                 dx3: float, dy3: float,
                 dx4: float, dy4: float,
                 lambda_val: float,
                 angle_deg: float):
    p1, p2 = segment1.get_points()
    p3, p4 = segment2.get_points()

    x1, y1 = p1.get_x() + dx1, p1.get_y() + dy1
    x2, y2 = p2.get_x() + dx2, p2.get_y() + dy2
    x3, y3 = p3.get_x() + dx3, p3.get_y() + dy3
    x4, y4 = p4.get_x() + dx4, p4.get_y() + dy4


    u = x2 - x1
    v = y2 - y1
    p = x4 - x3
    q = y4 - y3

    eps_len = 1e-12
    B = u*u + v*v
    C = p*p + q*q
    if B < eps_len or C < eps_len:
        local_matrix = [[0.0]*9 for _ in range(9)]
        local_vector = [0.0]*9
        return [local_matrix, local_vector,
                {0: p1.get_id(), 1: p2.get_id(), 2: p3.get_id(), 3: p4.get_id()}]

    angle = math.radians(angle_deg)
    cs = math.cos(angle)

    M = [
        [-1, 0,  1, 0,  0, 0,  0, 0],  # u
        [ 0,-1,  0, 1,  0, 0,  0, 0],  # v
        [ 0, 0,  0, 0, -1, 0,  1, 0],  # p
        [ 0, 0,  0, 0,  0,-1,  0, 1],  # q
    ]


    if abs(cs) < 1e-8:
        A = u*p + v*q
        g_val = A


        g_uvpq = [p, q, u, v]


        Jd = [0.0]*8
        for col in range(8):
            s = 0.0
            for r in range(4):
                s += M[r][col] * g_uvpq[r]
            Jd[col] = s

        Hd = [[0.0]*8 for _ in range(8)]

    else:
        cs2 = cs * cs

        A = u*p + v*q

        g_val = A*A - cs2 * B * C

        gu = 2.0 * (A * p - cs2 * u * C)
        gv = 2.0 * (A * q - cs2 * v * C)
        gp = 2.0 * (A * u - cs2 * p * B)
        gq = 2.0 * (A * v - cs2 * q * B)
        g_uvpq = [gu, gv, gp, gq]

        H_uvpq = [[0.0]*4 for _ in range(4)]

        gradA = [p, q, u, v]
        for i in range(4):
            for j in range(4):
                H_uvpq[i][j] += 2.0 * gradA[i] * gradA[j]

        H_uvpq[0][2] += 2.0 * A
        H_uvpq[2][0] += 2.0 * A
        H_uvpq[1][3] += 2.0 * A
        H_uvpq[3][1] += 2.0 * A

        diag = [2.0*C, 2.0*C, 2.0*B, 2.0*B]
        for i in range(4):
            H_uvpq[i][i] -= cs2 * diag[i]

        H_uvpq[0][2] -= cs2 * (4.0*u*p)
        H_uvpq[0][3] -= cs2 * (4.0*u*q)
        H_uvpq[1][2] -= cs2 * (4.0*v*p)
        H_uvpq[1][3] -= cs2 * (4.0*v*q)

        H_uvpq[2][0] -= cs2 * (4.0*u*p)
        H_uvpq[3][0] -= cs2 * (4.0*u*q)
        H_uvpq[2][1] -= cs2 * (4.0*v*p)
        H_uvpq[3][1] -= cs2 * (4.0*v*q)

        Jd = [0.0]*8
        for col in range(8):
            s = 0.0
            for r in range(4):
                s += M[r][col] * g_uvpq[r]
            Jd[col] = s

        Hd = [[0.0]*8 for _ in range(8)]
        for i in range(8):
            for j in range(8):
                s = 0.0
                for a in range(4):
                    for b in range(4):
                        s += M[a][i] * H_uvpq[a][b] * M[b][j]
                Hd[i][j] = s

    lm = lambda_val

    local_matrix = [[0.0]*9 for _ in range(9)]
    for i in range(8):
        for j in range(8):
            local_matrix[i][j] = lm * Hd[i][j]
    for i in range(8):
        local_matrix[i][8] = Jd[i]
        local_matrix[8][i] = Jd[i]
    local_matrix[8][8] = 0.0

    local_vector = [0.0]*9
    for i in range(8):
        local_vector[i] = lm * Jd[i]
    local_vector[8] = g_val

    return [local_matrix, local_vector,
            {0: p1.get_id(), 1: p2.get_id(), 2: p3.get_id(), 3: p4.get_id()}]


def constraint_8(segment1: Segment, p3: Point,
                 delta_x1: float, delta_y1: float,
                 delta_x2: float, delta_y2: float,
                 delta_x3: float, delta_y3: float,
                 lmb: float):

    p1, p2 = segment1.get_points()

    x1, y1 = p1.get_x() + delta_x1, p1.get_y() + delta_y1
    x2, y2 = p2.get_x() + delta_x2, p2.get_y() + delta_y2
    x3, y3 = p3.get_x() + delta_x3, p3.get_y() + delta_y3

    u = x2 - x1
    v = y2 - y1
    w = x3 - x1
    t = y3 - y1

    g = w * v - t * u

    j1 = (t - v)
    j2 = (u - w)
    j3 = (-t)
    j4 = (w)
    j5 = (v)
    j6 = (-u)

    local_matrix = [
        [0, 0, 0, 0, 0, 0, j1],
        [0, 0, 0, 0, 0, 0, j2],
        [0, 0, 0, 0, 0, 0, j3],
        [0, 0, 0, 0, 0, 0, j4],
        [0, 0, 0, 0, 0, 0, j5],
        [0, 0, 0, 0, 0, 0, j6],
        [j1, j2, j3, j4, j5, j6, 0]
    ]

    local_vector = [
        lmb * j1,
        lmb * j2,
        lmb * j3,
        lmb * j4,
        lmb * j5,
        lmb * j6,
        g
    ]

    return [local_matrix, local_vector, {0: p1.get_id(), 1: p2.get_id(), 2: p3.get_id()}]


def constraint_9(point: Point, delta_x: float, delta_y: float,
                 lmb_x: float, lmb_y: float):
    local_matrix = [
        [0,   0,  1,  0],
        [0,   0,  0,  1],
        [1,   0,  0,  0],
        [0,   1,  0,  0]
    ]

    local_vector = [
        lmb_x,
        lmb_y,
        (point.get_x() + delta_x) - point.get_x(),  # хз сработает или нет
        (point.get_y() + delta_y) - point.get_y()
    ]

    return [local_matrix, local_vector, {0: point.get_id()}]


class Panel:
    constraints_dict = {1: constraint_1, 2: constraint_2, 3: constraint_3,
                        4: constraint_4, 5: constraint_5, 6: constraint_6,
                        7: constraint_7, 8: constraint_8, 9: constraint_9}

    constraints_lambdas = {1: 2, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 2}

    def __init__(self, panel_type: str, panel_id: int, req_points: int = 0,
                 req_segments: int = 0, constraint_type: int | None = None):
        self.id = panel_id
        self.panel_type = panel_type  # Constraint | CreatePoint | CreateSegment | DeleteSegment | DeleteConstraint
        self.req_points = req_points
        self.req_segments = req_segments
        self.constraint_type = constraint_type

    def get_req_points(self):
        return self.req_points

    def get_req_segments(self):
        return self.req_segments

    def get_id(self):
        return self.id

    def get_panel_type(self):
        return self.panel_type


def process_changes(matrix_size: int, constraints: List, points_order: Dict):
    eps = 1e-6
    number_points = len(points_order) * 2

    p = [100 for i in range(matrix_size)]
    initials = [0 for i in range(matrix_size)]

    iterations = 100
    counter = 0
    while np.linalg.norm(p) > eps and counter < iterations:
        counter += 1
        matrix = [[0. for i in range(matrix_size)] for j in range(matrix_size)]
        vector = [0 for i in range(matrix_size)]
        offset = 0
        for cnstr_ind in range(len(constraints)):
            current_offset = 0
            cnstr = constraints[cnstr_ind]
            # Ограничения на один объект (горизонтальность и вертикальность прямой, фиксация точки)
            if len(cnstr) == 2:
                if cnstr[1] == 9:
                    i1 = points_order[cnstr[0].get_id()] * 2
                    dx1, dy1 = initials[i1], initials[i1 + 1]
                    lm1 = initials[number_points + cnstr_ind + offset]
                    lm2 = initials[number_points + cnstr_ind + offset + 1]
                    current_offset += 1
                    ans, vec, order = Panel.constraints_dict[cnstr[1]](cnstr[0], dx1, dy1, lm1, lm2)
                else:
                    p1, p2 = cnstr[0].get_points()
                    i1 = points_order[p1.get_id()] * 2
                    i2 = points_order[p2.get_id()] * 2
                    dx1, dy1 = initials[i1], initials[i1 + 1]
                    dx2, dy2 = initials[i2], initials[i2 + 1]
                    lm = initials[number_points + cnstr_ind + offset]
                    ans, vec, order = Panel.constraints_dict[cnstr[1]](cnstr[0], dx1, dy1, dx2, dy2, lm)
            # Ограничения на пары объектов
            elif len(cnstr) == 3:
                if type(cnstr[0]).__name__ == "Segment":
                    p1, p2 = cnstr[0].get_points()
                    i1 = points_order[p1.get_id()] * 2
                    i2 = points_order[p2.get_id()] * 2
                    dx1, dy1 = initials[i1], initials[i1 + 1]
                    dx2, dy2 = initials[i2], initials[i2 + 1]
                    lm = initials[cnstr_ind + number_points + offset]
                    if type(cnstr[1]).__name__ == "Segment":
                        p3, p4 = cnstr[1].get_points()
                        i3 = points_order[p3.get_id()] * 2
                        i4 = points_order[p4.get_id()] * 2
                        dx3, dy3 = initials[i3], initials[i3 + 1]
                        dx4, dy4 = initials[i4], initials[i4 + 1]
                        ans, vec, order = Panel.constraints_dict[cnstr[2]](
                            cnstr[0], cnstr[1],
                            dx1, dy1,
                            dx2, dy2,
                            dx3, dy3,
                            dx4, dy4,
                            lm,
                        )
                    else:
                        p3 = cnstr[1]
                        i3 = points_order[p3.get_id()] * 2
                        dx3, dy3 = initials[i3], initials[i3 + 1]
                        ans, vec, order = Panel.constraints_dict[cnstr[2]](
                            cnstr[0], cnstr[1],
                            dx1, dy1,
                            dx2, dy2,
                            dx3, dy3,
                            lm
                        )
                else:
                    p1 = cnstr[0]
                    p2 = cnstr[1]
                    i1 = points_order[p1.get_id()] * 2
                    i2 = points_order[p2.get_id()] * 2
                    dx1, dy1 = initials[i1], initials[i1 + 1]
                    dx2, dy2 = initials[i2], initials[i2 + 1]
                    if cnstr[2] == 1:
                        lm1 = initials[cnstr_ind + number_points + offset]
                        lm2 = initials[cnstr_ind + number_points + offset + 1]
                        current_offset += 1
                        ans, vec, order = Panel.constraints_dict[cnstr[2]](
                            cnstr[0], cnstr[1],
                            dx1, dy1,
                            dx2, dy2,
                            lm1, lm2
                        )
                    else:
                        lm = initials[cnstr_ind + number_points + offset]
                        ans, vec, order = Panel.constraints_dict[cnstr[2]](
                            cnstr[0], cnstr[1],
                            dx1, dy1,
                            dx2, dy2,
                            lm
                        )
            else:  # len(cnstr) == 4 Пары объектов + значение (угол между прямыми или расстояние между точками)
                if cnstr[2] == 2:
                    p1 = cnstr[0]
                    p2 = cnstr[1]
                    i1 = points_order[p1.get_id()] * 2
                    i2 = points_order[p2.get_id()] * 2
                    dx1, dy1 = initials[i1], initials[i1 + 1]
                    dx2, dy2 = initials[i2], initials[i2 + 1]
                    lm = initials[cnstr_ind + number_points + offset]
                    ans, vec, order = Panel.constraints_dict[cnstr[2]](
                        cnstr[0], cnstr[1],
                        dx1, dy1,
                        dx2, dy2,
                        lm, cnstr[3]
                    )
                else:  # 9
                    p1, p2 = cnstr[0].get_points()
                    i1 = points_order[p1.get_id()] * 2
                    i2 = points_order[p2.get_id()] * 2
                    dx1, dy1 = initials[i1], initials[i1 + 1]
                    dx2, dy2 = initials[i2], initials[i2 + 1]
                    lm = initials[cnstr_ind + number_points + offset]
                    p3, p4 = cnstr[1].get_points()
                    i3 = points_order[p3.get_id()] * 2
                    i4 = points_order[p4.get_id()] * 2
                    dx3, dy3 = initials[i3], initials[i3 + 1]
                    dx4, dy4 = initials[i4], initials[i4 + 1]
                    ans, vec, order = Panel.constraints_dict[cnstr[2]](
                        cnstr[0], cnstr[1],
                        dx1, dy1,
                        dx2, dy2,
                        dx3, dy3,
                        dx4, dy4,
                        lm, cnstr[3]
                    )
            # ans - локальная матрица Якоби для обрабатываемого ограничения
            # vec - локальный вектор первых производных для обрабатываемого ограничения
            # order - порядок следования точек в локальной матрице
            for i in range(0, len(ans) - current_offset - 1, 2):
                real_i = points_order[order[i // 2]] * 2
                vector[real_i] += vec[i]
                vector[real_i + 1] += vec[i + 1]
                # Добавляем значения матрицы
                for j in range(0, len(ans[i]) - current_offset - 1, 2):
                    real_j = points_order[order[j // 2]] * 2
                    matrix[real_i][real_j] += ans[i][j]
                    matrix[real_i + 1][real_j] += ans[i + 1][j]
                    matrix[real_i][real_j + 1] += ans[i][j + 1]
                    matrix[real_i + 1][real_j + 1] += ans[i + 1][j + 1]
                # Добавляем лямбды (одну или две)
                for k in range(current_offset + 1):
                    real_j = cnstr_ind + number_points + offset + k
                    row = -(current_offset + 1 - k)
                    matrix[real_i][real_j] += ans[row][i]
                    matrix[real_i + 1][real_j] += ans[row][i + 1]
                    matrix[real_j][real_i] += ans[row][i]
                    matrix[real_j][real_i + 1] += ans[row][i + 1]
            if current_offset == 0:
                matrix[cnstr_ind + number_points + offset][cnstr_ind + number_points + offset] += ans[-1][-1]
                vector[cnstr_ind + number_points + offset] += vec[-1]
            else:
                matrix[cnstr_ind + number_points + offset + 1][cnstr_ind + number_points + offset + 1] += ans[-1][-1]
                vector[cnstr_ind + number_points + offset + 1] += vec[-1]
                matrix[cnstr_ind + number_points + offset][cnstr_ind + number_points + offset] += ans[-2][-2]
                vector[cnstr_ind + number_points + offset] += vec[-2]
            offset += current_offset
        for i in range(number_points):
            matrix[i][i] += 1
            vector[i] += initials[i]
        p = np.linalg.solve(np.array([np.array(i) for i in matrix]), - np.array(vector))
        initials = [initials[i] + p[i] for i in range(matrix_size)]
    return initials


class Solver:
    # Надо создавать и хранить тут список панелей, в которых заданы уравнения
    def __init__(self):
        self.points = dict()  # uuid : Point
        self.panels = dict()  # uuid : Panel
        self.segments = dict()  # uuid : Segment
        self.graph = dict()  # Список смежности с указанием параметра ограничений
        self.current_regime = Regime()
        # Добавление возможных ограничений и функций в качестве нажимаемых кнопок
        # Constraint | CreatePoint | CreateSegment | DeleteSegment | DeleteConstraint
        panel_constraint_1 = Panel("Constraint", 3, 2, 0, 1)
        panel_constraint_2 = Panel("Constraint", 5, 2, 0, 2)
        panel_constraint_3 = Panel("Constraint", 6, 0, 2, 3)
        panel_constraint_4 = Panel("Constraint", 7, 0, 2, 4)
        panel_constraint_5 = Panel("Constraint", 8, 0, 1, constraint_type=5)
        panel_constraint_6 = Panel("Constraint", 9, 0, 1, constraint_type=6)
        panel_constraint_7 = Panel("Constraint", 10, 0, 2, constraint_type=7)
        panel_constraint_8 = Panel("Constraint", 11, 1, 1, constraint_type=8)
        panel_constraint_9 = Panel("Constraint", 12, 1, constraint_type=9)

        self.panels[panel_constraint_1.get_id()] = panel_constraint_1
        self.panels[panel_constraint_2.get_id()] = panel_constraint_2
        self.panels[panel_constraint_3.get_id()] = panel_constraint_3
        self.panels[panel_constraint_4.get_id()] = panel_constraint_4
        self.panels[panel_constraint_5.get_id()] = panel_constraint_5
        self.panels[panel_constraint_6.get_id()] = panel_constraint_6
        self.panels[panel_constraint_7.get_id()] = panel_constraint_7
        self.panels[panel_constraint_8.get_id()] = panel_constraint_8
        self.panels[panel_constraint_9.get_id()] = panel_constraint_9
        panel_create_point = Panel("CreatePoint", 1)
        panel_create_segment = Panel("CreateSegment", 2, 2)
        panel_delete_constraint = Panel("Delete", 4)
        self.panels[panel_create_point.get_id()] = panel_create_point
        self.panels[panel_create_segment.get_id()] = panel_create_segment
        self.panels[panel_delete_constraint.get_id()] = panel_delete_constraint

    def handle_delete(self, triggered_obj: UUID | int | None):
        if triggered_obj is not None:
            if triggered_obj in self.points:
                triggered_obj = self.points[triggered_obj]
            elif triggered_obj in self.segments:
                triggered_obj = self.segments[triggered_obj]
        for vertex in self.graph[triggered_obj].keys():
            self.graph[vertex].pop(triggered_obj)
        self.graph.pop(triggered_obj)
        print("deleted")

    def handle_delete_constraint(self, triggered_obj1: UUID, triggered_obj2: UUID | None = None):
        if triggered_obj1 in self.points:
            triggered_obj1 = self.points[triggered_obj1]
        elif triggered_obj1 in self.segments:
            triggered_obj1 = self.segments[triggered_obj1]
        if triggered_obj2 is not None:
            if triggered_obj2 in self.points:
                triggered_obj2 = self.points[triggered_obj2]
            elif triggered_obj2 in self.segments:
                triggered_obj2 = self.segments[triggered_obj2]
            self.graph[triggered_obj2].pop(triggered_obj1)
        self.graph[triggered_obj1].pop(triggered_obj2)
        print("constr deleted")

    def handle_move(self, coordinates: List, triggered_obj: UUID):
        qt_message = dict()
        constraints_deq = deque()

        for key in self.segments.keys():
            if self.segments[key].get_points()[0].get_id() == triggered_obj \
                    or self.segments[key].get_points()[1].get_id() == triggered_obj:
                constraints_deq.append(self.segments[key])
        triggered_obj = self.points[triggered_obj]
        triggered_obj.new_coordinates(coordinates)
        constraints_deq.append(triggered_obj)
        points_order = dict()  # (point_uuid) : (point_row_number in jacobi matrix)
        i = 0
        n = 0
        seen_constraints = list()  # uuid или два uuid + номер ограничения
        constraints = list()
        while len(constraints_deq) > 0:
            current_obj = constraints_deq.pop()
            if type(current_obj).__name__ == "Segment":
                seg_point_1, seg_point_2 = current_obj.get_points()
                if not (seg_point_1.get_id() in points_order):
                    points_order[seg_point_1.get_id()] = i
                    constraints_deq.append(seg_point_1)
                    i += 1
                if not (seg_point_2.get_id() in points_order):
                    points_order[seg_point_2.get_id()] = i
                    constraints_deq.append(seg_point_2)
                    i += 1
            else:
                if not (current_obj.get_id() in points_order):
                    points_order[current_obj.get_id()] = i
                    i += 1
            for next_obj_key in self.graph[current_obj].keys():
                next_obj = self.graph[current_obj][next_obj_key]
                if next_obj_key is not None:
                    new_constraint = {current_obj.get_id(), next_obj_key.get_id(), next_obj[0]}
                    if not (new_constraint in seen_constraints):
                        seen_constraints.append(new_constraint)
                        if type(current_obj).__name__ == "Segment":  # Первыми всегда идут отрезки
                            constraints.append([current_obj, next_obj_key, next_obj[0]])
                        else:
                            constraints.append([next_obj_key, current_obj, next_obj[0]])
                        if len(next_obj) > 1:
                            constraints[-1].append(next_obj[1])
                        n += Panel.constraints_lambdas[next_obj[0]]
                        constraints_deq.append(next_obj_key)
                else:
                    new_constraint = {current_obj.get_id(), next_obj[0]}
                    if not (new_constraint in seen_constraints):
                        seen_constraints.append(new_constraint)
                        constraints.append([current_obj, next_obj[0]])
                        n += Panel.constraints_lambdas[next_obj[0]]
        n += i * 2
        deltas = process_changes(n, constraints, points_order)  # x1 y1 x2 y2 x3 y3
        qt_message["Move"] = []
        for key, value in points_order.items():
            self.points[key].update_coordinates(deltas[value * 2], deltas[value * 2 + 1])
            qt_message["Move"].append([key, self.points[key].get_x(), self.points[key].get_y()])
        return qt_message

    # Основная функция, которая запускает процесс обработки ввода
    # Текущий режим + ввод на этом шаге = что нужно делать (пересчитывать, перекрашивать или ничего)
    # Предполагается, что несвязанные напрямую с геометрией нажатия обрабатываются в основном цикле Qt
    # Должен возвращать новые цвета и новые координаты для каждого uuid, претерпевшего изменения
    def handle_input(self, coordinates: List, right_button_pressed: bool,
                     triggered_obj: UUID | int | None, left_button_hold: bool = False, value: float | None = None):
        qt_message = dict()
        if triggered_obj is not None:
            if triggered_obj in self.points:
                triggered_obj = self.points[triggered_obj]
            elif triggered_obj in self.segments:
                triggered_obj = self.segments[triggered_obj]
            else:
                triggered_obj = self.panels[triggered_obj]
        # triggered_obj отправляет None, если нажатие никого не задело, а если задело, то целиком объект
        instruction = self.current_regime.update_regime_state(coordinates, right_button_pressed, triggered_obj)
        # Словарь-инструкция содержит объекты! (а у них уже есть id, которые нужно отдать Qt с нужной инструкцией)
        # Либо отдать solver'у с нужными координатами и формулами, а потом уже Qt с инструкциями
        # "CreateElements", "Constraint", "ConstraintObj", "PaintSelection", "RemoveSelection"

        # Solver
        constraints_deq = deque()
        # constraints едят и сегменты и точки, потом раскладывают это в точки
        # по сути не может же быть больше одного ограничения у двух элементов
        if len(instruction["Constraint"]) > 0:
            constraint = instruction["Constraint"][0].constraint_type  # Число - номер ограничения
            vertex1 = instruction["ConstraintObj"][0]
            if len(instruction["ConstraintObj"]) > 1:
                vertex2 = instruction["ConstraintObj"][1]
                if not(vertex2 in self.graph):
                    self.graph[vertex2] = dict()
                if value is not None:
                    self.graph[vertex2][vertex1] = [constraint, value]
                else:
                    self.graph[vertex2][vertex1] = [constraint]
                constraints_deq.append(vertex2)
            else:
                vertex2 = None
            if not(vertex1 in self.graph):
                self.graph[vertex1] = dict()
            if value is not None:
                self.graph[vertex1][vertex2] = [constraint, value]
            else:
                self.graph[vertex1][vertex2] = [constraint]
            constraints_deq.append(vertex1)

            # У нас есть один или два объекта сейчас в deq
            # Если это сегмент, нам нужны условия и на него, и на его точки

            points_order = dict()  # (point_uuid) : (point_row_number in jacobi matrix)
            i = 0
            n = 0
            seen_constraints = list()  # uuid или два uuid + номер ограничения
            constraints = list()
            while len(constraints_deq) > 0:
                current_obj = constraints_deq.pop()
                if type(current_obj).__name__ == "Segment":
                    seg_point_1, seg_point_2 = current_obj.get_points()
                    if not(seg_point_1.get_id() in points_order):
                        points_order[seg_point_1.get_id()] = i
                        constraints_deq.append(seg_point_1)
                        i += 1
                    if not(seg_point_2.get_id() in points_order):
                        points_order[seg_point_2.get_id()] = i
                        constraints_deq.append(seg_point_2)
                        i += 1
                else:
                    if not(current_obj.get_id() in points_order):
                        points_order[current_obj.get_id()] = i
                        i += 1
                for next_obj_key in self.graph[current_obj].keys():
                    next_obj = self.graph[current_obj][next_obj_key]
                    if next_obj_key is not None:
                        new_constraint = {current_obj.get_id(), next_obj_key.get_id(), next_obj[0]}
                        if not(new_constraint in seen_constraints):
                            seen_constraints.append(new_constraint)
                            if type(current_obj).__name__ == "Segment":  # Первыми всегда идут отрезки
                                constraints.append([current_obj, next_obj_key, next_obj[0]])
                            else:
                                constraints.append([next_obj_key, current_obj, next_obj[0]])
                            if len(next_obj) > 1:
                                constraints[-1].append(next_obj[1])
                            n += Panel.constraints_lambdas[next_obj[0]]
                            constraints_deq.append(next_obj_key)
                    else:
                        new_constraint = {current_obj.get_id(), next_obj[0]}
                        if not(new_constraint in seen_constraints):
                            seen_constraints.append(new_constraint)
                            constraints.append([current_obj, next_obj[0]])
                            n += Panel.constraints_lambdas[next_obj[0]]
            n += i * 2
            deltas = process_changes(n, constraints, points_order)  # x1 y1 x2 y2 x3 y3
            qt_message["Move"] = []
            for key, value in points_order.items():
                self.points[key].update_coordinates(deltas[value * 2], deltas[value * 2 + 1])
                qt_message["Move"].append([key, self.points[key].get_x(), self.points[key].get_y()])

        if len(instruction["CreateElements"]) > 0:
            qt_message["CreatePoint"] = []
            qt_message["CreateSegments"] = []
            for elem in instruction["CreateElements"]:
                if type(elem).__name__ == "Point":
                    qt_message["CreatePoint"].append([elem.get_id(), elem.get_x(), elem.get_y()])
                    self.points[elem.get_id()] = elem
                    self.graph[elem] = dict()
                else:
                    qt_message["CreateSegments"].append([[i.get_id() for i in elem.get_points()], elem.get_id()])
                    self.segments[elem.get_id()] = elem
                    self.graph[elem] = dict()
        return qt_message


class Regime:
    def __init__(self, regime_type: str = "No regime"):
        self.regime_type = regime_type
        self.selected_points = list()  # Здесь внутри объекты!
        self.selected_segments = list()  # Здесь внутри объекты!
        self.selected_panel = None  # Здесь внутри объекты!

    def update_regime_state(self, coordinates: List, right_button_pressed: bool,
                            triggered_obj: Point | Segment | Panel | None) -> Dict:
        # triggered_obj - целиком объект, либо None, если никто не задет!
        # CreateElements - если действие привело к созданию нового элемента
        # Constraint, ConstraintObj - если действие привело к созданию нового ограничения
        return_dict = {"CreateElements": [], "Constraint": [], "ConstraintObj": [],
                       "PaintSelection": [], "RemoveSelection": []}  # Здесь внутри объекты!
        if right_button_pressed:
            self.free_selected_items(return_dict)
        if self.regime_type == "No regime":
            if triggered_obj is not None:
                return_dict["PaintSelection"].append(triggered_obj)
                if type(triggered_obj).__name__ == "Point":
                    self.selected_points.append(triggered_obj)
                    self.regime_type = "Select"
                elif type(triggered_obj).__name__ == "Segment":
                    self.selected_segments.append(triggered_obj)
                    self.regime_type = "Select"
                else:
                    self.selected_panel = triggered_obj
                    if triggered_obj.get_panel_type() == "CreateSegment":
                        self.regime_type = "CreateSegment"
                    elif triggered_obj.get_panel_type() == "CreatePoint":
                        self.regime_type = "CreatePoint"
                    elif triggered_obj.get_panel_type() == "Constraint":
                        self.regime_type = "Select"
        elif self.regime_type == "CreatePoint":
            if triggered_obj is None:  # если ставить новую точку слишком близко к старой точке, то не создаст
                new_point = Point(coordinates[0], coordinates[1])
                return_dict["CreateElements"].append(new_point)
                self.free_selected_items(return_dict)
        elif self.regime_type == "CreateSegment":
            if len(self.selected_points) > 0:  # не первая точка сегмента -> завершение режима (если это точка)
                if type(triggered_obj).__name__ == "Point":  # Граница отрезка - существующая точка
                    new_segment = Segment(self.selected_points[0], triggered_obj)
                    return_dict["CreateElements"].append(new_segment)
                    self.free_selected_items(return_dict)
                elif triggered_obj is None:  # Граница отрезка - новая точка
                    new_point = Point(coordinates[0], coordinates[1])
                    new_segment = Segment(self.selected_points[0], new_point)
                    return_dict["CreateElements"].append(new_segment)
                    return_dict["CreateElements"].append(new_point)
                    self.free_selected_items(return_dict)
            else:  # первая точка сегмента -> продолжение режима
                if type(triggered_obj).__name__ == "Point":
                    self.selected_points.append(triggered_obj)
                elif triggered_obj is None:
                    new_point = Point(coordinates[0], coordinates[1])
                    return_dict["CreateElements"].append(new_point)
                    self.selected_points.append(new_point)
        elif self.regime_type == "Select":  # В режиме выбора объектов (геометрия и кнопки)
            if triggered_obj is not None:
                if type(triggered_obj).__name__ == "Panel" and self.selected_panel is None:
                    if triggered_obj.get_req_points() == len(self.selected_points) and \
                            triggered_obj.get_req_segments() == len(self.selected_segments):
                        # Удовлетворено условие создания ограничения, надо создать ограничение
                        if triggered_obj.get_panel_type() == "CreateSegment":
                            return_dict["CreateElements"].append(Segment(self.selected_points[0],
                                                                         self.selected_points[1]))
                        else:
                            return_dict["Constraint"].append(triggered_obj)
                            for seg in self.selected_segments:
                                return_dict["ConstraintObj"].append(seg)
                            for pnt in self.selected_points:
                                return_dict["ConstraintObj"].append(pnt)
                        self.free_selected_items(return_dict)
                    elif triggered_obj.get_req_points() >= len(self.selected_points) and \
                            triggered_obj.get_req_segments() >= len(self.selected_segments):
                        # Ограничение ещё до конца не условлено, но в принципе возможно для текущего выбора
                        return_dict["PaintSelection"].append(triggered_obj)

                elif type(triggered_obj).__name__ == "Point":
                    if self.selected_panel is not None:  # Уже выбран тип ограничения
                        # Для выбранного ограничения можно добавить точку
                        if self.selected_panel.get_req_points() > len(self.selected_points) + 1:
                            self.selected_points.append(triggered_obj)
                            return_dict["PaintSelection"].append(triggered_obj)
                        # Добавление точки завершает ограничение
                        elif self.selected_panel.get_req_points() == len(self.selected_points) + 1:
                            # Удовлетворено условие создания ограничения, надо создать ограничение
                            return_dict["Constraint"].append(self.selected_panel)
                            return_dict["ConstraintObj"].append(triggered_obj)
                            for seg in self.selected_segments:
                                return_dict["ConstraintObj"].append(seg)
                            for pnt in self.selected_points:
                                return_dict["ConstraintObj"].append(pnt)
                            self.free_selected_items(return_dict)
                    else:  # Ограничение ещё не выбрано
                        # Выбор третьего объекта не имеет смысла для существующих ограничений в принципе
                        if len(self.selected_points) + len(self.selected_segments) < 2:
                            self.selected_points.append(triggered_obj)
                            return_dict["PaintSelection"].append(triggered_obj)

                elif type(triggered_obj).__name__ == "Segment":
                    if self.selected_panel is not None:  # Уже выбран тип ограничения
                        # Для выбранного ограничения можно добавить отрезок
                        if self.selected_panel.get_req_segments() > len(self.selected_segments) + 1:
                            self.selected_segments.append(triggered_obj)
                            return_dict["PaintSelection"].append(triggered_obj)
                        # Добавление точки завершает ограничение
                        elif self.selected_panel.get_req_segments() == len(self.selected_segments) + 1:
                            # Удовлетворено условие создания ограничения, надо создать ограничение
                            return_dict["Constraint"].append(self.selected_panel)
                            return_dict["ConstraintObj"].append(triggered_obj)
                            for seg in self.selected_segments:
                                return_dict["ConstraintObj"].append(seg)
                            for pnt in self.selected_points:
                                return_dict["ConstraintObj"].append(pnt)
                            self.free_selected_items(return_dict)
                    else:  # Ограничение ещё не выбрано
                        # Выбор третьего объекта не имеет смысла для существующих ограничений в принципе
                        if len(self.selected_points) + len(self.selected_segments) < 2:
                            self.selected_segments.append(triggered_obj)
                            return_dict["PaintSelection"].append(triggered_obj)

        return return_dict

    def free_selected_items(self, return_dict: Dict) -> None:
        # Если была выбрана панель, значит, что она была покрашена, а остальные в тени, надо возвращать
        # Если были выбраны точки и отрезки, значит, они были подсвечены, надо убирать подсветку
        # Информация о надобности перекраски должна отправляться в return dict
        if self.selected_panel is not None:
            return_dict["RemoveSelection"].append(self.selected_panel)
        for pnt in self.selected_points:
            return_dict["RemoveSelection"].append(pnt)
        for seg in self.selected_segments:
            return_dict["RemoveSelection"].append(seg)
        self.selected_segments = list()
        self.selected_points = list()
        self.selected_panel = None
        self.regime_type = "No regime"
