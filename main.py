import pygame,sys
pygame.init()
pygame.mixer.init()
sys.path.append('src')

from src.settings import *
import src.states.playing as play



screen = pygame.display.set_mode(SCREEN_DIMENSIONS,pygame.SCALED)

state_runs = {"game":play.run}

state_runs['game'](screen,state_runs)
