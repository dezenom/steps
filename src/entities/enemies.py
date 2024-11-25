import pygame , math
from entities.entity import Entity
from entities.health_bar import HealthBar
from random import randint
from mytoolkit_pygame.AnimationHandler import Animation_Handler

# NORMAL ENEMY
class lazerEnemy(Entity):
    def __init__(self,pos,screen,player,size = [16,16],inc= {}):
        super().__init__(pos,screen,size)
        self.player = player
        self.winc = inc
        # movement
        self.change = 0
        self.range = randint(50,100)

        self.maxspeed = randint(1,3)+inc["sp"]
        self.speedy= 0
        self.attack_speed = 5
        self.timer = 300
        self.atk_dmg = 50 + inc["ap"]
        self.attacking = False
        # animation
        self.animation = Animation_Handler(self.animspeed,"res/Animations/enemy/eye1.png",[16,16]) 

        # health and others
        self.original_maxhp = 150 + inc["hp"]
        self.maxhealth = self.original_maxhp
        self.health = self.maxhealth
        self.healthbar = HealthBar((200,200,255),self,[20,4])
        

# movement

    def follow(self):
        self.speedx = self.maxspeed
        self.speedy = self.maxspeed
        if not self.attacking:
            self.mag = math.sqrt(self.vector[0]**2 + self.vector[1]**2)
            point = [self.player.rect.x - self.rect.x ,self.player.rect.y - self.rect.y ]
            self.change+=0.02
            self.direction.y = math.sin(self.change)
            self.speedy = self.maxspeed

            if abs(point[0]) > self.range:
                self.rect.x += 5 * point[0]/abs(point[0])
            if abs(point[1]) > 50:
                self.rect.y += 5 * point[1]/abs(point[1])

    def attack(self):
    
        if self.timer < 0:
            self.attacking = True
            self.direction.x = self.vector[0]/self.mag  if self.mag > 0 else 0
            self.direction.y = self.vector[1]/self.mag  if self.mag > 0 else 0
            self.maxspeed = 6
            self.timer = randint(100,150)
        if self.timer < 100 and self.timer > 70:
            self.attacking = False
            self.maxspeed = randint(1,3)+self.winc["sp"]
            self.range = randint(0,50)
            self.speedx = 0
        self.timer -= 1

    def movement(self):

        self.vector = [self.player.rect.x - self.rect.x,self.player.rect.y - self.rect.y]
        self.follow()
        self.attack()
        if self.immunity > 0:
            self.speedx = 0
            self.speedy = 0 

        self.rect.x += self.speedx * self.direction.x * self.dt 
        self.rect.y += self.speedy * self.direction.y * self.dt 

    def collision(self):
        for obj in self.player.projectiles:
            if self.rect.colliderect(obj[1]) and self.immunity < 0:
                self.damage(self.player.atk_dmg)
                self.direction.x = -obj[2][0]
                self.direction.y = -obj[2][1]
                self.speedx = 15
                self.speedy = 15
                obj[4]-=1
                for i in range(4):
                    self.particles.add_particle([self.rect.centerx,self.rect.centery],4,(randint(240,255),230,230))
        if self.rect.colliderect(self.player.rect) and self.player.immunity < 0:
            if self.player.rect.y +20< self.rect.y and self.immunity < 0:
                self.damage(self.player.atk_dmg)
                self.player.direction.y = -3
                self.rect.y += 10
                
            else:
                self.player.damage(self.atk_dmg)
                for i in range(4):
                    self.particles.add_particle([self.rect.centerx,self.rect.centery],4,(randint(240,255),230,230))
                self.player.speedx += 4*-self.direction.x  
                self.player.direction.y = -5



# animation
    def get_status(self):
        direction = [self.vector[0]/self.mag ,self.vector[1]/self.mag ]  if self.mag > 0 else [0,0]

        if direction[0] <0:
            self.is_left = True
        else: self.is_left = False
        if direction[1] > 0:
            self.status = 4
        if direction[1] < 0:
            self.status = 5

    def render(self,offset):
        super().render(offset)
        self.healthbar.draw(self.screen,[self.rect.centerx-10,self.rect.centery-20]+offset)

    def update(self,scroll,dt):
        super().update(scroll,dt)
        self.movement()
        self.get_status()
        self.collision()

