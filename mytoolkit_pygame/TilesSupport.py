import pygame
from sys import path
from res.levels import levels
from settings import *
from entities.enemies import *
#### utils #####


def get_image(image_source,framex,size=TILE_CONT,layery=0):
    fullimage = pygame.image.load(image_source)
    image = pygame.Surface((size[0],size[1]))
    lengthx = fullimage.get_width()/size[0] -1
    if framex > lengthx :
        layery += int(framex//lengthx)
        framex = int(framex%lengthx)-layery

    image.blit(fullimage,(framex*-size[0],layery*-size[1],size[0],size[1]))
    image.set_colorkey((0,0,0))

    return image
def render_text(screen,text,pos,fonts,size):
    font = pygame.font.Font(fonts,size)
    text = font.render(text,False,(50,50,50))
    rect = text.get_rect(center = pos)
    screen.blit(text,rect)
class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,group,framex = None,tile_id = None,imagesource=None,tile_size= TILE_CONT):
        super().__init__(group)
        self.pos = pos
        # image , tile type and rect 
        # with tile type all tiles can be in one group , is that optimal, absolutely not 
        if imagesource != None:
            self.image = get_image(imagesource,framex,size = tile_size)
        else: 
            self.image = pygame.Surface(tile_size)
            self.image.fill((0,0,0))
        self.tile_type = tile_id
        self.rect = self.image.get_frect(topleft=(pos))
        
        # position in level array
        self.frame = framex

    def draw(self,screen,offset):
        pos = self.rect.topleft + offset
        screen.blit(self.image,pos)   
    def update(self,scroll):
        self.rect.x -= scroll[0] 
        self.rect.y -= scroll[1] 
class Buttons ():
    def __init__(self,pos,screen,scale,imagesource) :
        self.screen = screen
        self.playimage, self.exitimage = pygame.transform.scale_by(get_image(imagesource,5,size=[40,30]),scale),pygame.transform.scale_by(get_image(imagesource,6,size=[40,30]),scale)
        self.playrect, self.exitrect = self.playimage.get_frect(center = pos[0]),self.playimage.get_frect(center = pos[1])
        self.collide = False

    def render(self):
        
        self.screen.blit(self.playimage,self.playrect)
        self.screen.blit(self.exitimage,self.exitrect)


    def update(self,click):
        # check mouse collision

        if self.playrect.collidepoint(pygame.mouse.get_pos()):
            if click:
                return "play"
            else: return ""
        if self.exitrect.collidepoint(pygame.mouse.get_pos()):
            if click:
                return "exit"
            else :return ""
        return ""



#### tilemanager #####
        


class TILE_SUPPORT():
    def __init__(self,game) :
        self.sprites = pygame.sprite.Group()
        self.game = game
        self.map = levels(current_level)
        self.set_world()

        
    
    def set_world(self):
        size = 16
        self.load_sprites(self.map,"res/levels/tiles/tiles.png")
        self.playpos = self.tile_sieve(1,self.sprites)
        for rect in self.playpos:
            self.game.player.rect.topleft = (rect.x,rect.y)
        self.platbs = self.tile_sieve(0,self.sprites)

    # used to spawn maps

    def load_sprites(self,Array,imres=None):
        for row_index,row in enumerate(Array):
            for col_index,col in enumerate(row):
                x = col_index * TILE_CONT[0]
                y = row_index * TILE_CONT[1]
                if col > -1: tile_id = 0
                if col == 99:tile_id = 1
                if col>-1:
                    tiles = Tile((x,y),self.sprites,framex=col,tile_id=tile_id,imagesource=imres)
    
            
    # collision checker / returns a list of every hit object in the group
    
    def tile_sieve(self,tile_id,group):
        tyle_list = []
        for sprite in group.sprites():
            if sprite.tile_type == tile_id:
                tyle_list.append(sprite.rect)
        return tyle_list
    
    def platformer_physics(self,entities= None):
        self.game.player.applygravity()
        for rect in self.platbs:
            if rect.colliderect(self.game.player.rect):
                if self.game.player.direction.y > 0: 
                    self.game.player.rect.bottom = rect.top
                    self.game.player.direction.y = 0
                    
                    self.game.player.on_ground = True
                    self.game.player.collisions["down"] = 1
                elif self.game.player.direction.y < 0:
                    self.game.player.rect.top = rect.bottom
                    self.game.player.direction.y = 0
                    self.game.player.collisions["up"] = 1
        if self.game.player.direction.y > self.game.player.gravity or self.game.player.direction.y < 0:
            self.game.player.on_ground = False

        self.game.player.rect.x += self.game.player.direction.x * self.game.player.speedx * self.dt 

        for rect in self.platbs:
            if rect.colliderect(self.game.player.rect):
                if self.game.player.direction.x < 0: 
                    self.game.player.rect.left = rect.right
                    self.game.player.collisions["left"] = 1
                elif self.game.player.direction.x > 0:
                    self.game.player.rect.right = rect.left
                    self.game.player.collisions["right"] = 1

        # for ent in entities:
        #     if entities != None:   
        #             for rect in self.platbs:
        #                 if rect.colliderect(ent.rect):
        #                     if ent.direction.y > 0: 
        #                         ent.bottom = rect.top
        #                         ent.direction.y = 0
                                
        #                         ent.on_ground = True
        #                         ent.collisions["down"] = 1
        #                     elif ent.direction.y < 0:
        #                         ent.rect.top = rect.bottom
        #                         ent.direction.y = 0
        #                         ent.collisions["up"] = 1
        #             if ent.direction.y > self.game.player.gravity or ent.direction.y < 0:
        #                 ent.on_ground = False
        #             ent.rect.x += ent.direction.x * ent.speedx * self.dt 

        #             for rect in self.platbs:
        #                 if rect.colliderect(ent.rect):
        #                     if ent.direction.x < 0: 
        #                         ent.rect.left = rect.right
        #                         ent.collisions["left"] = 1
        #                     elif ent.direction.x > 0:
        #                         ent.rect.right = rect.left
        #                         ent.collisions["right"] = 1
                        



    def render(self,screen,offset):
        for sprite in self.sprites:
            sprite.draw(screen,offset)


    def update(self,scroll,dt,entities):
        self.dt = dt * self.game.player.inc if dt > 0 else 1
        self.sprites.update(scroll)
        self.platformer_physics(entities)
