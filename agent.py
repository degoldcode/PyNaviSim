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
        self.control = Controller()
        
    def update(self):
        dir = vec2d(0,0)
        if self.mode_run == 0:
            dphi= gauss(0.0,0.5)
        elif self.mode_run == 1:
            dphi = 0.5*(sin(self.theta-self.phi-pi))
        self.phi += dphi
        dir.x = 3.*cos(self.phi)
        dir.y = 3.*sin(self.phi)
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
        self.control.update(self.phi, 3.)
        
    
    def drop(self):
        ph= Pheromone(self.pos)
        self.pheros.append(ph)
        
class Controller:
    def __init__(self):
        self.num_units=360
        self.PIN = PIN(self.num_units)
        
    def update(self, angle, speed):
        self.PIN.update(angle, speed)
        
class PIN:
    def __init__(self, num):
        self.num_units= num        
        self.HD = CircularArray(self.num_units) 
        self.G = CircularArray(self.num_units)
        self.M = CircularArray(self.num_units)
        self.PI = CircularArray(self.num_units)
        self.cosker = np.zeros((self.num_units,self.num_units))
        for i in range(0,self.num_units):
            for j in range(0,self.num_units):
                self.cosker[i,j] = cos(2.*pi*(i-j)/self.num_units)
                
        
    def update(self, angle, speed):
        self.HD.activity = np.cos(angle-self.HD.pref)
        self.G.activity = speed*self.HD.activity
        np.clip(self.G.activity,0.,1.)
        self.M.activity = self.G.activity + self.M.activity
        self.PI.activity = np.dot(self.cosker, self.M.activity)
        
class CircularArray:
    def __init__(self, num_elem):
        self.N = num_elem
        self.activity = np.array(range(self.N))
        self.pref = np.array(range(self.N))
        for i in range(0,self.N):
            self.pref[i] = 2.*pi*i/self.N
        
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