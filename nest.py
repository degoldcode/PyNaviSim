from random import uniform, gauss
from agent import Agent, Pheromone, Controller

class Nest:
    def __init__(self,pos):
        self.agents= []
        self.pos= pos
        self.size = 10
        self.num_agents = 10
        self.mode_run= 0        ### 0 == Out, 1 == Home
        self.color = (int(uniform(0,255)),int(uniform(0,255)),int(uniform(0,255)))
        print self.color
        self.theta = 0.0
        self.phi = 0.0
        
        for i in range(10):
            self.add_agent(self.pos)
            
    def update(self):
        if self.mode_run==0:
            while len(self.agents) < self.num_agents:
                self.add_agent(self.pos)
                self.actiontext = "Created agent"
        for a in self.agents:
            a.update()
            if a.mode_run==1:
                if a.dist < 10:              
                    self.agents.remove(a)
                    self.actiontext = "Removed agent"
	    
    def add_agent(self, pos):
      a= Agent()
      a.pos = pos
      a.npos = self.pos
      a.color= self.color
      self.agents.append(a)