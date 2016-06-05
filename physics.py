# encoding: utf-8
from background import Blackground
from ball import Ball
from collision import collide_circle_with_border, collide_circle_with_poly, collide_circle_with_circle, \
    collide_rect_with_border, collide_rect_with_rect
from poly import Polygon
from rectan import Rect


class PhysicsEngine:
    def __init__(self, gravity, tree):
        """
        :type tree: collision.BBoxTree
        """
        self.gravity = gravity
        self.bodies = []
        self.manifolds = 0
        self.collide_tests = 0
        self.tree_tests = 0
        self.tree = tree

    def add_bodies(self, *bodies):
        self.bodies.extend(bodies)

    def process(self, elapsed):
        self.manifolds = 0
        self.collide_tests = 0
        self.tree_tests = 0
        for body in self.bodies:
            if isinstance(body, (Ball, Rect)):
                body.speed += 0.5 * self.gravity * elapsed
                body.set_pos(body.pos + body.speed * elapsed)
                body.speed += 0.5 * self.gravity * elapsed

        collisions_list = []
        collided = set()
        for i1 in range(len(self.bodies)):
            body1 = self.bodies[i1]
            box1 = body1.bbox()
            self.tree_tests += 1
            bodies2 = self.tree.query_box(box1)
            # bodies2 = self.bodies
            for body2 in bodies2:
                if body1 is body2 or (body2, body1) in collided:
                    continue
                self.collide_tests += 1
                manifold = self.__collide_bodies(body1, body2)
                if manifold:
                    collisions_list.append(manifold)
                collided.add((body1, body2))

        # for i1 in range(len(self.bodies)):
        #     for i2 in range(i1 + 1, len(self.bodies)):
        #         body1 = self.bodies[i1]
        #         body2 = self.bodies[i2]
        #         self.collide_tests += 1
        #         manifold = self.__collide_bodies(body1, body2)
        #         if manifold:
        #             collisions_list.append(manifold)

        m_types = {}
        for manifold in collisions_list:
            self.manifolds += 1
            manifold.collide()
            key = str(manifold.__class__)
            m_types[key] = m_types.get(key, 0) + 1
        print(m_types)

    @staticmethod
    def __collide_bodies(body1, body2):
        manifold = None
        if body1.__class__ != Ball and body1.__class__ != Rect:
            body1, body2 = body2, body1

        if body1.__class__ == Ball:
            if body2.__class__ == Blackground:
                manifold = collide_circle_with_border(body1, body2)
            elif body2.__class__ == Polygon:
                manifold = collide_circle_with_poly(body1, body2)
            elif body2.__class__ == Ball:
                manifold = collide_circle_with_circle(body1, body2)
            elif body2.__class__ == Rect:
                pass
        elif body1.__class__ == Rect:
            if body2.__class__ == Blackground:
                manifold = collide_rect_with_border(body1, body2)
            elif body2.__class__ == Rect:
                manifold = collide_rect_with_rect(body1, body2)
        return manifold
