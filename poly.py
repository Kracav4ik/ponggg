# encoding: utf-8
from utils import Vec2d


DEFAULT_COLOR = (128, 255, 32)


class Polygon:
    def __init__(self, points):
        self.points = points
        self.speed = Vec2d()
        self.colors = {}

    def center(self):
        """
        :rtype: Vec2d
        """
        return sum(self.points, Vec2d())/len(self.points)

    def clear_colors(self):
        self.colors.clear()

    def set_color(self, segment_idx, color):
        self.colors[segment_idx] = color

    def get_segment(self, i):
        return [self.points[i-1], self.points[i]]

    def render(self, screen):
        """
        :type screen: screen.Screen
        """
        if self.colors:
            for i in range(len(self.points)):
                screen.draw_polyline(self.colors.get(i, DEFAULT_COLOR), self.get_segment(i), True)
        else:
            screen.draw_polyline(DEFAULT_COLOR, self.points, True)
        screen.draw_polyline(DEFAULT_COLOR, [self.center(), self.center()])
