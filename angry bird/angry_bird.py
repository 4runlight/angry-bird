import math
import pygame
import time
import pymunk as pm
from character import Bird
from level import Level

#��ʼ��
pygame.init()
#������������
screen=pygame.display.set_mode((1200,650))
#���ô��ڱ���
pygame.display.set_caption('angry bird')

#��ʼ�������ͽ�ɫ
redbird=pygame.image.load("D:/python/angry bird/resources/images/red-bird3.png").convert_alpha()
background=pygame.image.load("D:/python/angry bird/resources/images/background3.png").convert_alpha()
sling_image=pygame.image.load("D:/python/angry bird/resources/images/sling-3.png").convert_alpha()
full_sprite=pygame.image.load("D:/python/angry bird/resources/images/full-sprite.png").convert_alpha()
#�������ͼƬ�Ա㵼��
rect=pygame.Rect(181,1050,50,50)
cropped=full_sprite.subsurface(rect).copy()
pig_image=pygame.transform.scale(cropped,(30,30))
#��ʼ����ť
buttons=pygame.image.load("D:/python/angry bird/resources/images/selected-buttons.png").convert_alpha()
#��Ϸʧ�ܶ���
pig_happy=pygame.image.load("D:/python/angry bird/resources/images/pig_failed.png").convert_alpha()
#��ʼ������
stars3=pygame.image.load("D:/python/angry bird/resources/images/stars.png").convert()
stars1=pygame.image.load("D:/python/angry bird/resources/images/stars1.png").convert()
stars2=pygame.image.load("D:/python/angry bird/resources/images/stars2.png").convert()

#��ͣ
rect=pygame.Rect(164,10,60,60)
pause_button=buttons.subsurface(rect).copy()
#����һ��
rect=pygame.Rect(24,4,100,100)
replay_button=buttons.subsurface(rect).copy()
#��һ��
rect=pygame.Rect(142,365,130,100)
next_button=buttons.subsurface(rect).copy()
clock=pygame.time.Clock()
#��ʼ��Ϸ
rect=pygame.Rect(18,212,100,100)
play_button=buttons.subsurface(rect).copy()
clock=pygame.time.Clock()

running=True

#��������
space=pm.Space()
space.gravity=(0.0,-700.0)
#��ʼ��
pigs=[]
birds=[]
balls=[]
polys=[]            #�����
beams=[]            #����
columns=[]          #����
poly_points=[]
ball_number=0
polys_dict={}
mouse_distance=0
rope_lenght=90      #����
angle=0             #�Ƕ�
x_mouse=0
y_mouse=0
count=0
mouse_pressed=False
t1=0
t2=0
tick_to_next_circle=10
RED=(255,0,0)       #��ɫ
BLUE=(0,0,255)
BLACK=(0,0,0)
WHITE=(255,255,255)
sling_x,sling_y=135,450     #����λ��
sling2_x,sling2_y=160,450
score=0             #�÷�
game_state=0
bird_path=[]
counter=0
restart_counter=False
bonus_score_once=True
#����
bold_font=pygame.font.SysFont("arial",30,bold=True)
bold_font2=pygame.font.SysFont("arial",40,bold=True)
bold_font3=pygame.font.SysFont("arial",50,bold=True)
wall=False

#����
static_body=pm.Body(body_type=pm.Body.STATIC)
x1=0.0,60.0
y1=1200.0,60.0
x2=1200.0,800.0
static_lines=[pm.Segment(static_body,x1,y1,0.0)]
static_lines1=[pm.Segment(static_body,y1,x2,0.0)]
for line in static_lines:
    line.elasticity=0.95    #����
    line.friction=1         #Ħ����
    line.collision_type=3   #��ײ����
for line in static_lines1:
    line.elasticity=0.95
    line.friction=1
    line.collision_type=2
space.add(static_body)
for line in static_lines:
    space.add(line)

#��pymunk����ת����Ϊpygame
def to_pygame(p):
    return int(p.x),int(-p.y+600)

#���ص��ʸ��
def vector(p0,p1):
    a=p1[0]-p0[0]
    b=p1[1]-p0[1]
    return(a,b)

#���ص�ĵ�λ����
def unit_vector(v):
    h=((v[0]**2)+(v[1]**2))**0.5
    if h==0:
        h=0.000000000000001
    ua=v[0]/h
    ub=v[0]/h
    return (ua,ub)

#��������֮��ľ���
def distance(x1,y1,x,y):
    dx=x-x1
    dy=y-y1
    d=((dx**2)+(dy**2))**0.5
    return d

#��ʼ������
def load_music():
    song1="D:/python/angry bird/resources/sounds/angry-birds.ogg"
    pygame.mixer.music.load(song1)
    pygame.mixer.music.play(-1)

