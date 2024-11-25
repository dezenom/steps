import pygame
from entities.enemies import *
from random import randint,choices
from mytoolkit_pygame.TilesSupport import render_text,get_image


class WavePlay():
    def __init__(self,player,screen,game,display):
        self.player = player
        self.screen = screen
        self.display = display
        self.game = game

        self.wave_no = 1
        self.wavelimit = 2 * self.wave_no
        self.entitylimit = 6
        self.timer = 0
        self.all_spawned = 0
        self.wait = False
        self.enemies = [SharpEnemy,Shooter,lazerEnemy]
        self.entities = []
        self.inc = {"hp": 0,"ap": 0,"sp":0}
        # self.spawn(SharpBoss,(randint(-200,800),randint(-200,800)),self.screen,True,1)

        self.time = 3840

        # cards
        self.carding = False
        self.used_cards = 0
        self.og_cardPos = []
        self.cards = self.get_cards("res/levels/tiles/dek.png",10)
        self.indexes = []
        for i in range(len(self.cards)-1):
            self.indexes.append(i)
        self.av_cards = []

        for card in self.cards:
            self.og_cardPos.append((card[1].x,card[1].y))

    def spawner(self):
        self.entitylimit = 6 + 2* self.wave_no//10
        if self.all_spawned < self.wavelimit:
            if len(self.entities)<self.entitylimit and self.timer < 0:
                self.game.scale = 0.8
                self.wait = False
                self.spawn(choices(self.enemies,[50,15,35],k=1)[0],(randint(-200,800),randint(-200,800)),self.screen,False)
                self.all_spawned +=1
                self.timer = 40
                if self.wave_no%10 == 0 and self.all_spawned== self.wavelimit:
                    self.spawn(SharpBoss,(0,0),self.screen,True,1)
                    self.game.scale = 0.6




        if self.all_spawned >= self.wavelimit and len(self.entities)==0:
            self.game.scale = 1
            self.time = 3840
            self.all_spawned = 0
            self.wave_no += 1
            self.timer = 1200
            self.wait = True
            self.wavelimit = 2 * self.wave_no
            self.carding = True
            # 0-damage, 1-health, 2-pierce, 3-charge, 4-add, 5-speed, 6-large, 7-control, 8-jump, 9-dash 
            self.av_cards = list(set(choices([0,1,2,3,4,5,6,7,8,9],[200,400,0,1000,200,100,50,150,0,100],k=3)))
            if len(self.av_cards) < 3:
                self.av_cards.append(2)
                if len(self.av_cards)<3:
                    self.av_cards.append(8)
        if self.wait :
            self.player.health += 2 if self.player.health<self.player.maxhealth-5 else 0
        self.timer -= 1

        
# inc

    
    def get_cards(self,imgsource,no):
        cards = []
        for i in range(no):
            img = get_image(imgsource,i,(80,100))
            img.set_alpha(128)
            rect = img.get_rect(center = (self.display.get_width()/2,self.display.get_height()-80))
            if i == 2: rect.x = rect.x -20
            cards.append([img,rect,i,1])
        return cards

    def upgrades(self):

        def render():
            for i,card in enumerate(self.av_cards):
                self.cards[card][1].x = self.og_cardPos[i][0] +110 - i*110 if not len(self.av_cards) ==1 else self.cards[card][1].x
                self.display.blit(pygame.transform.scale_by(pygame.transform.rotate(self.cards[card][0],-10+10*i),self.cards[card][3]),self.cards[card][1])

        def update():
            for i,card in enumerate(self.av_cards):
                if self.cards[card][1].collidepoint(pygame.mouse.get_pos()):
                    self.cards[card][3] = 1.5
                    self.cards[card][1] = pygame.transform.scale_by(self.cards[card][0],self.cards[card][3]).get_rect()
                    self.cards[card][1].x = self.og_cardPos[i][0] -20
                    self.cards[card][1].y = self.og_cardPos[i][1] -40
                    if self.game.click:
                        self.inc["hp"]+= randint(10,80)/5 if self.inc["hp"] < 2000 else 0
                        self.inc["ap"]+= randint(10,30)/3 if self.inc["ap"] < 200 else 0
                        self.inc["sp"]+= randint(1,3)/10 if self.inc["sp"] < 3 else 0
                        self.player.increments[card]()
                        self.av_cards.remove(card)
                        self.used_cards +=1
                        if self.used_cards==2:
                            self.carding = False
                            self.used_cards = 0
                else: 
                    self.cards[card][3] = 1
                    self.cards[card][1] = pygame.transform.scale_by(self.cards[card][0],self.cards[card][3]).get_rect()
                    self.cards[card][1].x = self.og_cardPos[i][0]
                    self.cards[card][1].y = self.og_cardPos[i][1]
        if self.carding:
            update()
            render()



    def spawn(self, enemy ,pos , screen,boss,num=1):
        if not boss:self.entities.append(enemy(pos,screen,self.player,inc = self.inc))
        if boss:
            for i in range(num):
                pos = (randint(-200,800),randint(-200,800))
                self.entities.append(enemy(pos,screen,self.player))
    def despawn(self):
        for entity in self.entities:
            if entity.health <= 0:
                self.entities.remove(entity)

    def render(self,offset):
        for entity in self.entities:
            entity.render(offset)

        render_text(self.display,f"time {self.time//60}",[self.display.get_width()-80,20],
                "res/fonts/Daydream.ttf",13)
        
        if self.wait:
            render_text(self.display,f"NEXT WAVE IN  {self.timer//60+1}",[self.display.get_width()/2,20],
                    "res/fonts/Daydream.ttf",13)
            render_text(self.display,f"space to skip",[self.display.get_width()/2,50],
                    "res/fonts/Daydream.ttf",8)
        else:  render_text(self.display,f"WAVE  {self.wave_no}",[self.display.get_width()/2,20],
                    "res/fonts/Daydream.ttf",20)
        self.upgrades()
    
    def update(self,scroll,dt):
        for entity in self.entities:
            entity.update(scroll,dt)
        self.despawn()
        self.spawner()
        self.time -= 1 if not self.wait else 0