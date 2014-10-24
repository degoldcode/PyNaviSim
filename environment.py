from nest import Nest
from vec2d import vec2d
from objects import Goal, Landmark, Pipe

class Environment:
    def __init__(self, num_agents=1, num_nests=1, num_goals=0, num_lmarks=0, num_pipes=0):
        self.nests= []
        self.goals= []
        self.landmarks= []
        self.pipes= []
        self.bound = 50
        self.mode_run= 0        ### 0 == Out, 1 == Home        

        for i in range(num_nests):
            n= Nest(vec2d(0,0))
            for a in n.agents:
                a.npos = n.pos
            
            self.nests.append(n)
            self.selected= self.nests[len(self.nests)-1]	

    def add_nest(self, pos):
      n = Nest(pos)
      #n.pos = pos
            
      self.nests.append(n)
      self.selected= self.nests[len(self.nests)-1]
    
    def update(self):
        for n in self.nests:
            n.update()