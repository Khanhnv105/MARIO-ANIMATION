from random import randint

import pygame

from data.engine.VFX.particle import Particle
from data.engine.math.vector import Vector


class ColoredParticle(Particle):
    """
    Circulo (preferentemente pequeño) que
    disminuye su tamañ de forma lineal ademas
    tiene compatiblilidad con interpolacion
    lineal de colores
    """

    def __init__(
            self,
            manager,
            position,
            velocity,
            color1,
            color2=None,
            min_radius=3,
            max_radius=10,
            frames=100
    ):
        super().__init__(manager, position, layer=3)
        self.velocity = Vector(velocity[0], velocity[1])
        self.radius = randint(min_radius, max_radius)
        self.START_RADIUS = self.radius
        self.START_COLOR = color1
        self.END_COLOR = color1 if not color2 else color2
        self.FRAMES = frames
        self.color = self.START_COLOR
        self.life = 1

    def update(self, **kwargs):
        self.life -= (1 / self.FRAMES) * kwargs["dt"]
        self.velocity.y += 0.2 * kwargs["dt"]
        self.position += self.velocity * kwargs["dt"]
        self.radius = self.START_RADIUS * self.life
        if self.radius <= 0:
            self.destroy()
        else:
            self.color = self.START_COLOR.lerp(self.END_COLOR, self.radius / self.START_RADIUS)

    def draw(self, surface, offset=(0, 0)):
        center = (
            self.position.x - offset[0],
            self.position.y - offset[1]
        )
        radius = int(self.radius)

        pygame.draw.circle(
            surface,
            (0, 0, 0),
            center,
            radius + 2
        )

        pygame.draw.circle(
            surface,
            self.color,
            center,
            radius
        )

    def _delay(self):
        self.time = pygame.time.get_ticks() + self.DELAY
