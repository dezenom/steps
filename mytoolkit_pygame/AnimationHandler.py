import pygame
from TilesSupport import get_image

class Animation_Handler():
    def __init__(self,animation_speed, spritesheet, framesize) :
        self.SPRITESHEET = spritesheet
        # animation control
        self.animation_speed = animation_speed
        self.current_index = 0
        self.FRAME_SIZE = framesize

    def animation(self,status,left,down=False):
        self.current_index+=self.animation_speed
        if self.current_index >= 11*5:
            self.current_index = 0
        
        image = get_image(self.SPRITESHEET,self.current_index//5,size=self.FRAME_SIZE,layery=status)
        rect = image.get_bounding_rect()
        if (rect.w == 0 and rect.h == 0):
            self.current_index = 0
            image = get_image(self.SPRITESHEET,self.current_index//5,size=self.FRAME_SIZE,layery=status)

        image = pygame.transform.flip(image,left,down)    


        return image
    
