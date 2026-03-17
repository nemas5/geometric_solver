
class Dot():
    def __init__(self, uuid, x, y):
        self.uuid = uuid
        self.x = x
        self.y = y

class Example():
    def __init__(self):
        pass
    def handle_input(self, coordinates, right_button_pressed: bool, 
                     triggered_obj, left_button_hold: bool = False):
        if triggered_obj == 1 :
            dots = []
            return ([1], dots)
        else:
            for i, coord in enumerate(coordinates):
                dot = Dot(uuid=i, x=coord[0], y=coord[1])
                dots.append(dot)
            return ([], dots)
    
    # return (triggered_obj, dots)