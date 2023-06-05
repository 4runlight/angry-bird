import pymunk as pm
from pymunk import Vec2d    #平面向量类
import pygame
import math


class Polygon():
    def __init__(self, pos, length, height, space, mass=5.0):
        #创造障碍物
        moment = 1000
        body = pm.Body(mass, moment)
        #获得障碍物位置
        body.position = Vec2d(*pos)
        #障碍物参数赋值
        shape = pm.Poly.create_box(body, (length, height))
        shape.color = (0, 0, 255)
        shape.friction = 0.5
        shape.collision_type = 2
        space.add(body, shape)
        
        self.body = body
        self.shape = shape
        
        #初始化障碍物图片
        wood = pygame.image.load("D:/python/angry bird/resources/images/wood.png").convert_alpha()
        wood2 = pygame.image.load("D:/python/angry bird/resources/images/wood2.png").convert_alpha()
        rect = pygame.Rect(251, 357, 86, 22)
        self.beam_image = wood.subsurface(rect).copy()
        rect = pygame.Rect(16, 252, 22, 84)
        self.column_image = wood2.subsurface(rect).copy()
    
    #pymunk坐标转化为python坐标
    def to_pygame(self, p):
        return int(p.x), int(-p.y+600)

    #障碍物绘制
    def draw_poly(self, element, screen):
        poly = self.shape
        #获得障碍物顶点
        ps = poly.get_vertices()
        ps.append(ps[0])
        ps = map(self.to_pygame, ps)
        ps = list(ps)
        #确定颜色
        color = (255, 0, 0)
        #绘制障碍物
        pygame.draw.lines(screen, color, False, ps)

        if element == 'beams':
            #获得障碍物位置
            p = poly.body.position
            p = Vec2d(*self.to_pygame(p))
            #障碍物旋转
            angle_degrees = math.degrees(poly.body.angle) + 180
            rotated_logo_img = pygame.transform.rotate(self.beam_image,angle_degrees)
            #绘制障碍物                                           
            offset = Vec2d(*rotated_logo_img.get_size()) / 2.
            np = p - offset
            screen.blit(rotated_logo_img, (np.x, np.y))
        if element == 'columns':
            #获得障碍物位置
            p = poly.body.position
            p = Vec2d(*self.to_pygame(p))
            #障碍物旋转
            angle_degrees = math.degrees(poly.body.angle) + 180
            rotated_logo_img = pygame.transform.rotate(self.column_image,angle_degrees)
            #绘制障碍物                                           
            offset = Vec2d(*rotated_logo_img.get_size()) / 2.0
            np = p - offset
            screen.blit(rotated_logo_img, (np.x, np.y))
