# encoding: utf-8
from collision import AABB
from utils import Vec2d


class Rect:
    def __init__(self, pos, half_extents, color):
        """
        :param pos: Центр прямоугольнока
        :param half_extents: Тупл из половины высоты и половины длины
        :param color: Цвет прямоугольника
        """
        self.pos = pos
        self.half_extents = half_extents
        self.speed = Vec2d(200, 0)
        self.color = color

    def render(self, screen):
        """
        :type screen: screen.Screen
        """
        x, y = self.pos - self.half_extents
        w, h = 2*self.half_extents
        screen.draw_rect(self.color, x, y, w, h)
        screen.draw_frame(self.color*1.5, x, y, w, h)

    def bbox(self):
        return AABB(self.pos + self.half_extents, self.pos - self.half_extents)

    def set_pos(self, pos):
        """
        :type pos: Vec2d
        """
        self.pos = pos
