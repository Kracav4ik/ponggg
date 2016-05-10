# encoding: utf-8
from math import *

BALL_COLOR = (255, 128, 128)


def circle_vertices(x, y, r, n=32):
    result = []
    a = 2 * pi / n
    for i in range(n):
        result.append((sin(a * i) * r + x, cos(a * i) * r + y))
    return result


class Ball:
    def __init__(self, x, y, r):
        self.y = y
        self.x = x
        self.r = r

    def render(self, screen):
        """
        :type screen: screen.Screen
        """
        screen.draw_polygon(BALL_COLOR, circle_vertices(self.x, self.y, self.r))
