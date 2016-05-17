# encoding: utf-8
from utils import Vec2d, dot, cross, component_mul


class Manifold:
    def collide(self):
        """меняет скорости у объектов, которые составляют манифолд"""


class CircleCircleManifold(Manifold):
    def __init__(self, circle1, circle2):
        """
        :type circle1: ball.Ball
        :type circle2: ball.Ball
        """
        self.circle1 = circle1
        self.circle2 = circle2

    def collide(self):
        obj1 = self.circle1
        obj2 = self.circle2
        if obj1.pos == obj2.pos:
            return
        t = (obj1.pos - obj2.pos).norm()
        n = Vec2d(t.y, -t.x)
        u1 = dot(obj1.speed, n) * n + dot(obj2.speed, t) * t
        u2 = dot(obj2.speed, n) * n + dot(obj1.speed, t) * t
        obj1.speed = u1
        obj2.speed = u2


def collide_circle_with_circle(obj1, obj2):
    """
    :type obj1: ball.Ball
    :type obj2: ball.Ball
    :rtype: Manifold|None
    """
    if (obj1.pos - obj2.pos).len() > obj2.r + obj1.r:
        return None
    if dot(obj1.pos - obj2.pos, obj1.speed - obj2.speed) < 0:
        return CircleCircleManifold(obj1, obj2)
    return None


class CircleBorderManifold(Manifold):
    def __init__(self, circle, hor, vert):
        """
        :type circle: ball.Ball
        :type hor: bool
        :type vert: bool
        """
        self.circle = circle
        self.hor = hor
        self.vert = vert

    def collide(self):
        obj = self.circle
        x_mul = -1 if self.hor else 1
        y_mul = -1 if self.vert else 1
        obj.speed = component_mul(obj.speed, Vec2d(x_mul, y_mul))


def collide_circle_with_border(obj, border):
    """
    :type obj: ball.Ball
    :param border: background.Blackground
    :rtype: Manifold|None
    """
    v = obj.speed
    r = obj.r
    left = obj.pos - Vec2d(r, 0)
    right = obj.pos + Vec2d(r, 0)
    up = obj.pos - Vec2d(0, r)
    down = obj.pos + Vec2d(0, r)

    screen_left_top = border.pos
    screen_right_bottom = border.pos + border.dims

    # столкновения с рамкой
    hor = False
    if left.x <= screen_left_top.x:
        if v.x <= 0:
            hor = True
    elif right.x >= screen_right_bottom.x:
        if v.x >= 0:
            hor = True

    vert = False
    if up.y <= screen_left_top.y:
        if v.y <= 0:
            vert = True
    elif down.y >= screen_right_bottom.y:
        if v.y >= 0:
            vert = True

    if hor or vert:
        return CircleBorderManifold(obj, hor, vert)
    return None


def collide_circle_with_poly(ball, poly):
    """
    :type ball: ball.Ball
    :type poly: poly.Polygon
    """
    for i in range(len(poly.points)):
        if dist_2_segment(ball.pos, poly.points[i - 1], poly.points[i]) <= ball.r:
            return True
    return False


def dist_2_segment(x0, x1, x2):
    """
    :type x0: Vec2d
    :type x1: Vec2d
    :type x2: Vec2d
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
    :type poly: poly.Polygon
    """
    for i in range(len(poly.points)):
        if cross(poly.points[i-1] - poly.points[i], point - poly.points[i]) >= 0:
            return False
    return True