#��������
def sling_action():
    global mouse_distance   #���������
    global rope_lenght
    global angle            #�Ƕ�
    global x_mouse
    global y_mouse
    #����̶��ڵ�����
    v=vector((sling_x,sling_y),(x_mouse,y_mouse))   #����뵯���γɵ�ʸ��
    uv=unit_vector(v)
    uv1=uv[0]
    uv2=uv[1]
    mouse_distance=distance(sling_x,sling_y,x_mouse,y_mouse)
    pu = (uv1*rope_lenght+sling_x, uv2*rope_lenght+sling_y)     #�����м������
    bigger_rope=102
    x_redbird=x_mouse-20    #�������
    y_redbird=y_mouse-20
    if mouse_distance>rope_lenght:
        pux,puy=pu
        pux-=20
        puy-=20
        pu1=pux,puy
        screen.blit(redbird,pu1)    #����С��
        #���Ƶ���
        pu2=(uv1*bigger_rope+sling_x,uv2*bigger_rope+sling_y)
        pygame.draw.line(screen,(0,0,0),(sling2_x,sling2_y),pu2,5)
        screen.blit(redbird,pu1)
        pygame.draw.line(screen,(0,0,0),(sling_x,sling_y),pu2,5)
    else:
        mouse_distance+=10
        pygame.draw.line(screen,(0,0,0),(sling2_x,sling2_y),(x_mouse,y_mouse),5)
        screen.blit(redbird,(x_redbird,y_redbird))
        pygame.draw.line(screen,(0,0,0),(sling_x,sling_y),(x_mouse,y_mouse),5)
    
    #���ʸ���Ƕ�
    dx=x_mouse-sling_x
    dy=y_mouse-sling_y
    if dx==0:
        dx=0.000000000000001
    angle=math.atan((float(dy))/dx)

#�ؿ��ɹ�
def draw_level_cleared():
    global game_state
    global bonus_score_once
    global score
    #��ʾ����
    level_cleared=bold_font3.render("Level Cleared!",1,BLACK)
    score_level_cleared=bold_font2.render(str(score),1,BLACK)
    if level.number_of_birds >= 0 and len(pigs) == 0:
        if bonus_score_once:
            score += (level.number_of_birds-1)*10000
        bonus_score_once=False
        game_state=4
        rect=pygame.Rect(300,0,600,800)
        pygame.draw.rect(screen,WHITE,rect)
        screen.blit(level_cleared,(450,90))
        #��ʾ�Ǽ�
        if score >= level.one_star and score <= level.two_star:
            screen.blit(stars1,(310,190))
        if score >= level.two_star and score <= level.three_star:
            screen.blit(stars2,(310,190))
        if score >= level.three_star:
            screen.blit(stars3,(310,190))
        screen.blit(score_level_cleared,(550,400))
        screen.blit(replay_button,(510,480))
        screen.blit(next_button,(620,480))

#�ؿ�ʧ��
def draw_level_failed():
    global game_state
    failed = bold_font3.render("Level Failed",1,BLACK)
    if level.number_of_birds <= 0 and time.time() - t2 > 5 and len(pigs) >0:
        game_state=3
        rect=pygame.Rect(300,0,600,800)
        pygame.draw.rect(screen,WHITE,rect)
        screen.blit(failed,(450,90))
        screen.blit(pig_happy,(380,120))
        screen.blit(replay_button,(520,460))

#���¿�ʼ
def restart():
    pigs_to_remove = []
    birds_to_remove = []
    columns_to_remove = []
    beams_to_remove = []
    #������Ӹ�������
    for pig in pigs:
        pigs_to_remove.append(pig)
    for pig in pigs_to_remove:
        space.remove(pig.shape, pig.shape.body)
        pigs.remove(pig)
    for bird in birds:
        birds_to_remove.append(bird)
    for bird in birds_to_remove:
        space.remove(bird.shape, bird.shape.body)
        birds.remove(bird)
    for column in columns:
        columns_to_remove.append(column)
    for column in columns_to_remove:
        space.remove(column.shape, column.shape.body)
        columns.remove(column)
    for beam in beams:
        beams_to_remove.append(beam)
    for beam in beams_to_remove:
        space.remove(beam.shape, beam.shape.body)
        beams.remove(beam)
        
