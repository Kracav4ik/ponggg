# encoding: utf-8
from background import Blackground
from ball import Ball
from collision import collide_circle_with_border, collide_circle_with_poly, collide_circle_with_circle
from poly import Polygon
from rectan import Rect


class PhysicsEngine:
    def __init__(self, gravity):
        self.gravity = gravity
        self.bodies = []

    def add_bodies(self, *bodies):
        self.bodies.extend(bodies)

    def process(self, elapsed):
        for body in self.bodies:
            if isinstance(body, (Ball, Rect)):
                body.speed += 0.5 * self.gravity * elapsed
                body.set_pos(body.pos + body.speed * elapsed)
                body.speed += 0.5 * self.gravity * elapsed

        collisions_list = []
        for i1 in range(len(self.bodies)):
            for i2 in range(i1 + 1, len(self.bodies)):
                body1 = self.bodies[i1]
                body2 = self.bodies[i2]
                manifold = self.__collide_bodies(body1, body2)
                if manifold:
                    collisions_list.append(manifold)

        for manifold in collisions_list:
            manifold.collide()

    @staticmethod
    def __collide_bodies(body1, body2):
        manifold = None
        if not isinstance(body1, Ball):
            body1, body2 = body2, body1

        if isinstance(body1, Ball):
            if isinstance(body2, Blackground):
                manifold = collide_circle_with_border(body1, body2)
            elif isinstance(body2, Polygon):
                manifold = collide_circle_with_poly(body1, body2)
            elif isinstance(body2, Ball):
                manifold = collide_circle_with_circle(body1, body2)
        return manifold
