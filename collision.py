# encoding: utf-8
import random

from utils import Vec2d, dot, cross, component_mul, max_coords, min_coords, Color4


class AABB:
    def __init__(self, *points):
        self.bbl = None
        ":type: Vec2d|None"
        self.fur = None
        ":type: Vec2d|None"

        for point in points:
            self.add(point)

    def __bool__(self):
        return self.bbl is not None

    def add(self, point):
        """
        :type point: Vec2d|None
        """
        if point is None:
            return
        if not self:
            self.bbl = self.fur = point
            return
        self.bbl = min_coords(self.bbl, point)
        self.fur = max_coords(self.fur, point)

    def is_inside(self, point):
        """
        :type point: Vec2d
        """
        if not self:
            return False
        return self.bbl.x <= point.x <= self.fur.x and self.bbl.y <= point.y <= self.fur.y

    def union(self, aabb):
        """
        :type aabb: AABB
        :rtype : AABB
        """
        return AABB(self.bbl, self.fur, aabb.bbl, aabb.fur)

    def intersection(self, aabb):
        """
        :type aabb: AABB
        """
        result = AABB()
        if self and aabb:
            new_bbl = max_coords(self.bbl, aabb.bbl)
            new_fur = min_coords(self.fur, aabb.fur)
            if new_bbl.x <= new_fur.x and new_bbl.y <= new_fur.y:
                result.add(new_bbl)
                result.add(new_fur)
        return result

    def extend(self, value):
        """Увеличивает размер ббокса в value раз
        :type value: int|float
        """
        if not self:
            return self
        center = (self.bbl + self.fur) / 2
        bbl = center + (self.bbl - center)*value
        fur = center + (self.fur - center)*value
        return AABB(bbl, fur)


class BBoxNode:
    def __init__(self, obj=None):
        """
        :type obj: rectan.Rect|poly.Polygon|ball.Ball
        """
        self.obj = obj
        self.left = None
        ":type : BBoxNode"
        self.right = None
        ":type : BBoxNode"
        self.color = Color4.from_hsv(random.randint(0, 359), 50, 50)

    def bbox(self):
        """
        :rtype : AABB
        """
        if self.obj:
            return self.obj.bbox().extend(1.1)
        else:
            left_box = AABB() if self.left is None else self.left.bbox()
            right_box = AABB() if self.right is None else self.right.bbox()
            return left_box.union(right_box).extend(1.1)

    def render(self, screen):
        """
        :type screen: screen.Screen
        """
        bbox = self.bbox()
        x, y = bbox.bbl
        w, h = bbox.fur - bbox.bbl
        screen.draw_frame(self.color, x, y, w, h)
        if self.left:
            self.left.render(screen)
        if self.right:
            self.right.render(screen)


class BBoxTree:
    def __init__(self):
        self.root = None
        ":type : BBoxNode"

    def add(self, obj):
        if not self.root:
            self.root = BBoxNode(obj)
        else:
            def insert(node):
                """
                :type node: BBoxNode
                """
                to_left = random.choice([True, False])
                if to_left:
                    if node.left:
                        insert(node.left)
                    else:
                        node.left = BBoxNode(obj)
                        assert node.obj
                        node.right = BBoxNode(node.obj)
                        node.obj = None
                else:
                    if node.right:
                        insert(node.right)
                    else:
                        node.right = BBoxNode(obj)
                        assert node.obj
                        node.left = BBoxNode(node.obj)
                        node.obj = None
            insert(self.root)

    def clear(self):
        self.root = None

    def query_box(self, bbox):
        """
        :type bbox: AABB
        """
        return []

    def render(self, screen):
        """
        :type screen: screen.Screen
        """
        if self.root:
            self.root.render(screen)


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

        v1, v2 = obj1.speed, obj2.speed
        if self.vert:
            v1, v2 = Vec2d(v2.x, v1.y), Vec2d(v1.x, v2.y)
        if self.hor:
            v1, v2 = Vec2d(v1.x, v2.y), Vec2d(v2.x, v1.y)
        obj1.speed, obj2.speed = v1, v2


def collide_rect_with_rect(obj1, obj2):
    """
    :type obj1: rectan.Rect
    :type obj2: rectan.Rect
    :rtype: Manifold | None
    """
    half_width1, half_height1 = obj1.half_extents.data
    x1, y1 = obj1.pos.data
    left1 = x1 - half_width1
    right1 = x1 + half_width1
    up1 = y1 - half_height1
    down1 = y1 + half_height1

    half_width2, half_height2 = obj2.half_extents.data
    x2, y2 = obj2.pos.data
    left2 = x2 - half_width2
    right2 = x2 + half_width2
    up2 = y2 - half_height2
    down2 = y2 + half_height2

    intersect_x = False
    intersect_y = False
    if left1 <= right2 and left2 <= right1 or left2 <= right1 and left1 <= right2:
        intersect_x = True
    if up1 <= down2 and up2 <= down1 or up2 <= down1 and up1 <= down2:
        intersect_y = True
    if not intersect_x or not intersect_y:
        return None

    hor = True
    vert = True

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
