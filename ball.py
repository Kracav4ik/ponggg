# encoding: utf-8
from math import *

from utils import Vec2d, unit_vector

BALL_COLOR = (255, 128, 128)


def circle_vertices(pos, r, n=32):
    result = []
    a = 2 * pi / n
    for i in range(n):
        result.append(pos + r * unit_vector(a * i))
    return result


class Ball:
    def __init__(self, x, y, r):
        self.pos = Vec2d(x, y)
        self.r = r
        self.speed = Vec2d()

    def render(self, screen):
        """
        :type screen: screen.Screen
        """
        screen.draw_polygon(BALL_COLOR, circle_vertices(self.pos, self.r))
