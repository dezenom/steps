import pygame
from random import randint

class particle_system():
    def __init__(self) :
        self.particles = []
    def add_particle(self,pos,radius,colour):
        radius = radius
        direction = [randint(-5,5),randint(-5,5)]
        particle = [pos,radius,direction,colour]
        self.particles.append (particle)
    def emit(self,screen,offset):
        if self.particles:
            self.delete()
            for particle in self.particles:
                particle[0][0] += particle[2][0]
                particle[0][1] += particle[2][1]
                particle[2][1] += 1.3
                particle[1] -= 0.2
                pygame.draw.circle(screen, particle[3],particle[0]+offset,particle[1])
        self.delete()
    def delete(self):
        particle = [particle for particle in self.particles if particle[1]>0]
        self.particles = particle