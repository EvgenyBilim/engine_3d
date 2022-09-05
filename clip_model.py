

class ClipModel:
    """
    Вспомогательный класс для усечения полигонов модели.

    При прохождении мимо длинных полигонов возникают артефакты, если один
    конец полигона находится в видимой области, а воторой позади фокусного
    расстояния камеры.

    Чтобы этого избежать, нужно усекать полигоны с образованием товых точек.
    (пока что работает криво)
    """

    def __init__(self, focus):
        self.focus = focus

    def clip(self, model):
        """Усекает полигоны модели, если это требуется. Если нет - возвращает исходную модель."""

        new_model = self._clip(model)
        if new_model:
            return new_model

        return model

    def _clip(self, model):
        """Усекает у модели полигоны, которые пересекают границу экрана."""

        if self.object_full_visible(model['points']):
            return None

        if self.object_full_invisible(model['points']):
            model['points'] = []
            model['lines'] = []
            model['faces'] = []
            return None

        new_model = {
            'points': model['points'],
            'lines': [],
            'faces': [],
        }

        for line in model['lines']:
            a = model['points'][line[0]]
            b = model['points'][line[1]]

            vis_a = self.point_is_visible(a)
            vis_b = self.point_is_visible(b)

            if vis_a and vis_b:
                new_model['lines'].append(line)
                continue

            if not vis_a or not vis_b:
                point_w = self.calc_w(a, b)
                point_index = len(model['points'])
                model['points'].append(point_w)

                if not vis_a:
                    line[0] = point_index

                if not vis_b:
                    line[1] = point_index

                new_model['lines'].append(line)

        return new_model

    def calc_w(self, a, b):
        """Вычисляет точку пересечения линии из точек ab с краем экрана."""

        x1, z1 = a[0], a[2]
        x2, z2 = b[0], b[2]
        x3, z3 = 0, self.focus  # self.focus * -1
        x4, z4 = max(abs(a[0]), abs(b[0])), max(abs(a[2]), abs(b[2]))

        try:
            px = ((x1 * z2 - z1 * x2) * (x3 - x4) - (x1 - x2) *
                  (x3 * z4 - z3 * x4)) / ((x1 - x2) * (z3 - z4) - (z1 - z2) * (x3 - x4))
        except ZeroDivisionError:
            px = 0  # вряд ли тут 0

        try:
            pz = ((x1 * z2 - z1 * x2) * (z3 - z4) - (z1 - z2) *
                  (x3 * z4 - z3 * x4)) / ((x1 - x2) * (z3 - z4) - (z1 - z2) * (x3 - x4))
        except ZeroDivisionError:
            pz = 0  # вряд ли тут 0

        try:
            py = a[1] - (a[0] - px) * (a[1] - b[1]) / (a[0] - b[0])
        except ZeroDivisionError:
            py = a[1]

        return [px, py, pz]

    def object_full_visible(self, points):
        """Проверяет, что объект полностью в видимой области экрана."""

        for point in points:
            if not self.point_is_visible(point):
                return False

        return True

    def object_full_invisible(self, points):
        """Проверяет, что объект полностью за пределами видимой области экрана."""

        for point in points:
            if self.point_is_visible(point):
                return False

        return True

    def point_is_visible(self, point):
        """Проверяет, что точка в видимой области экрана."""

        tang = 0.4142135623730950488016887242097  # вычисленное значение tan(22.5)
        delta_z = point[2] - self.focus
        tx = delta_z * tang

        if point[0] < -tx or point[0] > tx:
            return False

        return True