class SharpEnemy(Entity):
    def __init__(self,pos,screen,player,size = [16,16],inc = {}):
        super().__init__(pos,screen,size)
        self.player = player
        self.winc = inc
        # movement
        self.change = 0

        self.maxspeed = randint(1,3)+inc["sp"]
        self.speedy= 0
        self.attack_speed = 5
        self.timer = 300
        self.atk_dmg = 50+inc["ap"]
        self.attacking = False
        # animation
        self.animation = Animation_Handler(self.animspeed,"res/Animations/enemy/eye1.png",[16,16]) 

        # health and others
        self.original_maxhp = 150 +inc["hp"]
        self.maxhealth = self.original_maxhp
        self.health = self.maxhealth
        self.healthbar = HealthBar((200,200,255),self,[20,4])
        

# movement

    def follow(self):
        self.mag = math.sqrt(self.vector[0]**2 + self.vector[1]**2)
        point = [self.player.rect.x - self.rect.x ,self.player.rect.y - self.rect.y ]
        if not self.attacking:
            self.change+=0.03
            self.direction.x = math.cos(self.change)
            self.direction.y = math.sin(self.change)
        self.speedx = self.maxspeed
        self.speedy = self.maxspeed

        if abs(point[0]) > 100:
            self.rect.x += abs(point[0])/20 * point[0]/abs(point[0])
        if abs(point[1]) > 100:
            self.rect.y += abs(point[1])/20 * point[1]/abs(point[1])

    def attack(self):
    
        if self.timer < 0:
            self.attacking = True
            self.direction.x = self.vector[0]/self.mag  if self.mag > 0 else 0
            self.direction.y = self.vector[1]/self.mag  if self.mag > 0 else 0
            self.maxspeed = self.attack_speed
            self.timer = randint(100,300)
        if self.timer < 100:
            self.attacking = False
            self.maxspeed = randint(1,3)+self.winc["sp"]
        self.timer -= 1

    def movement(self):

        self.vector = [self.player.rect.x - self.rect.x,self.player.rect.y - self.rect.y]
        self.follow()
        self.attack()
        if self.immunity > 0:
            self.speedx = 0
            self.speedy = 0 

        self.rect.x += self.speedx * self.direction.x * self.dt 
        self.rect.y += self.speedy * self.direction.y * self.dt 

    def collision(self):
        for obj in self.player.projectiles:
            if self.rect.colliderect(obj[1]) and self.immunity < 0:
                self.damage(self.player.atk_dmg)
                self.direction.x = -obj[2][0]
                self.direction.y = -obj[2][1]
                self.speedx = 15
                self.speedy = 15
                obj[4]-=1
                for i in range(4):
                    self.particles.add_particle([self.rect.centerx,self.rect.centery],4,(randint(240,255),230,230))
        if self.rect.colliderect(self.player.rect) and self.player.immunity < 0:
            if self.player.rect.y +20< self.rect.y and self.immunity < 0:
                self.damage(self.player.atk_dmg)
                self.player.direction.y = -3
                self.speedy = 15
                self.direction.y = 1
                
            else:
                self.player.damage(self.atk_dmg)
                for i in range(4):
                    self.particles.add_particle([self.rect.centerx,self.rect.centery],4,(randint(240,255),230,230))
                self.player.speedx += 4*-self.direction.x  
                self.player.direction.y = -5



# animation
    def get_status(self):
        direction = [self.vector[0]/self.mag ,self.vector[1]/self.mag ]  if self.mag > 0 else [0,0]

        if direction[0] <0:
            self.is_left = True
        else: self.is_left = False
        if direction[1] > 0:
            self.status = 0 
        if direction[1] < 0:
            self.status = 1 

    def render(self,offset):
        super().render(offset)
        self.healthbar.draw(self.screen,[self.rect.centerx-10,self.rect.centery-20]+offset)

    def update(self,scroll,dt):
        super().update(scroll,dt)
        self.movement()
        self.get_status()
        self.collision()

class Shooter(Entity):
    def __init__(self,pos,screen,player,size = [16,16],inc = {}):
        super().__init__(pos,screen,size)
        self.player = player
        self.winc = inc
        # movement
        self.maxspeed = 0.8
        self.speedy= 0
        self.pos_timer = -100
        self.point = [0,0]

        self.projectiles = []
        self.proj_speed = 5+inc["sp"]
        self.timer =30
        self.atk_dmg = 50+inc["ap"]
        # animation
        self.animation = Animation_Handler(self.animspeed,"res/Animations/enemy/eye1.png",[16,16]) 

        # health and others
        self.original_maxhp = 100+inc["hp"]
        self.maxhealth = self.original_maxhp
        self.health = self.maxhealth
        self.healthbar = HealthBar((200,200,255),self,[20,4])
        

