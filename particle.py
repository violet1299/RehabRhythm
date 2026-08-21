import pygame, random, math
from config import *
class Particle:
    def __init__(self,x,y,color=None):
        self.x=x; self.y=y; a=random.uniform(0,math.pi*2); s=random.uniform(1.5,4.5); self.vx=math.cos(a)*s; self.vy=math.sin(a)*s; self.alpha=180; self.size=random.randint(4,9); self.color=color or random.choice([BLUE,GREEN,YELLOW,WHITE])
    def update(self):
        self.x+=self.vx; self.y+=self.vy; self.vx*=0.96; self.vy*=0.96; self.alpha-=6; return self.alpha>0
    def draw(self,screen):
        if self.alpha<=0: return
        surf=pygame.Surface((self.size*2,self.size*2),pygame.SRCALPHA); pygame.draw.circle(surf,(*self.color,self.alpha),(self.size,self.size),self.size); screen.blit(surf,(int(self.x-self.size),int(self.y-self.size)))
def create_hit_particles(x,y,judgement="GOOD"):
    color,count=(GREEN,24) if judgement=="PERFECT" else (BLUE,16) if judgement=="GOOD" else (RED,8)
    return [Particle(x,y,color) for _ in range(count)]
