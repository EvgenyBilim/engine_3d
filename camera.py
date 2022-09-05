

class Camera:
    """Класс камеры."""

    def __init__(self, position, angle):
        self.position = position
        self.angle = angle

    def rotate_x(self, angle):
        """Поворачивает камеру по оси x на угол angle."""
        self.angle[0] += angle

    def rotate_y(self, angle):
        """Поворачивает камеру по оси y на угол angle."""
        self.angle[1] += angle

    def rotate_z(self, angle):
        """Поворачивает камеру по оси y на угол angle."""
        self.angle[2] += angle

    def offset_x(self, offset):
        """Смещает камеру вдоль оси x на расстояние offset."""
        self.position[0] += offset

    def offset_y(self, offset):
        """Смещает камеру вдоль оси y на расстояние offset."""
        self.position[1] += offset

    def offset_z(self, offset):
        """Смещает камеру вдоль оси z на расстояние offset."""
        self.position[2] += offset
