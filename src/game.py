import pygame,sys
sys.path.append("mytoolkit_pygame")

from mytoolkit_pygame.TilesSupport import TILE_SUPPORT,get_image
from entities.waveplay import WavePlay
from entities.player import player
from settings import *

class GAME():
    def __init__(self,display):

        self.running = True

        # screen
        self.display = display

        size = (1280,640)
        self.internal_screen = pygame.Surface(size,pygame.SRCALPHA)
        self.internal_screen_rect = self.internal_screen.get_rect(center = (SCREEN_DIMENSIONS[0]//2,SCREEN_DIMENSIONS[1]//2))
        self.size_vector = pygame.math.Vector2(size)
        self.scale = 1
        self.offset = pygame.math.Vector2((size[0]//2-SCREEN_DIMENSIONS[0]//2,size[1]//2-SCREEN_DIMENSIONS[1]//2))
        # basic scroll camera 
        self.scroll = (0,0)
        self.camera_entities = []
        
        # player
        self.player = player((30,30),self.internal_screen,self.display)
        self.camera_entities.append(self.player.rect)

        # level/world
        self.TileManager = TILE_SUPPORT(self)

        # enemies
        self.waveplay = WavePlay(self.player,self.internal_screen,self,display)



#camera  
        
    def getscroll(self):
        scroll = [0,0]
        scroll[0] += self.player.rect.x - scroll[0] - SCREEN_DIMENSIONS[0]/2
        scroll[1] += self.player.rect.y - scroll[1] - SCREEN_DIMENSIONS[1]/2
        return scroll
    def camera(self):
        self.scroll = self.getscroll()
        self.scroll[0] = self.scroll[0]//10
        self.scroll[1] = self.scroll[1]//5
        for rect in self.camera_entities:
            rect.x -= self.scroll[0]
            rect.y -= self.scroll[1]

# events
    def event_handler(self):
        self.click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player.jump = True
                if event.key == pygame.K_SPACE and self.waveplay.wait:
                    self.waveplay.timer = 0
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.click = True
                if not self.waveplay.carding:
                    self.player.attacking = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.player.dash = True
        

# sprites
    
    def render(self):

        scaled_screen = pygame.transform.scale(self.internal_screen,self.size_vector*self.scale)
        rect = scaled_screen.get_rect(center =(SCREEN_DIMENSIONS[0]//2,SCREEN_DIMENSIONS[1]//2))
        self.display.blit(scaled_screen,rect)
        self.internal_screen.fill((80, 80, 80))

        self.TileManager.render(self.internal_screen,self.offset)
        self.waveplay.render(self.offset)
        self.player.render(self.offset)
    def update(self,dt):
        self.event_handler()
        self.camera()

        self.TileManager.update(self.scroll,dt,self.waveplay.entities)
        self.waveplay.update(self.scroll,dt)
        self.player.update(self.scroll,dt)