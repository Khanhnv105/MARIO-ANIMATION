from random import random

import pygame

from data.engine.UI.elements.pixelart.pixelart_font import PixelartFont
from data.engine.VFX.particle import Particle
from data.engine.math.vector import Vector


class TextParticle(Particle):

    def __init__(self, text, manager, position, color="White", frames=50):
        super().__init__(manager, position, 11)
        font = PixelartFont(text, 3, f"data/Assets/Free/Menu/Text/Text ({color}) (8x10).png", 8, 10)
        self.IMAGE = font.copy()
        self.velocity = Vector((random() - 0.5) * 6, -3)
        self.life = 1
        self.FRAMES = frames

    def update(self, **kwargs):
        self.life -= (1 / self.FRAMES) * kwargs["dt"]
        if self.life <= 0:
            self.destroy()
        self.velocity.y += 0.2 * kwargs["dt"]
        self.position += self.velocity * kwargs["dt"]

    def draw(self, surface, offset=(0, 0)):
        image = pygame.transform.scale(
            self.IMAGE,
            (
                int(self.IMAGE.get_width() * self.life),
                int(self.IMAGE.get_height() * self.life)
            )
        )
        surface.blit(
            image,
            (
                self.position.x - image.get_width() // 2 - offset[0],
                self.position.y - image.get_height() // 2 - offset[1]
            )
        )
