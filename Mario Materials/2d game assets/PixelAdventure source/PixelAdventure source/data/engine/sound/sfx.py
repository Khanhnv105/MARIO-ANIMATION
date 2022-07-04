import os

import pygame


class SFX:
    def __init__(self, folder, volume=1):
        self.sounds = {}
        for name in os.listdir(folder):
            path = folder + f"/{name}"
            sound = pygame.mixer.Sound(path)
            self.sounds[name] = sound

        self.volume = volume
        self.off = False
        self.set_volume(volume)

    def turn_off(self):
        self.off = True

    def turn_on(self):
        self.off = False

    def set_volume(self, volume: float):
        self.volume = volume
        for sound_name in self.sounds:
            self.sounds[sound_name].set_volume(self.volume)

    def play(self, name):
        if not self.off:
            self.sounds[name].play()