# movement


    def follow(self):
        self.mag = math.sqrt(self.vector[0]**2 + self.vector[1]**2)
        rng = 80
        if self.pos_timer <= 0:
            self.point = [randint(30,620),randint(10,300)]
            self.pos_timer = 150
        self.pos_timer -=1
        dist = (self.point[0]-self.rect.x,self.point[1]-self.rect.y)
        if abs(dist[0])> rng:
            self.speedx = self.maxspeed
            self.direction.x = dist[0]/abs(dist[0]) if abs(dist[0])> 0 else 0
        if abs(dist[1])> rng:
            self.speedy = self.maxspeed
            self.direction.y = dist[1]/abs(dist[1]) if abs(dist[1])> 0 else 0


    def attack(self):
    
        if self.timer < 0:
            img = pygame.image.load("res/projectiles/star.png")
            rect = img.get_rect(topleft = (self.rect.centerx,self.rect.centery))
            direction = (self.vector[0]/self.mag  if self.mag > 0 else 0,self.vector[1]/self.mag  if self.mag > 0 else 0)
            self.projectiles.append([img,rect,direction])
            self.timer = randint(10,20)
        self.timer -= 1
        for obj in self.projectiles:
            obj[1].x += self.proj_speed*obj[2][0] - self.scroll[0]
            obj[1].y += self.proj_speed*obj[2][1] - self.scroll[1]
            if abs(obj[1].x)>690 or abs(obj[1].y)>350:
                self.projectiles.remove(obj)
    def movement(self):

        self.vector = [self.player.rect.x - self.rect.x,self.player.rect.y - self.rect.y]
        if self.immunity < 0:
            self.follow()
            self.attack()
        if self.immunity > 0:
            self.speedx = 0
            self.speedy = 0 

        self.rect.x += self.speedx * self.direction.x * self.dt 
        self.rect.y += self.speedy * self.direction.y* self.dt 

        self.speedx = 0
        self.speedy = 0

    def collision(self):
        for obj in self.player.projectiles:
            if self.rect.colliderect(obj[1]) and self.immunity < 0:
                self.damage(self.player.atk_dmg)
                self.direction.x = -obj[2][0]
                self.direction.y = -obj[2][1]
                self.speedx = 15
                self.speedy = 15
                obj[4]-=1
                for i in range(4):
                    self.particles.add_particle([self.rect.centerx,self.rect.centery],4,(randint(240,255),230,230))
        for obj in self.projectiles:
            if self.player.rect.colliderect(obj[1]) and self.player.immunity < 0:
                self.player.damage(self.atk_dmg)
                self.player.speedx = 5
                self.player.direction.x= obj[2][0]
                self.player.direction.y = 5 * obj[2][1]
            
                for i in range(4):
                    self.particles.add_particle([self.player.rect.centerx,self.player.rect.centery],4,(randint(240,255),230,230))

            for pobj in self.player.projectiles:
                if obj[1].colliderect(pobj[1]) and obj in self.projectiles and pobj in self.player.projectiles:
                    self.projectiles.remove(obj)
                    self.player.projectiles.remove(pobj)


# animation
    def get_status(self):
        direction = [self.vector[0]/self.mag ,self.vector[1]/self.mag ]  if self.mag > 0 else [0,0]

        if direction[0] <0:
            self.is_left = True
        else: self.is_left = False
        self.status = 3 if self.timer > 60 else 2

    def render(self,offset):
        super().render(offset)
        self.healthbar.draw(self.screen,[self.rect.centerx-10,self.rect.centery-20]+offset)
        for obj in self.projectiles:
            self.screen.blit(obj[0],obj[1].topleft+offset)

    def update(self,scroll,dt):
        super().update(scroll,dt)
        self.scroll = scroll
        self.movement()
        self.get_status()
        self.collision()

# BOSS 


