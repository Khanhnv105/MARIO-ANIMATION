import pygame

from data.engine.animation.sprite_animation.single_animation_controller import SingleAnimationController
from data.engine.entity.image_collideable_entity import ImageCollideableEntity
from data.engine.math.vector import Vector
from data.scripts.particles.circular_particle import CircularParticle
from data.scripts.players.base_player import BasePlayer
from data.scripts.utils import dynamic_animation_creation


class Trampoline(ImageCollideableEntity):
    """
    Trampoline tiene cuatro direcciones
    Top, Bottom, Left y Right.
    A traves de estas direcciones se determinan las
    componenetes de las fuerzas normalizadas y
    luego se multiplica esa fuerza por el
    parametro de force magnitude
    """

    def __init__(self, group, position, direction="Top", force_magnitude=15):
        self.DIRECTION = direction

        if direction == "Left":
            position = position[0] + 8, position[1]

        elif direction == "Bottom":
            position = position[0], position[1] - 8

        force_x = 0
        force_y = 0
        if direction == "Left":
            force_x = -1
        elif direction == "Right":
            force_x = 1

        if direction == "Top":
            force_y = -1
        elif direction == "Bottom":
            force_y = 1

        self.force = Vector(force_x * force_magnitude, force_y * force_magnitude)
        self.animation = SingleAnimationController(
            dynamic_animation_creation(
                images_path=f"data/Assets/Free/Traps/Trampoline/{direction}/Jump",
                cycle_mode="END",
                images_scale=2
            )
        )
        rect = self.animation.get_image().get_rect()
        rect.h /= 2
        rect.x = position[0]
        rect.y = position[1] + rect.h

        super().__init__(group, position, self.animation.get_image(), layer=1)
        self.points_offset = 0

        gravity_acc = 0.5
        self.distance = (self.force.y * self.force.y) / (2 * gravity_acc)
        self.amount_of_points = 10
        self.factor = self.distance / self.amount_of_points

    def collision(self, other) -> None:
        if other.__class__.__base__.__name__ == "BasePlayer" and not self.animation.is_running():

            if self.DIRECTION == "Top":
                other.ground()
                other.velocity.y = self.force.y
            elif self.DIRECTION == "Bottom":
                other.velocity.y = self.force.y

            elif self.DIRECTION == "Left" or self.DIRECTION == "Right":
                other.velocity.x = self.force.x

            other.play_sound("Action Misc 3.wav")
            other.on_ground = False
            self.animation.reset()
            CircularParticle(self.group.particles_manager, self.rectangle.center, 100, (255, 51, 51))
            self.group.game_scene.camera.push(self.force)

    def update(self, **kwargs) -> None:
        self.animation.update(kwargs['dt'])
        self.points_offset -= 1 * kwargs["dt"]
        if abs(self.points_offset) > self.factor * 2:
            self.points_offset = 0

    def draw(self, surface, offset=(0, 0)):
        surface.blit(
            self.animation.get_image(),
            (
                self.rectangle.x - offset[0],
                self.rectangle.y - offset[1]
            )
        )

        pygame.draw.circle(surface, (150, 150, 150), (self.rectangle.centerx - offset[0], self.rectangle.centery - self.distance - offset[1]), 7)
        pygame.draw.circle(surface, (150, 150, 150), (self.rectangle.centerx - offset[0], self.rectangle.centery - offset[1]), 7)

        for i in range(1, self.amount_of_points):
                point_distance = self.factor * i
                pygame.draw.circle(surface, (150, 150, 150), (self.rectangle.centerx - offset[0], -offset[1] + self.factor + self.rectangle.centery - point_distance + self.points_offset), 3)

