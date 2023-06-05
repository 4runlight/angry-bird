import pymunk as pm
from pymunk import Vec2d    #ƽ��������
import pygame
import math


class Polygon():
    def __init__(self, pos, length, height, space, mass=5.0):
        #�����ϰ���
        moment = 1000
        body = pm.Body(mass, moment)
        #����ϰ���λ��
        body.position = Vec2d(*pos)
        #�ϰ��������ֵ
        shape = pm.Poly.create_box(body, (length, height))
        shape.color = (0, 0, 255)
        shape.friction = 0.5
        shape.collision_type = 2
        space.add(body, shape)
        
        self.body = body
        self.shape = shape
        
        #��ʼ���ϰ���ͼƬ
        wood = pygame.image.load("D:/python/angry bird/resources/images/wood.png").convert_alpha()
        wood2 = pygame.image.load("D:/python/angry bird/resources/images/wood2.png").convert_alpha()
        rect = pygame.Rect(251, 357, 86, 22)
        self.beam_image = wood.subsurface(rect).copy()
        rect = pygame.Rect(16, 252, 22, 84)
        self.column_image = wood2.subsurface(rect).copy()
    
    #pymunk����ת��Ϊpython����
    def to_pygame(self, p):
        return int(p.x), int(-p.y+600)

    #�ϰ������
    def draw_poly(self, element, screen):
        poly = self.shape
        #����ϰ��ﶥ��
        ps = poly.get_vertices()
        ps.append(ps[0])
        ps = map(self.to_pygame, ps)
        ps = list(ps)
        #ȷ����ɫ
        color = (255, 0, 0)
        #�����ϰ���
        pygame.draw.lines(screen, color, False, ps)

        if element == 'beams':
            #����ϰ���λ��
            p = poly.body.position
            p = Vec2d(*self.to_pygame(p))
            #�ϰ�����ת
            angle_degrees = math.degrees(poly.body.angle) + 180
            rotated_logo_img = pygame.transform.rotate(self.beam_image,angle_degrees)
            #�����ϰ���                                           
            offset = Vec2d(*rotated_logo_img.get_size()) / 2.
            np = p - offset
            screen.blit(rotated_logo_img, (np.x, np.y))
        if element == 'columns':
            #����ϰ���λ��
            p = poly.body.position
            p = Vec2d(*self.to_pygame(p))
            #�ϰ�����ת
            angle_degrees = math.degrees(poly.body.angle) + 180
            rotated_logo_img = pygame.transform.rotate(self.column_image,angle_degrees)
            #�����ϰ���                                           
            offset = Vec2d(*rotated_logo_img.get_size()) / 2.0
            np = p - offset
            screen.blit(rotated_logo_img, (np.x, np.y))
