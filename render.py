# encoding: utf-8
import pygame

from screen import Screen
from utils import Vec2d


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
        self.color = (64, 255, 64)
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
