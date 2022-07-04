from random import randint, random
import pygame

from data.engine.math.vector import Vector
from data.scripts.particles.circular_particle import CircularParticle
from data.scripts.particles.colored_particle import ColoredParticle
from data.scripts.players.base_player import BasePlayer


class ImagesSaver:
    """
    Clase que guarda las imagenes del Player
    cada cierto tiempo, y luego en base a si
    indice las renderiza con una transparencia
    decreciente en base al tiempo pasado
    """

    def __init__(self, length, max_transparency=None, delay=20):
        self.MAX_TRANSPARENCY = max_transparency
        self.LENGTH = length
        self.DELAY = delay

        self.start()

        self.last_time_saved = 0
        self.started = False

    def start(self):
        self.started = True
        self.images = [0 for _ in range(self.LENGTH)]
        self.positions = [(0, 0) for _ in range(self.LENGTH)]

    def end(self):
        self.started = False

    def update(self, image, top_left_position, **kwargs):
        if self.last_time_saved < kwargs["clock_ticks"]:
            self.images.pop(0)
            self.positions.pop(0)
            self.images.append(image.convert_alpha())
            self.positions.append(top_left_position)
            self.last_time_saved = self.DELAY + kwargs["clock_ticks"]

    def draw(self, surface, offset):

        if not self.started:
            return

        for index in range(len(self.images)):
            if self.images[index]:
                if self.MAX_TRANSPARENCY:
                    transparency = int((index / (self.LENGTH - 1)) * self.MAX_TRANSPARENCY)
                else:
                    transparency = 255
                image = self.images[index]
                if transparency != 255:
                    image.set_alpha(transparency)

                surface.blit(
                    image,
                    (
                        self.positions[index][0] - offset[0],
                        self.positions[index][1] - offset[1]
                    )
                )


class NinjaFrog(BasePlayer):

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
            JUMP=(pygame.K_c, pygame.K_SPACE),
            TURBO=(pygame.K_x, pygame.K_LSHIFT)
        )
        self.MAX_JUMPS = 2
        self.images_saver = ImagesSaver(10, max_transparency=150)

    def key_down(self, name):
        super().key_down(name)
        if "TURBO" == name:
            self.images_saver.start()

    def key_up(self, name):
        super().key_up(name)
        if "TURBO" == name:
            self.images_saver.end()

    def keys_held(self, names):
        if "TURBO" in names:
            self.MAX_SPEED = 8
        super().keys_held(names)

    def update(self, **kwargs) -> None:
        super().update(**kwargs)
        self.MAX_SPEED = 4
        if self.holding_key("TURBO"):
            self.images_saver.update(self.image, self._get_image_position(), **kwargs)

    def make_jump(self):
        if self.available_jumps > 0:
            self._jump_sound()
            self.velocity.y = -10
            self.on_ground = False
            self.available_jumps -= 1
            if self.available_jumps == 0:
                self.animations_controller.start_animation("DOUBLEJUMP")
                self.animations_controller.stop("HIT")
            self.group.game_scene.camera.push(Vector(0, -6))

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
                30,
                self._get_color_from_image(),
                thickness=50,
                frames=20
            )

    def draw(self, surface, offset=(0, 0)):
        if self.images_saver.images:
            self.images_saver.draw(surface, offset)

        super().draw(surface, offset)

    """
    Private methods
    """
