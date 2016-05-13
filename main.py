# encoding: utf-8
import random

import pygame
import sys
import time

from background import Blackground
from ball import Ball, BALL_COLOR
from poly import Polygon
from screen import Screen
from utils import Vec2d, random_vector, dot

pygame.init()

WINDOW_SIZE = (1280, 720)  # размер окна в пикселах
WINDOW_BG_COLOR = (0, 0, 0)  # цвет окна
OFFSET = 50

window_surface = pygame.display.set_mode(WINDOW_SIZE)
screen = Screen(window_surface)
width, height = screen.get_size()
backyblacky = Blackground(OFFSET, OFFSET, width - 2 * OFFSET, height - 2 * OFFSET)
BALL_X = width / 2
BALL_Y = height / 2
BALL_SPEED = 1350
GRAVITY = Vec2d(0, 500)

megapoly = Polygon([Vec2d(300, 250), Vec2d(400, 300), Vec2d(350, 450), Vec2d(200, 400), Vec2d(200, 300)])


def create_balls():
    magic_ball = Ball(BALL_X, BALL_Y, 50)
    magic_ball.speed = BALL_SPEED * random_vector()

    result = [magic_ball]
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            if x == 0 and y == 0:
                continue
            result.append(Ball(BALL_X + 150 * x, BALL_Y + 150 * y, random.randint(10, 40)))

    return result


balls_list = create_balls()


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


def collide_circles(obj1, obj2):
    """
    :type obj1: Ball
    :type obj2: Ball
    """
    if obj1.pos == obj2.pos:
        return
    t = (obj1.pos - obj2.pos).norm()
    n = Vec2d(t.y, -t.x)
    u1 = dot(obj1.speed, n)*n + dot(obj2.speed, t)*t
    u2 = dot(obj2.speed, n)*n + dot(obj1.speed, t)*t
    obj1.speed = u1
    obj2.speed = u2


def circles_collide(obj1, obj2):
    """
    :type obj1: Ball
    :type obj2: Ball
    """
    if (obj1.pos - obj2.pos).len() > obj2.r + obj1.r:
        return False
    return dot(obj1.pos - obj2.pos, obj1.speed - obj2.speed) < 0


def try_collide_with_border(obj):
    v = obj.speed
    r = obj.r
    left = obj.pos - Vec2d(r, 0)
    right = obj.pos + Vec2d(r, 0)
    up = obj.pos - Vec2d(0, r)
    down = obj.pos + Vec2d(0, r)

    screen_left_top = backyblacky.pos
    screen_right_bottom = backyblacky.pos + backyblacky.dims

    # столкновения с рамкой
    if left.x <= screen_left_top.x:
        if v.x <= 0:
            obj.speed = Vec2d(-v.x, v.y)
    elif right.x >= screen_right_bottom.x:
        if v.x >= 0:
            obj.speed = Vec2d(-v.x, v.y)

    if up.y <= screen_left_top.y:
        if v.y <= 0:
            obj.speed = Vec2d(v.x, -v.y)
    elif down.y >= screen_right_bottom.y:
        if v.y >= 0:
            obj.speed = Vec2d(v.x, -v.y)


def collide_circle_with_poly(ball, poly):
    return (poly.center() - ball.pos).len() < 100


def process_game(elapsed):
    """Подвинуть игровые объекты
    """
    # двигаем объекты
    for ball in balls_list:
        ball.set_pos(ball.pos + ball.speed * elapsed)
        ball.speed += GRAVITY * elapsed

    # столкновения объектов со стенкой
    for ball in balls_list:
        try_collide_with_border(ball)

    for ball in balls_list:
        if collide_circle_with_poly(ball, megapoly):
            ball.color = (255, 255, 32)
        else:
            ball.color = BALL_COLOR

    # столкновения объектов друг с другом
    for i1 in range(len(balls_list)):
        for i2 in range(i1 + 1, len(balls_list)):
            ball1 = balls_list[i1]
            ball2 = balls_list[i2]
            if circles_collide(ball1, ball2):
                collide_circles(ball1, ball2)


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


def render():
    """Отрисовка игры на экране
    """
    main_screen = pygame.display.get_surface()
    main_screen.fill(WINDOW_BG_COLOR)

    backyblacky.render(screen)
    for ball in balls_list:
        ball.render(screen)
    megapoly.render(screen)

    frame_time = (time.time() - frame_start)*1000
    screen.draw_text('frame time %.2f ms' % frame_time, screen.get_font('Arial', 14), (64, 255, 64), 10, 10)

    pygame.display.flip()


MAX_FPS = 50
clock = pygame.time.Clock()
clock.tick()
# игровой цикл
while True:
    elapsed = clock.tick(MAX_FPS)

    frame_start = time.time()

    handle_input()
    process_game(elapsed / 1000)
    recolor()
    render()
