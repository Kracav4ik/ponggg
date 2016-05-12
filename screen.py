# encoding: utf-8

import pygame


class Screen:
    """Экран, на котором можно рисовать
    surface - Объект класса pygame.Surface, на котором и происходит рисование
    """
    def __init__(self, surface):
        self.surface = surface
        self.fonts = {}

    def get_size(self):
        """Размер области, на которой мы рисуем
        """
        width, height = self.surface.get_size()
        return width, height

    def get_font(self, font_face, font_size):
        """Возвращаем кешированный шрифт
        font_face - название шрифта
        font_size - размер шрифта
        """
        font_key = (font_face, font_size)
        if font_key not in self.fonts:
            self.fonts[font_key] = pygame.font.SysFont(font_face, font_size)
        return self.fonts[font_key]

    def draw_rect(self, color, pix_x, pix_y, pix_w, pix_h):
        """Рисуем закрашенный прямоугольник
        color - Цвет, список из 3-х или 4-х чисел 0..255 (R, G, B) или (R, G, B, A), A == 0
        pix_x, pix_y - координаты левого верхнего угла в пикселях
        pix_w - Ширина в пикселях
        pix_h - Высота в пикселях
        """
        # noinspection PyArgumentList
        rect_surface = pygame.Surface((pix_w, pix_h), flags=pygame.SRCALPHA)
        rect_surface.fill(color)
        self.surface.blit(rect_surface, (pix_x, pix_y))

    def draw_polygon(self, color, points_list):
        """Рисуем закрашенный многоугольник
        color - Цвет, список из 3-х или 4-х чисел 0..255 (R, G, B) или (R, G, B, A), A == 0
        points_list - список вершин многоугольника
        """
        x_min, y_min = points_list[0]
        x_max, y_max = x_min, y_min
        for x, y in points_list:
            if x_max < x:
                x_max = x
            if x_min > x:
                x_min = x
            if y_max < y:
                y_max = y
            if y_min > y:
                y_min = y
        width = x_max - x_min + 1
        height = y_max - y_min + 1

        surface_points = []
        for x, y in points_list:
            surface_points.append([x - x_min, y - y_min])

        poly_surface = pygame.Surface((width, height), flags=pygame.SRCALPHA)
        pygame.draw.polygon(poly_surface, color, surface_points)
        self.surface.blit(poly_surface, (x_min, y_min))

    def draw_polyline(self, color, points_list, loop=False, thickness=1):
        """Рисуем ломаную линию
        color - Цвет, список из 3-х или 4-х чисел 0..255 (R, G, B) или (R, G, B, A), A == 0
        points_list - список вершин многоугольника
        thickness - Толщина рамки в пикселях (по умолчанию 1)
        loop - если True, рисует дополнительную линию от конца к началу
        """
        x_min, y_min = points_list[0]
        x_max, y_max = x_min, y_min
        for x, y in points_list:
            if x_max < x:
                x_max = x
            if x_min > x:
                x_min = x
            if y_max < y:
                y_max = y
            if y_min > y:
                y_min = y
        width = x_max - x_min + 1 + thickness*2
        height = y_max - y_min + 1 + thickness*2

        surface_points = []
        for x, y in points_list:
            surface_points.append([x - x_min + thickness, y - y_min + thickness])

        poly_surface = pygame.Surface((width, height), flags=pygame.SRCALPHA)
        pygame.draw.lines(poly_surface, color, loop, surface_points, thickness)
        self.surface.blit(poly_surface, (x_min - thickness, y_min - thickness))

    def draw_text(self, text, font, color, pix_x, pix_y, pix_w, pix_h):
        """Рисуем текст так, чтобы центр нарисованного текста был в центре заданного прямоугольника
        text - Текст
        font - Шрифт
        color - Цвет, список из 3-х чисел 0..255
        pix_x, pix_y - координаты левого верхнего угла прямоугольника в пикселях
        pix_w - Ширина прямоугольника в пикселях
        pix_h - Высота прямоугольника в пикселях
        """
        text_surface = font.render(text, False, color)
        text_x = pix_x + pix_w // 2 - text_surface.get_width() // 2
        text_y = pix_y + pix_h // 2 - text_surface.get_height() // 2
        self.surface.blit(text_surface, (text_x, text_y))

    def draw_frame(self, color, pix_x, pix_y, pix_w, pix_h, thickness=1):
        """Рисуем прямоугольную рамку
        color - Цвет, список из 3-х чисел 0..255
        pix_x, pix_y - координаты левого верхнего угла в пикселях
        pix_w - Ширина в пикселях
        pix_h - Высота в пикселях
        thickness - Толщина рамки в пикселях (по умолчанию 1)
        """
        pygame.draw.rect(self.surface, color, (pix_x, pix_y, pix_w, pix_h), thickness)

    def draw_texture(self, texture, pix_x, pix_y, pix_w, pix_h):
        """Рисуем текстуру так, чтобы ее центр был в центре заданного прямоугольника
        texture - текстура в виде объекта pygame.Surface
        pix_x, pix_y - координаты левого верхнего угла прямоугольника в пикселях
        pix_w - Ширина прямоугольника в пикселях
        pix_h - Высота прямоугольника в пикселях
        """
        tex_x = pix_x + pix_w // 2 - texture.get_width() // 2
        tex_y = pix_y + pix_h // 2 - texture.get_height() // 2
        self.surface.blit(texture, (tex_x, tex_y))
