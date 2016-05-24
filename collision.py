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


class RectBorderManifold(Manifold):
    def __init__(self, rect, hor, vert):
        """
        :type rect: rectan.Rect
        :type hor: bool
        :type vert: bool
        """
        self.rect = rect
        self.hor = hor
        self.vert = vert

    def collide(self):
        obj = self.rect
        x_mul = -1 if self.hor else 1
        y_mul = -1 if self.vert else 1
        obj.speed = component_mul(obj.speed, Vec2d(x_mul, y_mul))


def collide_rect_with_border(obj, border):
    """
    :type obj: rectan.Rect
    :type border: background.Blackground
    :rtype: Manifold | None
    """
    v = obj.speed
    half_width, half_height = obj.half_extents
    left = obj.pos - Vec2d(half_width, 0)
    right = obj.pos + Vec2d(half_width, 0)
    up = obj.pos - Vec2d(0, half_height)
    down = obj.pos + Vec2d(0, half_height)

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
        return RectBorderManifold(obj, hor, vert)
    return None


class CirclePolyManifold(Manifold):
    def __init__(self, circle, poly, normal):
        """
        :type circle: ball.Ball
        :type poly: poly.Polygon
        :type normal: Vec2d
        """
        self.circle = circle
        self.poly = poly
        self.normal = normal

    def collide(self):
        self.circle.speed -= 2 * self.normal * dot(self.circle.speed, self.normal)


def collide_circle_with_poly(ball, poly):
    """
    :type ball: ball.Ball
    :type poly: poly.Polygon
    :rtype: Manifold|None
    """
    X1, X2, MID = 1, 2, 3
    to_check = []
    for i in range(len(poly.points)):
        x0 = ball.pos
        x1 = poly.points[i - 1]
        x2 = poly.points[i]
        if dot(x1 - x2, x0 - x2) <= 0:
            check = X2
            x = (x0 - x2).len()
        elif dot(x2 - x1, x0 - x1) <= 0:
            check = X1
            x = (x0 - x1).len()
        else:
            check = MID
            x = abs(cross(x0 - x1, x2 - x1) / (x2 - x1).len())
        if x <= ball.r:
            to_check.append([x, i, check])
    if not to_check:
        return None

    to_check.sort()
    min_dist, min_i, min_check = to_check[0]
    if min_check == MID:
        p1 = poly.points[min_i - 1]
        p2 = poly.points[min_i]
        normal = (p2 - p1).norm().rot_cw()
    else:
        if min_check == X2:
            collided_i = min_i
        else:
            collided_i = min_i - 1
        p1 = poly.points[collided_i - 1]
        p2 = poly.points[collided_i]
        p3 = poly.points[collided_i + 1 - len(poly.points)]
        normal = ((p2 - p1).norm() + (p2 - p3).norm()).norm()

    if dot(normal, ball.speed) >= 0:
        return None

    return CirclePolyManifold(ball, poly, normal)


class RectRectManifold(Manifold):
    def __init__(self, rect1, rect2, hor, vert):
        """
        :type rect1: rectan.Rect
        :type rect2: rectan.Rect
        :type hor: bool
        :type vert: bool
        """
        self.rect1 = rect1
        self.rect2 = rect2
        self.hor = hor
        self.vert = vert

    def collide(self):
        obj1 = self.rect1
        obj2 = self.rect2
        v1 = obj1.speed
        v2 = obj2.speed

        if self.vert:
            obj1.speed = Vec2d(v2.x, v1.y)
            obj2.speed = Vec2d(v1.x, v2.y)
        if self.hor:
            obj1.speed = Vec2d(v1.x, v2.y)
            obj2.speed = Vec2d(v2.x, v1.y)


def collide_rect_with_rect(obj1, obj2):
    """
    :type obj1: rectan.Rect
    :type obj2: rectan.Rect
    :rtype: Manifold | None
    """
    half_width1, half_height1 = obj1.half_extents
    left1 = obj1.pos - Vec2d(half_width1, 0)
    right1 = obj1.pos + Vec2d(half_width1, 0)
    up1 = obj1.pos - Vec2d(0, half_height1)
    down1 = obj1.pos + Vec2d(0, half_height1)

    half_width2, half_height2 = obj2.half_extents
    left2 = obj2.pos - Vec2d(half_width2, 0)
    right2 = obj2.pos + Vec2d(half_width2, 0)
    up2 = obj2.pos - Vec2d(0, half_height2)
    down2 = obj2.pos + Vec2d(0, half_height2)

    hor = False
    vert = False
    if left1.x - right2.x <= 0 < right1.x - left2.x or left2.x - right1.x <= 0 < right2.x - left1.x:
        vert = True
    if up1.y - down2.y <= 0 < up1.y - down2.y or up2.y - down1.y <= 0 < up2.y - down1.y:
        hor = True
    if hor or vert:
        return RectRectManifold(obj1, obj2, hor, vert)
    return None


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


def sign(integer):
    if integer < 0:
        return -1
    elif integer > 0:
        return 1
    else:
        return 0


def line_intersects_segment(line_p1, line_p2, segment_p1, segment_p2):
    line = line_p2 - line_p1
    side1 = sign(cross(line, segment_p1))
    side2 = sign(cross(line, segment_p2))
    if side1 == side2 == 1 or side1 == side2 == -1:
        return False
    return True
