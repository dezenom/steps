import pygame as pg
import sys
from game import GAME
from settings import clock,FPS

def run(screen,state_manager):
    game = GAME(screen)

    while game.running:

        screen.fill((80, 80, 80))
        Dt = clock.tick(FPS)/1000.0
        if Dt > 0.5:
            Dt = 0
        
        game.update(Dt)
        game.render()
        pg.display.flip()