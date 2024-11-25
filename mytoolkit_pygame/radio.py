import pygame
from time import time
from random import randint

class Radio():
    def __init__(self,Musics = list,SoundEffects = dict) :
        self.SOUNDEFFECTS = SoundEffects
        self.MUSICS = Musics
        self.MUSICchannel = pygame.mixer.Channel(0)
        self.MUSICchannel.set_volume(0.1)
        self.EFECTSchannel = pygame.mixer.Channel(1)
        self.EFECTSchannel.set_volume(0.2)

        self.current_time = time()
        self.start_time = self.current_time

        self.randmusic = randint(0,len(self.MUSICS)-1)

        self.MUSICchannel.play(self.MUSICS[self.randmusic])

    def play_music(self):
        self.current_time = time()
        if self.MUSICS[self.randmusic].get_length() - (self.current_time-self.start_time) < -3:
            self.start_time = time()
            self.randmusic = randint(0,len(self.MUSICS)-1)
            self.MUSICchannel.play(self.MUSICS[self.randmusic])

    def play_effect(self,effect_name):
        self.EFECTSchannel.play(self.SOUNDEFFECTS[effect_name])