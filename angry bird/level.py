from character import Pig
from polygon import Polygon

class Level():
    def __init__(self,pigs,columns,beams,space):
        #初始化
        self.pigs = pigs
        self.columns = columns
        self.beams = beams
        self.space = space
        self.number = 0
        self.number_of_birds = 4
        #星级分数
        self.one_star = 30000
        self.two_star = 40000
        self.three_star = 60000
        self.bool_space = False

    #开口平台
    def open_flat(self,x,y,n):
        y0=y
        for i in range(n):
            y=y0+100+i*100
            p=(x,y)
            self.columns.append(Polygon(p,20,85,self.space))
            p=(x+60,y)
            self.columns.append(Polygon(p,20,85,self.space))
            p=(x+30,y+50)
            self.beams.append(Polygon(p,85,20,self.space))
    
    #闭口平台
    def closed_flat(self, x, y, n):
        y0 = y
        for i in range(n):
            y = y0+100+i*125
            p = (x+1, y+22)
            self.columns.append(Polygon(p, 20, 85, self.space))
            p = (x+60, y+22)
            self.columns.append(Polygon(p, 20, 85, self.space))
            p = (x+30, y+70)
            self.beams.append(Polygon(p, 85, 20, self.space))
            p = (x+30, y-30)
            self.beams.append(Polygon(p, 85, 20, self.space))
    #水平柱子
    def horizontal_pile(self,x,y,n):
        y += 70
        for i in range(n):
            p=(x,y+i*20)
            self.beams.append(Polygon(p,85,20,self.space))

    #垂直柱子
    def vertical_pile(self, x, y, n):
        y += 10
        for i in range(n):
            p = (x, y+85+i*85)
            self.columns.append(Polygon(p, 20, 85, self.space))
    
    #创造关卡零
    def build_0(self):
        #放置猪
        pig1 = Pig(980, 100, self.space)
        pig2 = Pig(985, 182, self.space)
        self.pigs.append(pig1)
        self.pigs.append(pig2)
        #放置障碍物
        p = (950, 80)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1010, 80)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (980, 150)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (950, 200)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1010, 200)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (980, 240)
        self.beams.append(Polygon(p, 85, 20, self.space))
        #设置小鸟数量
        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8
        #设置星级分数
        self.one_star = 30000
        self.two_star = 40000
        self.three_star = 60000

    #创造关卡一
    def build_1(self):
        #放置猪
        pig = Pig(1000, 100, self.space)
        self.pigs.append(pig)
        #放置障碍物
        p = (900, 80)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (850, 80)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (850, 150)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1050, 150)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1105, 210)
        self.beams.append(Polygon(p, 85, 20, self.space))
        #设置小鸟数量
        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def load_level(self):
        try:
            build_name ="build_"+str(self.number)
            getattr(self,build_name)()
        except AttributeError:
            self.number = 0
            build_name = "build_"+str(self.number)
            getattr(self,build_name)()