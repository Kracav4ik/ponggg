# encoding: utf-8
import pygame

from screen import Screen


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