class SharpBoss(Entity):
    def __init__(self,pos,screen,player,size = [80,160]):
        super().__init__(pos,screen,size)
        self.player = player
        # movement
        self.change = 0

        self.maxspeed = 3
        self.speedy= 0
        self.attack_speed = 8
        self.timer = 300
        self.atk_dmg = 150
        self.attacking = False
        # animation
        self.animation = Animation_Handler(self.animspeed,"res/Animations/enemy/bosses.png",[80,160]) 

        # health and others
        self.maxhealth = 1500
        self.health = self.maxhealth
        self.healthbar = HealthBar((200,200,255),self,[100,15])
        self.shielded = True
        self.shield_dmg = 0
        self.shield_timer = 0
        

# movement

    def follow(self):
        self.mag = math.sqrt(self.vector[0]**2 + self.vector[1]**2)
        point = [self.player.rect.x - self.rect.x ,self.player.rect.y - self.rect.y ]
        if not self.attacking:
            self.change+=0.03
            self.direction.x = math.cos(self.change)
            self.direction.y = math.sin(self.change)
        self.speedx = self.maxspeed
        self.speedy = self.maxspeed

        if abs(point[0]) > 200:
            self.rect.x += abs(point[0])/20 * point[0]/abs(point[0])
        if abs(point[1]) > 200:
            self.rect.y += abs(point[1])/20 * point[1]/abs(point[1])

    def attack(self):
    
        if self.timer < 0:
            self.attacking = True
            self.direction.x = self.vector[0]/self.mag  if self.mag > 0 else 0
            self.direction.y = self.vector[1]/self.mag  if self.mag > 0 else 0
            self.maxspeed = self.attack_speed
            self.timer = randint(100,300)
        if self.timer < 100:
            self.attacking = False
            self.maxspeed = randint(1,3)
        self.timer -= 1

    def shield(self):
        if self.shielded:
            self.shield_dmg+= self.maxhealth-self.health
            self.health = self.maxhealth
            self.healthbar.color = (100,200,100)
            if self.shield_dmg > 1000:
                self.shielded = False
                self.shield_timer = 600
                self.shield_dmg = 0
        else:self.healthbar.color = (200,200,255)
        self.shielded = True if self.shield_timer < 0 else False
        self.shield_timer -=1
    def movement(self):

        self.vector = [self.player.rect.x - self.rect.x,self.player.rect.y - self.rect.y]
        self.follow()
        self.attack()
        if self.immunity > 0:
            self.speedx = 0
            self.speedy = 0 

        self.rect.x += self.speedx * self.direction.x * self.dt 
        self.rect.y += self.speedy * self.direction.y * self.dt 

    def collision(self):
        for obj in self.player.projectiles:
            if self.rect.colliderect(obj[1]) and self.immunity < 0:
                self.damage(self.player.atk_dmg)
                self.direction.x = -obj[2][0]
                self.direction.y = -obj[2][1]
                self.speedx = 15
                self.speedy = 15
                obj[4]-=1
                for i in range(4):
                    self.particles.add_particle([self.rect.centerx,self.rect.centery],4,(randint(240,255),230,230))
        if self.rect.colliderect(self.player.rect) and self.player.immunity < 0:
            if self.player.rect.y +20< self.rect.y and self.immunity < 0:
                self.damage(self.player.atk_dmg)
                self.player.direction.y = -3
                self.speedy = 15
                self.direction.y = 1
                
            else:
                self.player.damage(self.atk_dmg)
                for i in range(4):
                    self.particles.add_particle([self.rect.centerx,self.rect.centery],4,(randint(240,255),230,230))
                self.player.speedx += 4*-self.direction.x  
                self.player.direction.y = -5



# animation
    def get_status(self):
        direction = [self.vector[0]/self.mag ,self.vector[1]/self.mag ]  if self.mag > 0 else [0,0]

        if direction[0] <0:
            self.is_left = True
        else: self.is_left = False

    def render(self,offset):
        super().render(offset)
        self.healthbar.draw(self.screen,self.rect.topleft+offset-(20,40))
    def update(self,scroll,dt):
        super().update(scroll,dt)
        self.movement()
        self.get_status()
        self.collision()
        self.shield()

