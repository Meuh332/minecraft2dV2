class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return self.x, self.y

    @property
    def x(self):
        return self._x * -1

    @property
    def y(self):
        return self._y * -1

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value
