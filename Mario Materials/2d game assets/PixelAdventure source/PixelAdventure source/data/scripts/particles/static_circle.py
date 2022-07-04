import pygame

from data.engine.VFX.particle import Particle


class StaticCircle(Particle):
    def __init__(self, manager, position, color, radius, frames=30):
        if isinstance(color, pygame.Color):
            self.COLOR = color

        else:
            self.COLOR = pygame.Color(color[0], color[1], color[2])

        super().__init__(manager, position, layer=-1)
        self.FRAMES = frames
        self.INITIAL_RADIUS = radius
        self.radius = radius
        self.life = 1

    def update(self, **kwargs):
        self.life -= (1 / self.FRAMES) * kwargs["dt"]
        if self.life <= 0:
            self.destroy()
        else:
            self.radius = int(self.life * self.INITIAL_RADIUS)

    def draw(self, surface, offset=(0, 0)):
        center = int(self.position.x - offset[0]), int(self.position.y - offset[1])

        pygame.draw.circle(
            surface,
            (0, 0, 0),
            center,
            self.radius + 2
        )

        pygame.draw.circle(
            surface,
            self.COLOR,
            center,
            self.radius
        )