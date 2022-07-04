from random import randint, random
import pygame

from data.engine.math.vector import Vector
from data.scripts.particles.circular_particle import CircularParticle
from data.scripts.particles.colored_particle import ColoredParticle
from data.scripts.players.base_player import BasePlayer


class DashImages:
    def __init__(self, length, max_alpha=255, frames=20):
        self.LENGTH = length
        self.MAX_ALPHA = max_alpha
        self.FRAMES = frames
        self.images = []
        self.start_position = Vector()
        self.moving_position = Vector()
        self.value = 0

    def start(self, actual_image, start_position):
        self.start_position = start_position
        self.images.clear()
        for index in range(self.LENGTH):
            image = actual_image.copy()
            alpha = ((self.LENGTH - 1 - index) / self.LENGTH) * self.MAX_ALPHA
            image.set_alpha(alpha)
            self.images.append(image)

    def update(self, actual_position, **kwargs):

        self.value += (1 / self.FRAMES) * kwargs["dt"]
        self.moving_position = self.start_position + (actual_position - self.start_position) * self.value

        if self.value > 1:
            self.value = 0
            self.images.clear()

    def draw(self, surface, actual_position, offset):

        for i, image in enumerate(self.images):
            value = i / (len(self.images) - 1)
            position = self.moving_position + (actual_position - self.moving_position) * value
            surface.blit(
                image,
                position - Vector(offset)
            )


class VirtualGuy(BasePlayer):

    def __init__(self, group, character_type: str, position, respawn_pos=None, input_blocked=False):
        super().__init__(
            group,
            character_type,
            position,
            respawn_pos,
            input_blocked,
            UP=pygame.K_UP,
            DOWN=pygame.K_DOWN,
            LEFT=pygame.K_LEFT,
            RIGHT=pygame.K_RIGHT,
            JUMP=pygame.K_c,
            DASH=pygame.K_x
        )
        self.dashed_time = 0
        self.show_dash = False
        self.dash_vector = Vector()
        self.dash_position = Vector()
        self.DASH_SHOWTIME = 200

        self.dash_images = DashImages(10, max_alpha=100)

    def key_down(self, name):
        super().key_down(name)

        if name == "DASH":
            self.dash_images.start(self.image, self._get_image_position())
            x = 0
            y = 0
            self.group.game_scene.sfx.play("Action Misc 20.wav")

            if self.holding_key("LEFT"):
                x -= 1
            if self.holding_key("RIGHT"):
                x += 1

            if self.holding_key("UP"):
                y -= 1
            if self.holding_key("DOWN"):
                y += 1

            self.dash_vector = Vector(x, y).normalized()

            self.dash_position = self.position

            displacement = Vector(x, y) * self.DASH_MAGNITUDE
            final = displacement + self.position
            self.set_center_pos(final.x, final.y)
            self.velocity = Vector(displacement / 20)
            self.group.game_scene.camera.push(Vector(x, y) * 2)
            self.show_dash = True
            self.dashed_time = pygame.time.get_ticks() + self.DASH_SHOWTIME

            self.group.game_scene.camera.push(-self.dash_vector * 10)

    def update(self, **kwargs) -> None:
        super().update(**kwargs)

        self.dash_images.update(self._get_image_position(), **kwargs)

        if self.dashed_time < kwargs["clock_ticks"]:
            self.show_dash = False

    def make_jump(self):
        available = self.available_jumps
        super().make_jump()
        if self.available_jumps < available:
            for _ in range(10):
                offset_x = random() * 10

                ColoredParticle(
                    self.group.particles_manager,
                    (self.collisions_rectangle.centerx + offset_x, self.collisions_rectangle.bottom),
                    Vector((random() - 0.5) * 2, -randint(3, 5)),
                    self._get_color_from_image(),
                    max_radius=6

                )
            CircularParticle(
                self.group.particles_manager,
                self.collisions_rectangle.center,
                50,
                self._get_color_from_image(),
                thickness=30,
                frames=20
            )

    def draw(self, surface, offset=(0, 0)):
        self.dash_images.draw(surface, self._get_image_position(), offset)
        super().draw(surface, offset)
