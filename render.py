from copy import deepcopy
from clip_model import ClipModel
from utils.common import sin, cos, angle_xy, angle_yz, angle_zx, distance_xy, distance_yz, distance_xz


class Render:
    """Класс для отрисовки трехмерных объектов на двухмерной плоскоти."""

    angle = 45
    focus = -725

    def __init__(self, objects, camera, canvas):
        self.objects = objects
        self.camera = camera
        self.canvas = canvas
        self.clip_model = ClipModel(self.focus)

    def render(self):
        """
        Итерируется по всем объектам и рисует их.
        Отрисовка происходит в несколько шагов:
            - Смещает мировые объекты (точнее, их локальную копию) относительно позиции камеры.
            - Поворачивает мировые объекты на угол камеры.
            - Проецирует точки на экран с учетом расстояния (это нужно для трехмерной
            перспективы - объекты, которые находятся дальше от камеры, выглядят меньше).
            - Усекает у моделей полигоны, которые пересекают границу экрана (пока работает криво).
        """

        self.canvas.delete('all')

        for obj in self.objects:
            model = deepcopy(obj.model)

            for i in model['points']:
                self.offset(i)
                self.rotate(i)
                self.screen(i)

            # Усечение полигонов не доделано и работает криво.
            model = self.clip_model.clip(model)
            self.draw(model)

    def offset(self, point):
        """Смещает мир относительно координат камеры."""

        point[0] -= self.camera.position[0]
        point[1] -= self.camera.position[1]
        point[2] -= self.camera.position[2]

    def rotate(self, point):
        """Поворачивает мир на угол камеры."""

        w = [0, 0, self.focus]

        # Поворачивает точку вокруг оси x
        angle_x = angle_yz(point, w) - self.camera.angle[0]
        wi_x = distance_yz(w, point)
        point[1] = (w[1] + wi_x * sin(angle_x))
        point[2] = (w[2] + wi_x * cos(angle_x))

        # Поворачивает точку вокруг оси y
        angle_y = angle_zx(point, w) - self.camera.angle[1]
        wi_y = distance_xz(w, point)
        point[0] = (w[0] + wi_y * sin(angle_y))
        point[2] = (w[2] + wi_y * cos(angle_y))

        # Поворачивает точку вокруг оси z
        angle_z = angle_xy(point, w) - self.camera.angle[2]
        wi_z = distance_xy(w, point)
        point[0] = (w[0] + wi_z * sin(angle_z))
        point[1] = (w[1] + wi_z * cos(angle_z))

    def screen(self, point):
        """Проецирует точку на плоскость экрана."""

        point[0] = (point[0] * self.focus / (point[2] - self.focus)) + 300  # pos_x
        point[1] = (point[1] * self.focus / (point[2] - self.focus)) + 200  # pos_y

    def draw(self, model):
        """Рисует объект в двухмерном пространстве."""

        for line in model['lines']:
            self.canvas.create_line(*model['points'][line[0]][:2], *model['points'][line[1]][:2])