#�����֮�����ײ
def post_solve_bird_pig(arbiter,space, _):
    surface=screen
    a,b=arbiter.shapes
    bird_body=a.body
    pig_body=b.body
    #��ײЧ��
    p1=to_pygame(bird_body.position)
    p2=to_pygame(pig_body.position)
    r=30
    pygame.draw.circle(surface,BLACK,p1,r,4)
    pygame.draw.circle(surface,RED,p2,r,4)
    #��������ײ������ֵ�����ұ����ײ
    for bird in birds:
        if bird_body == bird.body:
            bird.col=True
            bird.life-=20
        #С������ֵΪ�����ײ�������ʧ
        if bird.life<=0 or bird.col or bird.shape.body.position.y>= 590:
            birds_to_remove.append(bird)
        
        if birds_to_remove is not None:
            for bird in birds_to_remove:
                space.remove(bird.shape,bird.shape.body)
                birds.remove(bird)
            
    #����ײ��������ֵΪ��÷���ʧ
    pigs_to_remove = []
    for pig in pigs:
        if pig_body == pig.body:
            pig.life -=20
            if pig.life <= 0:
                pigs_to_remove.append(pig)
                global score
                score += 10000
        if pigs_to_remove is not None:
            for pig in pigs_to_remove:
                space.remove(pig.shape,pig.shape.body)
                pigs.remove(pig)

#�����ϰ���֮�����ײ
def post_solve_bird_wood(arbiter,space, _):
    poly_to_remove = []
    #�ϰ�����ײ����ʧ
    if arbiter.total_impulse.length > 1100:
        a,b=arbiter.shapes
        bird_body=a.body
        #����ײ������ֵ�����ұ����ײ
        ''' bird in birds:
            if bird_body == bird.body:
                bird.col=True
                bird.life-=20
        if bird.life<=0 or bird.col or bird.shape.body.position.y>= 590:
            birds_to_remove.append(bird)
        
        if birds_to_remove is not None:
            for bird in birds_to_remove:
                space.remove(bird.shape,bird.shape.body)
                birds.remove(bird)'''
        #�ϰ�����ײ��ʧ
        for column in columns:
            if b== column.shape:
                poly_to_remove.append(column)
        for beam in beams:
            if b ==beam.shape:
                poly_to_remove.append(beam)
        for poly in poly_to_remove:
            if poly in columns:
                columns.remove(poly)
            if poly in beams:
                beams.remove(poly)
        space.remove(b,b.body)
        global score
        score += 5000

#�����ϰ���֮�����ײ
def post_solve_pig_wood(arbiter,space, _):
    pigs_to_remove = []
    if arbiter.total_impulse.length > 700:
        pig_shape,wood_shape =arbiter.shapes
        #����ײ��������Ϊ����÷���ʧ
        for pig in pigs:
            if pig_shape == pig.shape:
                pig.life -= 20
                global score
                score +=10000
                if pig.life <= 0:
                    pigs_to_remove.append(pig)
    if pigs_to_remove is not None:
        for pig in pigs_to_remove:
            space.remove(pig.shape,pig.shape.body)
            pigs.remove(pig)

#���������ײ
space.add_collision_handler(0,1).post_solve=post_solve_bird_pig
#�����ϰ������ײ
space.add_collision_handler(0,2).post_solve=post_solve_bird_wood
#�����ϰ������ײ
space.add_collision_handler(1,2).post_solve=post_solve_pig_wood

#��������
load_music()

#���ùؿ�
level =Level(pigs,columns,beams,space)
level.number=0
level.load_level()


