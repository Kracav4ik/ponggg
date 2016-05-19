# encoding: utf-8
import pygame

from screen import Screen
from utils import Vec2d, Color4


class RenderManager:
    def __init__(self, size, bg_color):
        self.bg_color = bg_color
        self.window_surface = pygame.display.set_mode(size)
        self.screen = Screen(self.window_surface)
        self.drawables = []

    def add_drawables(self, *drawables):
        self.drawables.extend(drawables)

    def get_size(self):
        return self.screen.get_size()

    def render(self):
        """Отрисовка игры на экране
        """
        self.window_surface.fill(self.bg_color)

        for obj in self.drawables:
            obj.render(self.screen)

        pygame.display.flip()


class DebugText:
    def __init__(self):
        self.lines = []
        self.pos = Vec2d(10, 5)
        self.step = Vec2d(0, 20)
        self.color = Color4(64, 255, 64)
        self.font = ('Arial', 14)

    def clear_lines(self):
        self.lines.clear()

    def add_line(self, line):
        self.lines.append(line)

    def render(self, screen):
        font = screen.get_font(*self.font)
        pos = self.pos
        for line in self.lines:
            screen.draw_text(line, font, self.color, *pos)
            pos += self.step
        self.clear_lines()


class DebugCursor:
    def __init__(self):
        self.pos = Vec2d()
        self.visible = False
        self.radius = 10

    def render(self, screen):
        """
        :type screen: screen.Screen
        """
        if not self.visible:
            return
        cursor_color = Color4(128, 128, 128)
        x, y = self.pos
        width, height = screen.get_size()
        draw_point_list_x = [Vec2d(x, 0), Vec2d(x, height)]
        draw_point_list_y = [Vec2d(0, y), Vec2d(width, y)]
        screen.draw_polyline(cursor_color, draw_point_list_x)
        screen.draw_polyline(cursor_color, draw_point_list_y)
        if self.radius > 0:
            from ball import circle_vertices
            screen.draw_polyline(cursor_color, circle_vertices(self.pos, self.radius, int(self.radius)), True)
