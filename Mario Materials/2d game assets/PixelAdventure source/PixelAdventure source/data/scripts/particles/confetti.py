import math
from math import sin, cos
from random import randint, random

import pygame

from data.engine.VFX.particle import Particle
from data.engine.math.vector import Vector

COLORS = [
    (108, 217, 241, 255),
    (164, 204, 66, 255),
    (247, 236, 138, 255),
    (241, 139, 114, 255),
    (248, 156, 192, 255),
    (242, 188, 126, 255)
]
WHITE = pygame.Color(255, 255, 255)

class Confetti(Particle):
    def __init__(self, manager, position):
        super().__init__(manager, position, layer=11)
        c = COLORS[randint(0, len(COLORS) - 1)]
        self.COLOR = pygame.Color(c[0], c[1], c[2])
        self.OUTLINE = self.COLOR.lerp(WHITE, 0.3)
        self.rotation = random() * math.pi * 2
        self.frequency = random()
        self.size = randint(5, 15)

        self.velocity = Vector.random(random() * 5)

    def update(self, **kwargs):
        self.velocity.y += 0.1 * kwargs["dt"]
        self.rotation += sin(self.frequency * self.rotation) * kwargs["dt"]
        self.position += self.velocity * kwargs["dt"]
        self.size -= 0.1 * kwargs["dt"]

        if self.size <= 0:
            self.destroy()

    def _get_points(self):
        return [
            Vector.from_direction(self.rotation + math.pi * .5) * self.size,
            Vector.from_direction(self.rotation + math.pi) * self.size,
            Vector.from_direction(self.rotation + math.pi * 1.5) * self.size,
            Vector.from_direction(self.rotation) * self.size,
        ]

    def draw(self, surface, offset=(0, 0)):
        pos = self.position - offset
        points = [point + pos for point in self._get_points()]
        pygame.draw.polygon(
            surface,
            self.COLOR,
            points
        )
        pygame.draw.polygon(
            surface,
            self.OUTLINE,
            points,
            2
        )
