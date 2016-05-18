# encoding: utf-8
import random
import sys
import time

import pygame

from background import Blackground
from ball import Ball
from physics import PhysicsEngine
from poly import Polygon
from rectan import Rect
from render import RenderManager, DebugText, DebugCursor
from utils import Vec2d, random_vector, dot


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
                global balls_list
                balls_list = create_balls()
                print('SPAAAAAAAAAAAAAAAAAAAAACE!!!11')
        elif event.type == pygame.MOUSEMOTION:
            cursor.pos = Vec2d(*event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left mouse button
                cursor.visible = not cursor.visible
            elif event.button == 4:  # wheel up
                cursor.radius *= 1.1
            elif event.button == 5:  # wheel down
                cursor.radius /= 1.1


def process_game(elapsed):
    """Подвинуть игровые объекты
    """
    # двигаем объекты
    phys_engine.process(elapsed)

    recolor()


def recolor():
    sorted_balls = sorted(balls_list, key=lambda b: b.speed.len())
    min_spd = sorted_balls[0].speed.len()
    med_spd = sorted_balls[len(sorted_balls)//2].speed.len()
    max_spd = sorted_balls[-1].speed.len()
    for ball in sorted_balls:
        ball_spd = ball.speed.len()
        if ball_spd > med_spd:
            if med_spd == max_spd:
                color = (255, 255, 255)
            else:
                value = (ball_spd - med_spd) / (max_spd - med_spd)
                color = (255, 32, int(255 - value*223))
        else:
            if med_spd == min_spd:
                color = (255, 255, 255)
            else:
                value = (ball_spd - min_spd) / (med_spd - min_spd)
                color = (int(value*223 + 32), 32, 255)
        ball.trace_color = color


pygame.init()

WINDOW_SIZE = (1280, 720)  # размер окна в пикселах
WINDOW_BG_COLOR = (0, 0, 0)  # цвет окна
OFFSET = 50
GRAVITY = Vec2d(0, 500)

phys_engine = PhysicsEngine(GRAVITY)

render_manager = RenderManager(WINDOW_SIZE, WINDOW_BG_COLOR)

width, height = render_manager.get_size()
backyblacky = Blackground(OFFSET, OFFSET, width - 2 * OFFSET, height - 2 * OFFSET)
BALL_POS = Vec2d(width / 2, height / 2)
BALL_SPEED = 1350


def create_balls():
    magic_ball = Ball(BALL_POS, 50)
    magic_ball.speed = BALL_SPEED * random_vector()

    result = [magic_ball]
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            if x == 0 and y == 0:
                continue
            result.append(Ball(BALL_POS + Vec2d(150 * x, 150 * y), random.randint(10, 40)))

    return result

balls_list = create_balls()

Ep0 = 0
for ball in balls_list:
    Ep0 -= dot(GRAVITY, ball.pos)

megapoly = Polygon([Vec2d(300, 250), Vec2d(400, 300), Vec2d(350, 450), Vec2d(200, 400), Vec2d(200, 300)])

RECT_HALF_EXTENTS = Vec2d(20, 15)
rect_list = [Rect(Vec2d(150 + 2*i*RECT_HALF_EXTENTS.x, 70), RECT_HALF_EXTENTS) for i in range(10)]

MAX_FPS = 50
clock = pygame.time.Clock()
clock.tick()

debug_text = DebugText()

cursor = DebugCursor()

phys_engine.add_bodies(backyblacky)
phys_engine.add_bodies(*balls_list)
phys_engine.add_bodies(*rect_list)
phys_engine.add_bodies(megapoly)

render_manager.add_drawables(backyblacky)
render_manager.add_drawables(*balls_list)
render_manager.add_drawables(*rect_list)
render_manager.add_drawables(megapoly)
render_manager.add_drawables(debug_text)
render_manager.add_drawables(cursor)

# игровой цикл
while True:
    elapsed = clock.tick(MAX_FPS)

    frame_start = time.time()

    handle_input()
    process_game(elapsed / 1000)
    render_manager.render()

    frame_time = (time.time() - frame_start) * 1000
    debug_text.add_line('frame time %.2f ms' % frame_time)
    Ek = 0
    for ball in balls_list:
        Ek += ball.speed.len2() / 2
    debug_text.add_line('kinetic energy %.2f' % Ek)
    Ep = -Ep0
    for ball in balls_list:
        Ep -= dot(GRAVITY, ball.pos)
    debug_text.add_line('potential energy %.2f' % Ep)
    debug_text.add_line('full energy %.2f' % (Ek + Ep))
