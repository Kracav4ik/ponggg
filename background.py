# encoding: utf-8
from utils import Vec2d, WHITE


class Blackground:
    def __init__(self, x, y, width, height):
        """
        x, y - Левый верхний угол рамки
        width, height - Ширина и высота рамки
        """
        self.pos = Vec2d(x, y)
        self.dims = Vec2d(width, height)

    def render(self, screen):
        """
        :type screen: screen.Screen
        """
        frame_thickness = 2
        frame_color = WHITE

        screen.draw_frame(frame_color, self.pos.x, self.pos.y, self.dims.x, self.dims.y, frame_thickness)
