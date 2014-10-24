from pygamehelper import PygameHelper
import pygame
from pygame.locals import *
from vec2d import vec2d
from math import cos, sin
from environment import Environment
pygame.init()        	        
        
class Starter(PygameHelper):
    def __init__(self):
        infoObject = pygame.display.Info()
        print infoObject.current_w-100, infoObject.current_h-100
        self.w, self.h = infoObject.current_w-100, infoObject.current_h-100
        self.topx = vec2d(self.w/2, self.h/2)
        PygameHelper.__init__(self, size=(self.w, self.h), fill=((255,255,255)))
        self.bound = 50
        self.e = Environment()
        self.mode_build= 0      ### 0 == Agent, 1 == Goal, 2 == landmark, 3 == nest, 4 == pipe
        self.actiontext = "" 
        self.first = 0   
        self.firstpos = vec2d(0,0)   
        
    def update(self):
        self.e.update()
	
        for n in self.e.nests:
            for a in n.agents:
                bound = self.bound
                if a.pos.x<(-self.w/2+bound):
                    a.pos= a.pos + (self.w-2*bound,0)
                if a.pos.x>(self.w/2-bound):
                    a.pos= a.pos - (self.w-2*bound,0)
                if a.pos.y<(-self.h/2+bound):
                    a.pos= a.pos + (0,self.h-2*bound)
                if a.pos.y>(self.h/2-bound):
                    a.pos= a.pos - (0,self.h-2*bound)
        self.collision_detect()
                    
    def collision_detect(self):
        #here first detect and then resolve any overlaps
        for n in self.e.nests:
            for n2 in self.e.nests: 
                for a in n.agents:
                    for a2 in n2.agents:
                 
                     #we don't want to worry about an agent overlapping with himself
                     if a==a2: continue
                 
                     d= a.pos.get_distance(a2.pos)
                     dmax=10 
                     if d<dmax:
                         #resolve the collision!
                         overlap= dmax-d
                         dir= a2.pos- a.pos
                         if dir.length>1:
                             dir.length= overlap/2
                         dir.x= int(dir.x)
                         dir.y= int(dir.y) 
                         a2.pos= a2.pos+dir
                         a.pos= a.pos-dir
        
    def keyUp(self, key):
       if key==282: pygame.display.toggle_fullscreen()
       if key==97: self.mode_build= 0
       if key==103: self.mode_build= 1
       if key==104: 
           if self.e.selected== 0:
               for n in self.e.nests:
                   n.mode_run = 1
                   for a in n.agents:
                       a.mode_run = 1
           else:
               self.e.selected.mode_run = 1           
           for n in self.e.nests:
               if n== self.e.selected:
                   for a in n.agents:
                       a.mode_run = 1
       if key==108: self.mode_build= 2
       if key==110: self.mode_build= 3
       if key==111: 
           if self.e.selected== 0:
               for n in self.e.nests:
                   n.mode_run = 0
                   for a in n.agents:
                       a.mode_run = 0
           else:
               self.e.selected.mode_run = 0 
           for n in self.e.nests:
               if n== self.e.selected:
                   for a in n.agents:
                       a.mode_run = 0
       if key==112: self.mode_build= 4
       if key==127:
           for g in self.e.goals:
               if g==self.e.selected:
                   self.actiontext = "Removed goal "+str(self.e.goals.index(g))
                   self.e.goals.remove(self.e.selected)
           for lm in self.e.landmarks:
               if lm==self.e.selected:      
                   self.actiontext = "Removed landmark "+str(self.e.landmarks.index(lm))
                   self.e.landmarks.remove(self.e.selected)
           for n in self.e.nests:
               for a in n.agents:
                   if a==self.e.selected:
                       self.actiontext = "Removed agent "+str(n.agents.index(a))
                       n.agents.remove(self.e.selected)         
               if n== self.e.selected:
                   self.actiontext = "Removed nest "+str(self.e.nests.index(n))
                   self.e.nests.remove(self.e.selected)
                                    
            
       print key
        
    def mouseUp(self, button, pos):
        if button==3:
            if self.mode_build==0:             
                for n in self.e.nests:
                    if self.e.selected== n:
                        n.add_agent(n.pos)
                        n.num_agents += 1 
