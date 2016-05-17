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
        return self.x == other.x and self.y == other.y

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
        return apply2(self, other, lambda a, b: a+b)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        assert isinstance(other, numbers.Real), '%r must be a number' % other
        return self.apply(lambda t: t*other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self * (1/other)

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
    return apply2(v1, v2, min)


def max_coords(v1, v2):
    """Покомпонентный максимум
    :type v1: Vec2d
    :type v2: Vec2d
    """
    return apply2(v1, v2, max)


def unit_vector(angle):
    return Vec2d(math.sin(angle), math.cos(angle))


def random_vector():
    return unit_vector(random.random() * 2 * math.pi)
