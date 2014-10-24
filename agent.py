from vec2d import vec2d
from math import exp, pi, cos, sin, sqrt, atan2
from random import uniform, gauss
import numpy as np

PHEROMONES = 0

class Agent:
    def __init__(self):
        self.pheros= []
        if PHEROMONES== 1:        
            self.pdrop= 0.05
        else:
            self.pdrop= 0.00
        self.pos= vec2d(0,0)
        self.target= vec2d(0,0)
        self.phi = pi*uniform(0,359)/180.
        self.dist = sqrt(self.pos.x*self.pos.x + self.pos.y*self.pos.y)
        self.theta = 0.0
        self.size = 5
        self.color = (0,0,0)
        self.mode_run = 0
        self.npos = vec2d(0,0)
        
    def update(self):
        dir = vec2d(0,0)
        if self.mode_run == 0:
            dphi= gauss(0.0,0.5)
        elif self.mode_run == 1:
            dphi = 0.5*(sin(self.theta-self.phi-pi))
        self.phi += dphi
        dir.x = 3*cos(self.phi)
        dir.y = 3*sin(self.phi)
        if uniform(0.,1.) < self.pdrop:
            self.drop()
        for ph in self.pheros:
            ph.update()
            if ph.destroy== 1:
                self.pheros.remove(ph)
             
        if dir.length>3:
            dir.length= 3
        dir.x= int(dir.x)
        dir.y= int(dir.y)
        self.pos= self.pos + dir
        self.dist = sqrt((self.pos.x-self.npos.x)*(self.pos.x-self.npos.x) + (self.pos.y-self.npos.y)*(self.pos.y-self.npos.y))
        self.theta = atan2(self.pos.y-self.npos.y,self.pos.x-self.npos.x)
    
    def drop(self):
        ph= Pheromone(self.pos)
        self.pheros.append(ph)
        
class Controller:
    def __init__(self, pos):
        self.number=0
        
class CircularArray:
    def __init__(self, num_elem):
        self.N = num_elem
        self.activity = np.array(range(self.N))
        
class Pheromone:
    def __init__(self, pos):
        self.pos= pos
        self.size= 1
        self.dur= 0
        self.h= 0.0001
        self.life= exp(-self.h*self.dur)
        self.destroy= 0
        
    def update(self):
        self.dur += 1
        self.life= exp(-self.h*self.dur)
        if uniform(0.,1.) > self.life:
            self.destroy= 1