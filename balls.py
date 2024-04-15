import pymunk

class Balls:
    def __init__(self, space, static_body, radius, pos):
        self.space = space
        self.static_body = static_body
        self.radius = radius
        self.pos = pos
        self.shape = self.create_ball()

    def create_ball(self):
        body = pymunk.Body()
        body.position = self.pos
        shape = pymunk.Circle(body, self.radius)
        shape.mass = 5
        shape.elasticity = 0.8
        # use pivot joint to add friction
        pivot = pymunk.PivotJoint(body, self.static_body, (0, 0), (0, 0))
        pivot.max_bias = 0
        pivot.max_force = 1000
        self.space.add(body, shape, pivot)
        return shape