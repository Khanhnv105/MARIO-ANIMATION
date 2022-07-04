from math import pi, sin, cos

import pygame

from data.engine.entity.image_collideable_entity import ImageCollideableEntity
from data.engine.math.vector import Vector
from data.engine.physics.objects.pendulum import Pendulum
from data.engine.tile.tile_set_loader import load_tile
from data.engine.utils import draw_centered
from data.scripts.map.enemies.enemy import Enemy
from data.scripts.particles.static_circle import StaticCircle


class EnemyPendulum(Pendulum, ImageCollideableEntity, Enemy):

    def __init__(self, group, position, length, start_angle=72):
        image = load_tile("data/Assets/Free/Traps/Spiked Ball/Spiked Ball.png", 2, None)
        self.chain = load_tile("data/Assets/Free/Traps/Spiked Ball/Chain.png", 2, None)

        ImageCollideableEntity.__init__(self, group, position, image, layer=1)
        Pendulum.__init__(self, position, length, start_angle * pi / 180)

        self.distance_between_chains = (self.chain.get_width() ** 2 + self.chain.get_height() ** 2) ** 0.5 // 2
        self.radius = (self.image.get_width() + self.image.get_height()) // 4
        self.rotation = 0
        self.velocity = 0
        self.pendulum_pos = self._get_pendulum_position()

        self.DELAY = 60
        self.append_particle_time = 0

    def get_position(self):
        return self._get_pendulum_position()

    def update(self, **kwargs):
        super().update(**kwargs)

        # Velocidad calculada en base a la variacion de posiicon
        # del pendulo, Velodidad angular, es por eso que es escalar
        new_pos = self._get_pendulum_position()
        self.velocity = (new_pos - self.pendulum_pos).length

        self.pendulum_pos = new_pos
        self.rectangle.x = self.pendulum_pos.x - self.rectangle.w // 2
        self.rectangle.y = self.pendulum_pos.y - self.rectangle.h // 2
        self.rotation += kwargs["dt"] * 1
        self.update_data()

        if self.append_particle_time <= kwargs["clock_ticks"]:
            self.append_particle_time = kwargs["clock_ticks"] + self.DELAY
            StaticCircle(self.group.particles_manager, self.pendulum_pos, (50, 50, 50), 7)

    def draw(self, surface, offset=(0, 0)):
        degrees_angle = self.angle * 180 / pi

        sin_angle = sin(self.angle)
        cos_angle = cos(self.angle)
        amount_of_chains = int(self.length / self.distance_between_chains)
        chain = pygame.transform.rotate(self.chain, self.angle).convert_alpha()
        # Draw the chains
        position = self.position - Vector(offset)
        for i in range(amount_of_chains):
            distance = i * self.distance_between_chains
            draw_centered(
                surface,
                chain,
                (
                    position.x + sin_angle * distance,
                    position.y + cos_angle * distance
                )
            )

        # Draw the pendulum tail
        draw_centered(
            surface,
            pygame.transform.rotate(self.image, degrees_angle + self.rotation),
            self.pendulum_pos - Vector(offset)
        )
