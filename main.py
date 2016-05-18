# encoding: utf-8
import random
import sys
import time

import pygame

from background import Blackground
from ball import Ball, BALL_COLOR, circle_vertices
from collision import collide_circle_with_circle, collide_circle_with_border, collide_circle_with_poly, \
    point_inside_poly, dist_2_segment
from poly import Polygon
from screen import Screen
from utils import Vec2d, random_vector, dot


class Cursor:
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
        cursor_color = (128, 128, 128)
        x, y = self.pos
        draw_point_list_x = [Vec2d(x, 0), Vec2d(x, height)]
        draw_point_list_y = [Vec2d(0, y), Vec2d(width, y)]
        screen.draw_polyline(cursor_color, draw_point_list_x)
        screen.draw_polyline(cursor_color, draw_point_list_y)
        if self.radius > 0:
            screen.draw_polyline(cursor_color, circle_vertices(self.pos, self.radius, int(self.radius)), True)


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

cursor = Cursor()


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
        elif event.type == pygame.MOUSEMOTION:
            cursor.pos = Vec2d(*event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left mouse button
                cursor.visible = not cursor.visible
            elif event.button == 4:  # wheel up
                cursor.radius *= 1.1
            elif event.button == 5:  # wheel down
                cursor.radius /= 1.1


debug_lines = []


def process_game(elapsed):
    """Подвинуть игровые объекты
    """
    # двигаем объекты
    for ball in balls_list:
        ball.speed += 0.5 * GRAVITY * elapsed
        ball.set_pos(ball.pos + ball.speed * elapsed)
        ball.speed += 0.5 * GRAVITY * elapsed

    collisions_list = []

    # столкновения объектов со стенкой
    for ball in balls_list:
        manifold = collide_circle_with_border(ball, backyblacky)
        if manifold:
            collisions_list.append(manifold)

    for ball in balls_list:
        if point_inside_poly(ball.pos, megapoly):
            ball.color = (32, 128, 255)
        elif collide_circle_with_poly(ball, megapoly):
            ball.color = (255, 255, 32)
        else:
            ball.color = BALL_COLOR

    megapoly.clear_colors()
    debug_lines.clear()
    for i in range(len(megapoly.points)):
        p1 = megapoly.points[i - 2]
        p2 = megapoly.points[i - 1]
        p3 = megapoly.points[i]
        bisect = (p2 - p1).norm() + (p2 - p3).norm()
        if dist_2_segment(cursor.pos, megapoly.points[i - 1], megapoly.points[i]) <= cursor.radius:
            megapoly.set_color(i, (255, 128, 32))
        debug_lines.append([(255, 32, 32), [p2, p2 + 30*bisect.norm()]])

    # столкновения объектов друг с другом
    for i1 in range(len(balls_list)):
        for i2 in range(i1 + 1, len(balls_list)):
            ball1 = balls_list[i1]
            ball2 = balls_list[i2]
            manifold = collide_circle_with_circle(ball1, ball2)
            if manifold:
                collisions_list.append(manifold)

    for manifold in collisions_list:
        manifold.collide()


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


Ep0 = 0
for ball in balls_list:
    Ep0 -= dot(GRAVITY, ball.pos)


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
    screen.draw_text('frame time %.2f ms' % frame_time, screen.get_font('Arial', 14), (64, 255, 64), 10, 5)

    Ek = 0
    for ball in balls_list:
        Ek += ball.speed.len2()/2
    screen.draw_text('kinetic energy %.2f' % Ek, screen.get_font('Arial', 14), (64, 255, 64), 10, 25)
    Ep = -Ep0
    for ball in balls_list:
        Ep -= dot(GRAVITY, ball.pos)
    screen.draw_text('potential energy %.2f' % Ep, screen.get_font('Arial', 14), (64, 255, 64), 10, 45)
    screen.draw_text('full energy %.2f' % (Ek + Ep), screen.get_font('Arial', 14), (64, 255, 64), 10, 65)
    for color, lines in debug_lines:
        screen.draw_arrow(color, *lines)

    cursor.render(screen)

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