#��Ϸ����  
while running:
    #�������
    for event in pygame.event.get():
        #����˳����˳�
        if event.type==pygame.QUIT:
            running = False
        #��esc�˳�
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        #��w���л��߽�
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            if wall:
                for line in static_lines1:
                    space.remove(line)
                wall = False
            else:
                for line in static_lines1:
                    space.add(line)
                wall = True
        #��s����������״̬
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            space.gravity = (0.0,-10.0)
            level.bool_space =True
        #��n���ָ�
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
            space.gravity = (0.0,-700.0)
            level.bool_space =False
        #���С��
        if(pygame.mouse.get_pressed()[0] and x_mouse > 100 and
                x_mouse < 250 and y_mouse > 370 and y_mouse< 550):
            mouse_pressed =True
        #�ͷ�С��
        if(event.type == pygame.MOUSEBUTTONUP and
                event.button ==1 and mouse_pressed):
            mouse_pressed =False
            #�������С��������һ
            if level.number_of_birds > 0:
                level.number_of_birds -= 1
                t1 = time.time()*1000
                x0 = 154
                y0 = 156
                #�������������޷�������������
                if mouse_distance > rope_lenght:
                    mouse_distance = rope_lenght
                #װ��С��
                if x_mouse < sling_x+5:
                    bird = Bird(mouse_distance,angle,x0,y0,space)
                    birds.append(bird)
                else:
                    bird = Bird(-mouse_distance,angle,x0,y0,space)
                    birds.append(bird)
                #С��������ؿ�����
                if level.number_of_birds ==0:
                    t2 = time.time()
        #ȷ����Ϸ״̬
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if(x_mouse < 60 and y_mouse <155 and y_mouse > 90):
                game_state = 1
            if game_state ==1:
                if x_mouse > 500 and y_mouse > 200 and y_mouse < 300:
                    #��Ϸ��ͣ
                    game_state = 0
                if x_mouse > 500 and y_mouse > 300:
                    #���汾��
                    restart()
                    level.load_level()
                    game_state = 0
                    bird_path = []
            if game_state ==3:
                #�ؿ�ʧ�ܺ����¿�ʼ
                if x_mouse > 500 and x_mouse < 620 and y_mouse > 450:
                    restart()
                    level.load_level()
                    game_state = 0
                    bird_path = []
                    score = 0
            if game_state == 4:
                #�ؿ��ɹ�������һ��
                if x_mouse > 610 and y_mouse > 450:
                    restart()
                    level.number += 1
                    game_state = 0
                    level.load_level()
                    score = 0
                    bird_path = []
                    bonus_score_once = True
                #�ؿ��ɹ����¿�ʼ����
                if x_mouse < 610 and x_mouse >500 and y_mouse > 450:
                    restart()
                    level.load_level()
                    game_state = 0
                    bird_path = []
                    score = 0
    x_mouse,y_mouse = pygame.mouse.get_pos()
    #����
    screen.fill((130,200,100))
    screen.blit(background,(0,-50))
    #���Ƶ���
    rect = pygame.Rect(50,0,70,220)
    screen.blit(sling_image,(138,420),rect)
    #С��·��
    for point in bird_path:
        pygame.draw.circle(screen,WHITE,point,5,0)
    #�ȴ���С��
    if level.number_of_birds > 0:
        for i in range(level.number_of_birds-1):
            x = 100 - (i*35)
            screen.blit(redbird,(x,508))
    #��̬����
    if mouse_pressed and level.number_of_birds > 0:
        sling_action()
    else:
        if time.time()*1000 - t1 > 300 and level.number_of_birds > 0:
            screen.blit(redbird,(130,426))
        else:
            pygame.draw.line(screen,(0,0,0),(sling_x,sling_y-8),(sling2_x,sling2_y-7),5)
    birds_to_remove = []
    pigs_to_remove = []
    counter +=1

    #��
    for bird in birds:
        #������Ļ�����
        if (bird.shape.body.position.y>=590 or bird.shape.body.position.y <0
                or bird.shape.body.position.x<=0 or bird.shape.body.position.x>=1200):
            birds_to_remove.append(bird)
        #����С��
        p=to_pygame(bird.shape.body.position)
        x,y = p
        x -= 22
        y -= 20
        screen.blit(redbird,(x,y))

        if counter >=3 and time.time() -t1 < 5:
            bird_path.append(p)
            restart_counter = True
    if restart_counter:
        counter = 0
        restart_counter = False
    #��������
    if birds_to_remove is not None:
        for bird in birds_to_remove:
            birds.remove(bird)
            space.remove(bird.shape, bird.shape.body)
    if pigs_to_remove is not None:
        for pig in pigs_to_remove:
            pigs.remove(pig)
            space.remove(pig.shape, pig.shape.body)
            
    #����
    for line in static_lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1)
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, (150, 150, 150), False, [p1, p2])

    #��
    i=0
    for pig in pigs:
        i+=1
        pig = pig.shape
        #�������ʧ
        if pig.body.position.y < 0:
            pigs_to_remove.append(pig)
        #������λ��
        p=to_pygame(pig.body.position)
        x,y=p
        #����˶�
        angle_degrees=math.degrees(pig.body.angle)
        img=pygame.transform.rotate(pig_image,angle_degrees)
        w,h=img.get_size()
        x -= w*0.5
        y -= h*0.5
        screen.blit(img,(x,y))
    #�ϰ���
    for column in columns:
        column.draw_poly('columns', screen)
    for beam in beams:
        beam.draw_poly('beams', screen)
    #ÿһ֡�������θ���
    dt= 1.0/50.0/2.0
    for x in range(2):
        space.step(dt)

    #����
    rect = pygame.Rect(0,0,60,200)
    screen.blit(sling_image,(120,420),rect)

    #�÷�
    score_font =bold_font.render("SCORE",1,WHITE)
    number_font= bold_font.render(str(score),1,WHITE)
    screen.blit(score_font,(1060,90))
    if score ==0:
        screen.blit(number_font,(1100,130))
    else:
        screen.blit(number_font,(1060,130))

    #��ͣ
    screen.blit(pause_button,(10,90))
    if game_state == 1:
        screen.blit(play_button,(500,200))
        screen.blit(replay_button,(500,300))
    draw_level_cleared()
    draw_level_failed()

    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps:"+str(clock.get_fps()))
