# encoding: utf-8

import pygame
import sys


pygame.init()

WINDOW_SIZE = (1280, 720)  # размер окна в пикселах
WINDOW_BG_COLOR = (0, 0, 0)  # цвет окна

window_surface = pygame.display.set_mode(WINDOW_SIZE)


def handle_input():
    """Обработка input от игрока
    """
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()


def process_game():
    """Подвинуть игровые объекты
    """


def render():
    """Отрисовка игры на экране
    """
    main_screen = pygame.display.get_surface()
    main_screen.fill(WINDOW_BG_COLOR)

    pygame.display.flip()


# игровой цикл
while True:
    handle_input()
    process_game()
    render()
