import pygame, math
from mytoolkit_pygame.AnimationHandler import Animation_Handler
from mytoolkit_pygame.TilesSupport import render_text
from entities.entity import Entity
from settings import IMMUNITY
from entities.health_bar import HealthBar
from random import randint

health_bar = pygame.transform.scale_by(pygame.image.load("res/ui/bar.png"),2)

class player(Entity):
    def __init__(self,pos,screen,display,size = [25,24]):
        super().__init__(pos,screen,size) 
        self.display = display
        # movement
        self.collisions = { "up" : 0,
                            "down" : 0,
                            "left" : 0,
                            "right" : 0 }

        self.friction = 1
        self.speedy = -5
        self.maxspeed = 5
        self.acceleration = 1.2
        self.dash = False
        self.dash_cooldown = 0
        self.dash_speed = 3 
        # jump
        self.gravity = 0.4
        self.on_ground = False
        self.jump = False
        self.jumpcount = 0
        self.jumpmax = 1
        self.on_wall = 0

        # animation
        self.animspeed = 1
        self.animation = Animation_Handler(self.animspeed,"res/Animations/player_animations.png",size) 

        # attack
        self.attacking = False
        self.attack_cooldown = 0
        self.atk_dmg = 120
        self.pierce = 1
        self.projectiles = []
        self.knife = pygame.transform.scale_by(pygame.image.load("res/projectiles/knife.png"),2)
        self.proj_speed = 6
        self.noof_projectiles = 64
        self.proj_limit = 1
        self.proj_size = 1
        self.range = 5



        self.maxhealth = 1200
        self.health = self.maxhealth
        self.healthbar = HealthBar((255,100,120),self,[118,22])   


        self.changers()

    # player movement
    def keys(self):
        keys = pygame.key.get_pressed()
        if (self.jump and (self.on_ground or self.jumpcount <self.jumpmax)) or (self.jump and self.on_wall > 0):
            if self.on_wall > 0 and self.collisions["left"]:
                self.speedx = 6
                self.direction.x = 1
            if self.on_wall > 0 and self.collisions["right"]:
                self.speedx = 6
                self.direction.x = -1
            self.on_wall = 0
            self.on_ground = False
            self.jumpcount += 1
            self.direction.y = 0
            self.jumping()
        self.jump = False
        if keys[pygame.K_a] and self.speedx < self.maxspeed:
            if self.direction.x == 1:
                self.speedx = 0
            self.direction.x = -1
            self.speedx += self.acceleration
        elif keys[pygame.K_d] and self.speedx < self.maxspeed:
            if self.direction.x == -1:
                self.speedx = 0
            self.direction.x = 1
            self.speedx += self.acceleration
    def applyfriction(self):
        self.speedx -= self.friction 
        if self.speedx <= 0.1:
            self.speedx = 0
    def applygravity(self):
        self.direction.y += self.gravity if self.direction.y < 10 else 0 
        self.rect.y += self.direction.y * self.dt

    def jumping(self):
        self.direction.y = self.speedy
        self.rect.y += self.direction.y * self.dt 
        for i in range(3):
            self.particles.add_particle([self.rect.centerx,self.rect.bottomleft[1]],4,(255,255,255))

    def movement(self):
        if self.on_ground:
            self.jumpcount = 0
        if self.collisions["left"] or self.collisions["right"]:
            self.on_wall = 20
            self.jumpcount = 0
        self.gravity = 0.1 if self.collisions["left"] or self.collisions["right"] else 0.4
        self.on_wall -= 1

        self.keys()
        self.applyfriction()
        
        self.is_left = True if self.direction.x < 0 else False
        if self.speedx > 10 and not self.dash:
            self.speedx = 5
        if self.direction.y > 15 :self.direction.y = 0


    def get_status(self):

        if self.direction.y <-1:
            self.status = 2
        elif self.direction.y>1.5:
            self.status = 3
        else:
            if self.speedx <= 0.2:
                self.status = 0
            else:
                self.status = 1
        if (self.collisions["left"] or self.collisions["right"]):
            self.status = 5
        if self.attack_cooldown >-5:
            self.status = 6

    # actions
    def attack(self,scroll):
        vector = [self.rect.x - pygame.mouse.get_pos()[0] , self.rect.y - pygame.mouse.get_pos()[1]]
        mag = math.sqrt(vector[0]**2+vector[1]**2)
        self.nv = [vector[0]/mag,vector[1]/mag] if mag != 0 else [0,0]
        self.angle = math.degrees(math.asin(self.nv[1])) +45 if self.nv[0] > 0 else -math.degrees(math.asin(self.nv[1])) - 135
        if self.attacking and self.attack_cooldown < 0 and self.noof_projectiles>0:
            for i in range(self.proj_limit):
                self.speedx = 0
                self.attack_cooldown = 10
                img = pygame.transform.scale_by(self.knife,self.proj_size)
                rect = pygame.FRect(self.rect.centerx,self.rect.centery,
                                    img.get_width(),img.get_height())
                self.projectiles.append([img,
                                         rect,
                                         (self.nv[0] + randint(-4,4)*i/self.range,self.nv[1] + randint(-4,4)*i/self.range),
                                         -self.angle,
                                         self.pierce])
                for i in range(4):
                    self.particles.add_particle([self.rect.x,self.rect.y],1,(255,255,255))
    
            self.direction.x = self.nv[0]
            self.speedx += 5
            self.direction.y += 3 *self.nv[1]
            self.noof_projectiles-=1

        self.attack_cooldown -= 1
        self.attacking = False

        for obj in self.projectiles:
            obj[1].x += self.proj_speed *-obj[2][0] * self.dt - scroll[0] 
            obj[1].y += self.proj_speed *-obj[2][1] * self.dt - scroll[1] 
            if abs(obj[1][0])>self.screen.get_width() or abs(obj[1][1]) > self.screen.get_height() or obj[4]<1:
                self.projectiles.remove(obj)
    def dashing(self):
        if self.dash and self.dash_cooldown < 0:
            self.dash_cooldown = 90
            self.speedx += self.dash_speed
            self.immunity = IMMUNITY
            for i in range(4):
                self.particles.add_particle([self.rect.x,self.rect.y],2,(255,255,255))
        self.dash_cooldown -= 1
        if self.dash_cooldown < 60:
            self.dash = False

    def changers(self):
        def damage_inc():
            self.atk_dmg +=50
        def health_inc():
            self.maxhealth += 50
            self.health = self.maxhealth
        def pierce_inc():
            self.pierce+=1
        def charge():
            self.noof_projectiles = 64
        def add():
            if self.proj_limit < 20:
                self.proj_limit+=1
        def speed():
            self.proj_speed+=3
        def large():
            self.proj_size+=0.5
            self.proj_speed+=0.5
        def control():
            self.range += 5 if self.range < 100 else 0
        def jump():
            self.jumpmax +=1
        def dash():
            self.dash_speed += 5

        self.increments= [damage_inc,health_inc,pierce_inc,charge,add,speed,large,control,jump,dash]

    # draw and update
    def render(self,offset):
        super().render(offset)
        for obj in self.projectiles:
            rmg = pygame.transform.rotate(obj[0],obj[3])
            self.screen.blit(rmg,(obj[1].x-rmg.get_width()/2,obj[1].y-rmg.get_height()/2)+offset)
        self.healthbar.draw(self.display,[13,8])
        self.display.blit(health_bar, [4,5])
        self.display.blit(pygame.transform.scale_by(self.knife,1.5),[150,10])
        render_text(self.display,str(self.noof_projectiles),(190,25),"res/fonts/Daydream.ttf",10)
        
    def update(self,scroll,dt):
        self.dt = dt * self.inc if dt > 0 else 1
        self.movement()
        self.get_status()
        self.attack(scroll)
        self.dashing()
        self.immunity -=1

        
        self.collisions = { 
            "up" : 0,
            "down" : 0,
            "left" : 0,
            "right" : 0 }