class ShooterBoss(Entity):
    def __init__(self,pos,screen,player,size = [16,16],inc = {}):
        super().__init__(pos,screen,size)
        self.player = player
        self.winc = inc
        # movement
        self.maxspeed = 0.8
        self.speedy= 0
        self.pos_timer = -100
        self.point = [0,0]

        self.projectiles = []
        self.proj_speed = 5+inc["sp"]
        self.timer = 100
        self.atk_dmg = 50+inc["ap"]
        # animation
        self.animation = Animation_Handler(self.animspeed,"res/Animations/enemy/eye1.png",[16,16]) 

        # health and others
        self.original_maxhp = 100+inc["hp"]
        self.maxhealth = self.original_maxhp
        self.health = self.maxhealth
        self.healthbar = HealthBar((200,200,255),self,[20,4])
        

# movement


    def follow(self):
        self.mag = math.sqrt(self.vector[0]**2 + self.vector[1]**2)
        rng = 80
        if self.pos_timer <= 0:
            self.point = [randint(30,620),randint(10,300)]
            self.pos_timer = 150
        self.pos_timer -=1
        dist = (self.point[0]-self.rect.x,self.point[1]-self.rect.y)
        if abs(dist[0])> rng:
            self.speedx = self.maxspeed
            self.direction.x = dist[0]/abs(dist[0]) if abs(dist[0])> 0 else 0
        if abs(dist[1])> rng:
            self.speedy = self.maxspeed
            self.direction.y = dist[1]/abs(dist[1]) if abs(dist[1])> 0 else 0


    def attack(self):
    
        if self.timer < 0:
            img = pygame.image.load("res/projectiles/star.png")
            rect = img.get_rect(topleft = (self.rect.centerx,self.rect.centery))
            direction = (self.vector[0]/self.mag  if self.mag > 0 else 0,self.vector[1]/self.mag  if self.mag > 0 else 0)
            self.projectiles.append([img,rect,direction])
            self.timer = randint(10,20)
        self.timer -= 1
        for obj in self.projectiles:
            obj[1].x += self.proj_speed*obj[2][0] - self.scroll[0]
            obj[1].y += self.proj_speed*obj[2][1] - self.scroll[1]
            if abs(obj[1].x)>700 or abs(obj[1].y)>500:
                self.projectiles.remove(obj)
    def movement(self):

        self.vector = [self.player.rect.x - self.rect.x,self.player.rect.y - self.rect.y]
        if self.immunity < 0:
            self.follow()
            self.attack()
        if self.immunity > 0:
            self.speedx = 0
            self.speedy = 0 

        self.rect.x += self.speedx * self.direction.x * self.dt 
        self.rect.y += self.speedy * self.direction.y* self.dt 

        self.speedx = 0
        self.speedy = 0

    def collision(self):
        for obj in self.player.projectiles:
            if self.rect.colliderect(obj[1]) and self.immunity < 0:
                self.damage(self.player.atk_dmg)
                self.direction.x = -obj[2][0]
                self.direction.y = -obj[2][1]
                self.speedx = 15
                self.speedy = 15
                obj[4]-=1
                for i in range(4):
                    self.particles.add_particle([self.rect.centerx,self.rect.centery],4,(randint(240,255),230,230))
        for obj in self.projectiles:
            if self.player.rect.colliderect(obj[1]) and self.player.immunity < 0:
                self.player.damage(self.atk_dmg)
                self.player.speedx = 5
                self.player.direction.x= obj[2][0]
                self.player.direction.y = 5 * obj[2][1]
            
                for i in range(4):
                    self.particles.add_particle([self.player.rect.centerx,self.player.rect.centery],4,(randint(240,255),230,230))

            for pobj in self.player.projectiles:
                if obj[1].colliderect(pobj[1]) and obj in self.projectiles and pobj in self.player.projectiles:
                    self.projectiles.remove(obj)
                    self.player.projectiles.remove(pobj)


# animation
    def get_status(self):
        direction = [self.vector[0]/self.mag ,self.vector[1]/self.mag ]  if self.mag > 0 else [0,0]

        if direction[0] <0:
            self.is_left = True
        else: self.is_left = False
        self.status = 3 if self.timer > 60 else 2

    def render(self,offset):
        super().render(offset)
        self.healthbar.draw(self.screen,[self.rect.centerx-10,self.rect.centery-20]+offset)
        for obj in self.projectiles:
            self.screen.blit(obj[0],obj[1].topleft+offset)

    def update(self,scroll,dt):
        super().update(scroll,dt)
        self.scroll = scroll
        self.movement()
        self.get_status()
        self.collision()

