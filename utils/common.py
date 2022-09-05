import math


def distance_xy(a, b):
    return math.sqrt(abs(a[0] - b[0]) ** 2 + abs(a[1] - b[1]) ** 2)


def distance_xz(a, b):
    return math.sqrt(abs(a[0] - b[0]) ** 2 + abs(a[2] - b[2]) ** 2)


def distance_yz(a, b):
    return math.sqrt(abs(a[1] - b[1]) ** 2 + abs(a[2] - b[2]) ** 2)


def sin(a):
    return math.sin(math.radians(a))


def cos(a):
    return math.cos(math.radians(a))


def tan(a):
    return math.tan(math.radians(a))


def angle_xy(a, b):
    return math.degrees(math.atan2(a[0] - b[0], a[1] - b[1]))


def angle_zx(a, b):
    return math.degrees(math.atan2(a[0] - b[0], a[2] - b[2]))


def angle_yz(a, b):
    return math.degrees(math.atan2(a[1] - b[1], a[2] - b[2]))
