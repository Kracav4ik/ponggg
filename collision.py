# encoding: utf-8
from utils import Vec2d, dot, cross


def do_collide_circles(obj1, obj2):
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


def try_collide_with_border(obj, border):
    v = obj.speed
    r = obj.r
    left = obj.pos - Vec2d(r, 0)
    right = obj.pos + Vec2d(r, 0)
    up = obj.pos - Vec2d(0, r)
    down = obj.pos + Vec2d(0, r)

    screen_left_top = border.pos
    screen_right_bottom = border.pos + border.dims

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
    """
    :type ball: Ball
    :type poly: Polygon
    """
    for i in range(len(poly.points)):
        if dist_2_segment(ball.pos, poly.points[i - 1], poly.points[i]) <= ball.r:
            return True
    return False


def dist_2_segment(x0, x1, x2):
    """
    :type x0:Vec2d
    :type x1:Vec2d
    :type x2:Vec2d
    """
    if dot(x1-x2, x0-x2) <= 0:
        return (x0 - x2).len()
    elif dot(x2 - x1, x0 - x1) <= 0:
        return (x0 - x1).len()
    else:
        return abs(cross(x0 - x1, x2 - x1) / (x2 - x1).len())


def point_inside_poly(point, poly):
    """
    :type point: Vec2d
    :type poly: Polygon
    """
    for i in range(len(poly.points)):
        if cross(poly.points[i-1] - poly.points[i], point - poly.points[i]) >= 0:
            return False
    return True
