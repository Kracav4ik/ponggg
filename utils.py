# encoding: utf-8
import numbers

import math
import random


class Vec2d:
    """Двумерный вектор"""

    def __init__(self, x=0, y=0):
        """
        :type x: int|float
        :type y: int|float
        """
        self.data = (x, y)

    @property
    def x(self):
        return self.data[0]

    @property
    def y(self):
        return self.data[1]

    def __eq__(self, other):
        return self.data == other.data

    def __ne__(self, other):
        return not (self == other)

    def __iter__(self):
        return self.data.__iter__()

    def __len__(self):
        return self.data.__len__()

    def __getitem__(self, idx):
        return self.data[idx]

    def __pos__(self):
        return self

    def __neg__(self):
        return self.apply(lambda t: -t)

    def __add__(self, other):
        return Vec2d(self.data[0] + other.data[0], self.data[1] + other.data[1])

    def __sub__(self, other):
        return Vec2d(self.data[0] - other.data[0], self.data[1] - other.data[1])

    def __mul__(self, other):
        return Vec2d(self.data[0] * other, self.data[1] * other)

    def __rmul__(self, other):
        return Vec2d(self.data[0] * other, self.data[1] * other)

    def __truediv__(self, other):
        return Vec2d(self.data[0] / other, self.data[1] / other)

    def __abs__(self):
        return self.apply(abs)

    def len2(self):
        return dot(self, self)

    def len(self):
        return math.sqrt(self.len2())

    def norm(self):
        if self.x == 0 and self.y == 0:
            return self
        return self / self.len()

    def apply(self, fun):
        return Vec2d(fun(self.x), fun(self.y))

    def rot_cw(self):
        return Vec2d(self.y, -self.x)

    def rot_ccw(self):
        return Vec2d(-self.y, self.x)

    def __str__(self):
        return '(%.4f, %.4f)' % self.data

    def __repr__(self):
        return 'Vec2d(%s, %s)' % self.data

    @staticmethod
    def from_qt(qt_point):
        return Vec2d(qt_point.x(), qt_point.y())


def apply2(v1, v2, fun2):
    return Vec2d(fun2(v1.x, v2.x), fun2(v1.y, v2.y))


def component_mul(v1, v2):
    """Покомпонентное умножение
    :type v1: Vec2d
    :type v2: Vec2d
    """
    return apply2(v1, v2, lambda a, b: a*b)


def dot(v1, v2):
    """Скалярное произведение
    :type v1: Vec2d
    :type v2: Vec2d
    """
    return sum(component_mul(v1, v2))


def cross(v1, v2):
    """Векторное произведение
    :type v1: Vec2d
    :type v2: Vec2d
    """
    return dot(v1, v2.rot_cw())


def min_coords(v1, v2):
    """Покомпонентный минимум
    :type v1: Vec2d
    :type v2: Vec2d
    """
    return Vec2d(min(v1.data[0], v2.data[0]), min(v1.data[1], v2.data[1]))


def max_coords(v1, v2):
    """Покомпонентный максимум
    :type v1: Vec2d
    :type v2: Vec2d
    """
    return Vec2d(max(v1.data[0], v2.data[0]), max(v1.data[1], v2.data[1]))


def unit_vector(angle):
    return Vec2d(math.sin(angle), math.cos(angle))


def random_vector():
    return unit_vector(random.random() * 2 * math.pi)


def clamp(min_value, value, max_value):
    assert min_value <= max_value, 'min value %s must not be greater than max value %s' % (min_value, max_value)
    return max(min_value, min(value, max_value))


class Color4:
    def __init__(self, r, g, b, a=255):
        self.data = tuple(clamp(0, int(v), 255) for v in (r, g, b, a))

    @property
    def r(self):
        return self.data[0]

    @property
    def g(self):
        return self.data[1]

    @property
    def b(self):
        return self.data[2]

    @property
    def a(self):
        return self.data[3]

    def __eq__(self, other):
        return self.data == other.data

    def __ne__(self, other):
        return not (self == other)

    def __iter__(self):
        return self.data.__iter__()

    def __len__(self):
        return self.data.__len__()

    def __getitem__(self, idx):
        return self.data[idx]

    def __mul__(self, other):
        return Color4(self.data[0] * other, self.data[1] * other, self.data[2] * other, self.data[3] * other)

    def __rmul__(self, other):
        return Color4(self.data[0] * other, self.data[1] * other, self.data[2] * other, self.data[3] * other)

    def __truediv__(self, other):
        return Color4(self.data[0] / other, self.data[1] / other, self.data[2] / other, self.data[3] / other)

    def apply(self, fun):
        return Color4(*[fun(v) for v in self.data])

    def __str__(self):
        if self.a == 255:
            return '(%02X, %02X, %02X)' % self.data[:3]
        else:
            return '(%02X, %02X, %02X, %02X)' % self.data

    def __repr__(self):
        return 'Color4(%s, %s, %s, %s)' % self.data

    @staticmethod
    def from_hsv(h, s, v):
        """
        :type h: int|float
        :param h: Hue, 0..359
        :type s: int|float
        :param s: Saturation, 0..100
        :type v: int|float
        :param v: Value, 0..100
        """
        h = clamp(0, h, 360)
        if h == 360:
            h = 0
        s = clamp(0, s, 100)/100
        v = clamp(0, v, 100)/100

        v_min = (1 - s)*v
        delta = (v - v_min) * (h % 60) / 60
        if h < 60:
            r = v
            g = v_min + delta
            b = v_min
        elif h < 120:
            r = v - delta
            g = v
            b = v_min
        elif h < 180:
            r = v_min
            g = v
            b = v_min + delta
        elif h < 240:
            r = v_min
            g = v - delta
            b = v
        elif h < 300:
            r = v_min + delta
            g = v_min
            b = v
        else:
            r = v
            g = v_min
            b = v - delta

        return Color4(255*r, 255*g, 255*b)


WHITE = Color4(255, 255, 255)
BLACK = Color4(0, 0, 0)
