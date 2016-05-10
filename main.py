# encoding: utf-8

import pygame
import sys

from background import Blackground
from ball import Ball
from screen import Screen
from utils import Vec2d, random_vector

pygame.init()

WINDOW_SIZE = (1280, 720)  # размер окна в пикселах
WINDOW_BG_COLOR = (0, 0, 0)  # цвет окна
OFFSET = 50

window_surface = pygame.display.set_mode(WINDOW_SIZE)
screen = Screen(window_surface)
width, height = screen.get_size()
backyblacky = Blackground(OFFSET, OFFSET, width - 2 * OFFSET, height - 2 * OFFSET)
BALL_X = width/2
BALL_Y = height/2
BALL_SPEED = 350
magic_ball = Ball(BALL_X, BALL_Y, 50)
magic_ball.speed = BALL_SPEED * random_vector()


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
                magic_ball.pos = Vec2d(BALL_X, BALL_Y)
                magic_ball.speed = BALL_SPEED * random_vector()
                print('SPAAAAAAAAAAAAAAAAAAAAACE!!!11')


def process_game(elapsed):
    """Подвинуть игровые объекты
    """
    magic_ball.pos += magic_ball.speed*elapsed


def render():
    """Отрисовка игры на экране
    """
    main_screen = pygame.display.get_surface()
    main_screen.fill(WINDOW_BG_COLOR)

    backyblacky.render(screen)
    magic_ball.render(screen)

    pygame.display.flip()


MAX_FPS = 50
clock = pygame.time.Clock()
clock.tick()
# игровой цикл
while True:
    elapsed = clock.tick(MAX_FPS)

    handle_input()
    process_game(elapsed/1000)
    render()
