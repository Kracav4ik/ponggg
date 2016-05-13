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
        self.pos_list = [self.pos]
        self.trace_color = (255, 255, 255)

    def render(self, screen):
        """
        :type screen: screen.Screen
        """
        screen.draw_polyline(BALL_COLOR, circle_vertices(self.pos, self.r), True, 2)
        screen.draw_polyline(self.trace_color, self.pos_list)

    def set_pos(self, pos):
        """
        :type pos: Vec2d
        """
        self.pos = pos
        self.pos_list.append(pos.apply(int))
        if len(self.pos_list) > 20:
            self.pos_list = self.pos_list[1:]
