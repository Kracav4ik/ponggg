# encoding: utf-8

import pygame
import sys

from background import Blackground
from ball import Ball
from screen import Screen

pygame.init()

WINDOW_SIZE = (1280, 720)  # размер окна в пикселах
WINDOW_BG_COLOR = (0, 0, 0)  # цвет окна

window_surface = pygame.display.set_mode(WINDOW_SIZE)
screen = Screen(window_surface)
backyblacky = Blackground()
magic_ball = Ball(250, 150, 50)


def handle_input():
    """Обработка input от игрока
    """
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # клавиатура
            print('event', event)
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_SPACE:
                print('SPAAAAAAAAAAAAAAAAAAAAACE!!!11')


def process_game():
    """Подвинуть игровые объекты
    """


def render():
    """Отрисовка игры на экране
    """
    main_screen = pygame.display.get_surface()
    main_screen.fill(WINDOW_BG_COLOR)

    backyblacky.render(screen)
    magic_ball.render(screen)

    pygame.display.flip()


# игровой цикл
while True:
    handle_input()
    process_game()
    render()
