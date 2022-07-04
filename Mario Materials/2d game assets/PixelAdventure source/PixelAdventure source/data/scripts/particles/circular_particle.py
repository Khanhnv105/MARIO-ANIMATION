import pygame

from data.engine.VFX.particle import Particle


class CircularParticle(Particle):

    """
    Particula que inicialmente es un circulo pequeño
    con un grosor alto y a medida que aumenta el
    radio el grosor disminuye.
    Ademas tiene compatibilidad con interpolacion
    lineal de colores
    """

    def __init__(
            self,
            manager,
            position,
            radius,
            color1,
            color2=None,
            thickness=20,
            frames=30,
            filled=False
    ):
        super().__init__(manager, position, layer=3)

        self.INITIAL_RADIUS = radius
        self.INITIAL_THICKNESS = thickness
        self.FRAMES = frames
        self.START_COLOR = pygame.Color(color1[0], color1[1], color1[2])
        self.END_COLOR = pygame.Color(color2[0], color2[1], color2[2]) if color2 else self.START_COLOR
        self.FILLED = filled

        self.radius = radius
        self.thickness = thickness
        self.life = 0
        self.color = self.START_COLOR

    def update(self, **kwargs):
        self.life += (1 / self.FRAMES) * kwargs["dt"]

        if self.life >= 1:
            self.destroy()
        else:
            self.radius = self.life * self.INITIAL_RADIUS
            self.thickness = (1 - self.life) * self.INITIAL_THICKNESS
            self.color = self.START_COLOR.lerp(self.END_COLOR, self.life)

    def draw(self, surface, offset=(0, 0)):
        center = self.position.x - offset[0], self.position.y - offset[1]
        radius = int(self.radius)
        thickness = int(self.thickness)

        if thickness == 0:
            thickness = 1

        pygame.draw.circle(
            surface,
            (0, 0, 0),
            center,
            radius + 2,
            thickness + 2
        )

        pygame.draw.circle(
            surface,
            self.color,
            center,
            radius,
            thickness
        )
