# encoding: utf-8
from utils import Vec2d


class Polygon:
    def __init__(self, points):
        self.points = points
        self.speed = Vec2d()

    def center(self):
        """
        :rtype: Vec2d
        """
        return sum(self.points, Vec2d())/len(self.points)

    def render(self, screen):
        """
        :type screen: screen.Screen
        """
        screen.draw_polyline((128, 255, 32), self.points, True)
        screen.draw_polyline((128, 255, 32), [self.center(), self.center()])
