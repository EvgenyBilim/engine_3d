from copy import deepcopy
from utils.common import sin, cos, angle_xy, angle_yz, angle_zx, distance_xy, distance_yz, distance_xz


class Object3d:
    """Трехмерный объект."""

    def __init__(self, model, position):
        self.position = position
        self.model = self.load(model)

    def load(self, model):
        """Устанавливает координаты объекта в мировой системе коордиат."""

        _model = deepcopy(model)

        for i in _model['points']:
            i[0] += self.position[0]
            i[1] += self.position[1]
            i[2] += self.position[2]

        return _model

    def rotate_x(self, delta, w=None):
        """Поворачивает объект вокруг оси x."""

        if w is None:
            w = self.position

        for i in self.model['points']:
            angle = angle_yz(i, w) - delta
            wi = distance_yz(w, i)

            i[1] = (w[1] + wi * sin(angle))
            i[2] = (w[2] + wi * cos(angle))

    def rotate_y(self, delta, w=None):

        """Поворачивает объект вокруг оси y."""
        if w is None:
            w = self.position

        for i in self.model['points']:
            angle = angle_zx(i, w) - delta
            wi = distance_xz(w, i)

            i[0] = (w[0] + wi * sin(angle))
            i[2] = (w[2] + wi * cos(angle))

    def rotate_z(self, delta, w=None):
        """Поворачивает объект вокруг оси z."""
        if w is None:
            w = self.position

        for i in self.model['points']:
            angle = angle_xy(i, w) - delta
            wi = distance_xy(w, i)

            i[0] = (w[0] + wi * sin(angle))
            i[1] = (w[1] + wi * cos(angle))
