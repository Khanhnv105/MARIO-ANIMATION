
import pygame


class Music:

    def __init__(self, volume=1):

        self.playing = False
        self.tracks = None
        self.index = 0
        pygame.mixer.music.set_volume(volume)

    def load_tracks(self, tracks_path):
        self.tracks = tracks_path

    def play(self, name=None):
        if name is None:
            name = self.tracks[self.index]
        pygame.mixer.music.load(f"{name}")
        pygame.mixer.music.play()
        self.playing = True

    def fade(self, ms=500):
        pygame.mixer.music.fadeout(ms)

    def pause(self):
        pygame.mixer.music.stop()
        self.playing = False

    def unpause(self):
        pygame.mixer.music.unpause()
        self.playing = True

    def fade_in(self, ms=500):
        pygame.mixer.music.set_volume(1)

    def next(self):
        self.index += 1
        if self.index > len(self.tracks) - 1:
            self.index = 0
        self.play()

    def update(self, **kwargs):

        if not self.playing:
            return

        if not pygame.mixer.music.get_busy():
            self.next()
