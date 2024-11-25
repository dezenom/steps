import pygame
from settings import IMMUNITY
from mytoolkit_pygame.particles import particle_system

class Entity():
    def __init__(self,pos,screen,size =[16,16]):
        self.screen = screen
        self.image = pygame.Surface((size[0],size[1]))
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)
        # movement
        self.direction = pygame.Vector2((1,0))
        self.speedx = 0
        self.friction = 0.5
        self.maxspeed = 1
        self.dt = 0
        self.inc = 80
        # animation
        self.is_left = False
        self.id_down = False
        self.status = 0
        self.animspeed = 1 
        # damage and health
        self.immunity = 0
        self.health = 0
        self.maxhealth = 0
        self.atk_dmg = 0

        
        self.particles = particle_system()
        
    def damage(self,atkdmg):
        if self.immunity < 0:
            self.immunity = IMMUNITY
            self.health -= atkdmg


    # draw and update


    def render(self,offset):
        self.image = self.animation.animation(self.status,self.is_left)
        pos = self.rect.topleft + offset
        self.screen.blit(self.image,pos)   
        self.particles.emit(self.screen,offset)
    
    def update(self,scroll,dt):
        self.dt = dt * self.inc if dt > 0 else 1
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        self.immunity -=1
        self.anim_speed = 1.5 * self.dt
        
        self.collisions = { 
            "up" : 0,
            "down" : 0,
            "left" : 0,
            "right" : 0 }