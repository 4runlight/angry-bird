import pymunk as pm
from pymunk import Vec2d    #平面向量类


class Bird():
    def __init__(self, distance, angle, x, y, space):
        self.col=False
        self.life = 20
        mass = 5
        radius = 12
        #惯性
        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        body = pm.Body(mass, inertia)
        body.position = x, y
        #撞击力量
        power = distance * 53
        impulse = power * Vec2d(1, 0)
        #小鸟旋转
        angle = -angle
        body.apply_impulse_at_local_point(impulse.rotated(angle))
        
        shape = pm.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 1
        shape.collision_type = 0
        space.add(body, shape)
        
        self.body = body
        self.shape = shape


class Pig():
    def __init__(self, x, y, space):
        self.life = 20
        mass = 5
        radius = 14
        #惯性
        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        body = pm.Body(mass, inertia)
        body.position = x, y
        
        shape = pm.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 1
        shape.collision_type = 1
        space.add(body, shape)
        
        self.body = body
        self.shape = shape