#                        self.e.selected= n.agents[len(n.agents)-1]
                        self.actiontext = "Created agent"
            if self.mode_build==1: 
                g= Goal(vec2d(pos)-self.topx)
                self.e.goals.append(g)
                self.actiontext = "Created goal"
            if self.mode_build==2: 
                lm= Landmark()
                lm.pos= pos-self.topx
                self.e.landmarks.append(lm)
                self.actiontext = "Created landmark"
            if self.mode_build==3: 
                self.e.add_nest(pos-self.topx)
                self.actiontext = "Created nest"
            if self.mode_build==4:
		
		if self.first==1:
			p= Pipe()
			p.pos0= self.firstpos-self.topx
			p.pos1= pos-self.topx
			self.e.pipes.append(p)
	 		self.actiontext = "Created pipe"
			self.first = 0
		elif self.first==0:
			self.firstpos = pos
			self.first = 1
			self.actiontext = "Created pipe start point"
                
        if button==1:
            tooclose = 0
            for g in self.e.goals:
                if g.pos.get_distance(vec2d(pos)-self.topx) <= 10:
                    tooclose = 1
                    self.e.selected= g
                    self.actiontext = "Selected goal "+str(self.e.goals.index(g))
            for lm in self.e.landmarks:
                if lm.pos.get_distance(vec2d(pos)-self.topx) <= 10:
                    tooclose = 1
                    self.e.selected= lm
                    self.actiontext = "Selected landmark "+str(self.e.landmarks.index(lm))
            for n in self.e.nests:
                if n.pos.get_distance(vec2d(pos)-self.topx) <= 20:
                    tooclose = 1
                    self.e.selected= n
                    self.actiontext = "Selected nest "+str(self.e.nests.index(n))
                for a in n.agents:
                    if a.pos.get_distance(vec2d(pos)-self.topx) <= 20:
                        tooclose = 1
                        self.e.selected= a
                        self.actiontext = "Selected agent "+str(n.agents.index(a))
                    
            if tooclose == 0:
                self.e.selected= 0
                self.actiontext = ""
#        self.target= vec2d(pos)
        
    def mouseMotion(self, buttons, pos, rel):
        pass
    
    def textaction(self):
        font=pygame.font.Font(None,24)
        black = (0, 0, 0)
        scoretext=font.render(self.actiontext, 1,black)	
        if self.e.selected != 0:         
            thetatext=font.render("Theta = "+str(self.e.selected.theta), 1,black)
            self.screen.blit(thetatext, (self.bound+self.w/2, self.h-self.bound))
        self.screen.blit(scoretext, (self.bound, self.h-self.bound))
    
    def textmode(self):
        font=pygame.font.Font(None,24)
        black = (0, 0, 0) 
        if self.mode_build==0: scoretext=font.render("Build mode: Agent", 1,black)
        if self.mode_build==1: scoretext=font.render("Build mode: Goal", 1,black)
        if self.mode_build==2: scoretext=font.render("Build mode: Landmark", 1,black)
        if self.mode_build==3: scoretext=font.render("Build mode: Nest", 1,black)     
        if self.mode_build==4: scoretext=font.render("Build mode: Pipe", 1,black)
        self.screen.blit(scoretext, (self.w-self.bound-240, self.h-self.bound))
        
    def draw(self):
        self.screen.fill((255,255,255))
        self.textmode()
        self.textaction()
#        pygame.draw.line(self.screen, (0,0,0), pos, (pos[0]-rel[0], pos[1]-rel[1]), 5)
        
        pygame.draw.rect(self.screen, (255,0,0), (self.bound, self.bound, self.w-2*self.bound, self.h-2*self.bound),3)
        
 	for p in self.e.pipes:
            pygame.draw.line(self.screen, (0,0,0), p.pos0+self.topx, p.pos1+self.topx, p.width)
            if p==self.e.selected:
                pygame.draw.line(self.screen, (225,225,225), p.pos0+self.topx, p.pos1+self.topx, p.width-1)

        for lm in self.e.landmarks:
            pygame.draw.circle(self.screen, (180,115,115), lm.pos+self.topx, lm.size) 
            if lm==self.e.selected:
                pygame.draw.circle(self.screen, (225,225,225), lm.pos+self.topx, lm.size-1)
        
        for n in self.e.nests:
            pygame.draw.circle(self.screen, n.color, n.pos+self.topx, n.size)
            if n==self.e.selected:
                pygame.draw.circle(self.screen, (225,225,225), n.pos+self.topx, n.size-1)
            for a in n.agents:
                #           pygame.draw.circle(self.screen, (255,0,0), a.target, 5, 1)
                for ph in a.pheros:
                    pygame.draw.circle(self.screen, (200,200,15), ph.pos+self.topx, ph.size)
                pygame.draw.circle(self.screen, a.color, a.pos+self.topx, a.size)
                dirct = vec2d(0,0)
                dirct.x = int(15*cos(a.phi))
                dirct.y = int(15*sin(a.phi))             
                pygame.draw.line(self.screen, (0,0,255), a.pos+self.topx, (a.pos+self.topx+dirct))
             
                if a==self.e.selected:
                    pygame.draw.circle(self.screen, (225,225,225), a.pos+self.topx, a.size-2)
                else:
                    pygame.draw.circle(self.screen, (0,0,0), a.pos+self.topx, a.size-2)
                    
        
        for g in self.e.goals:
            pygame.draw.circle(self.screen, (240,240,15), g.pos+self.topx, g.size)
            if g==self.e.selected:
                pygame.draw.circle(self.screen, (225,225,225), g.pos+self.topx, g.size-1)
        
        
s = Starter()
s.mainLoop(24)
