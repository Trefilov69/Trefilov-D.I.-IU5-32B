from lab_python_oop.rectangle import Rectangle


class Square(Rectangle):

    FIGURE_TYPE = "Квадрат"

    def __init__(self, side, color):
        super().__init__(side, side, color)
        self.side = side

    def __repr__(self):
        return "{}: сторона = {}, цвет = {}, площадь = {}".format(
            self.get_figure_type(),
            self.side,
            self.fc.color,
            self.square()
        )
