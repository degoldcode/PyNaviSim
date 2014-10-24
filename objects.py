from vec2d import vec2d
from math import e, exp, pi, cos, sin, sqrt, atan2

class Goal:
    def __init__(self, pos):
        self.pos= pos
        self.size = 8
        self.theta = atan2(pos.y,pos.x)
            
class Landmark:
    def __init__(self):
        self.pos= vec2d(0,0)
        self.size = 4

class Pipe:
    def __init__(self):
        self.pos0= vec2d(0,0)
        self.pos1= vec2d(0,0)
        self.width = 3