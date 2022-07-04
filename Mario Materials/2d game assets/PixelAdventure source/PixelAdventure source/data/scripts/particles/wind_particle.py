from random import random, randint

from data.engine.VFX.particle import Particle
from pygame.draw import line


class WindParticle(Particle):

    def __init__(self, manager, position, direction_vector, frames=50, life_distance=None):

        """
        life_distance: Es la distancia que va a recorrer la particula hasta morir
        """

        super().__init__(manager, position)

        rand = random() + 1
        self.FRAMES = frames
        self.INITIAL_LENGTH = rand * 20
        self.velocity = rand * 4 * direction_vector
        self.position.y -= self.INITIAL_LENGTH

        if life_distance:
            """Se anula el parametro de frames"""
            self.FRAMES = (life_distance - self.INITIAL_LENGTH) / self.velocity.get_length()

        self.length = self.INITIAL_LENGTH
        self.life = 1
        self.direction = direction_vector

        c = randint(220, 255)
        self.COLOR = c, c, c

    def update(self, **kwargs):
        self.position += self.velocity * kwargs["dt"]
        self.life -= (1 / self.FRAMES) * kwargs["dt"]

        if self.life <= 0:
            self.destroy()

        self.length = self.INITIAL_LENGTH * self.life

    def draw(self, surface, offset=(0, 0)):
        line(
            surface,
            (0, 0, 0),
            self.position - offset,
            self.position - self.direction * self.length - offset,
            6
        )
        line(
            surface,
            self.COLOR,
            self.position - offset,
            self.position - self.direction * self.length - offset,
            5
        )
