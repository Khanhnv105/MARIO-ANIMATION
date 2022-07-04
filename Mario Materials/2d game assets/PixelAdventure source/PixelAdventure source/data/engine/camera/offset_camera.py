from random import randint

import pygame

from data.engine.math.vector import Vector


class OffsetManager:
    FOLLOW_DIVISOR = 25

    def __init__(self, display_size):
        self.SIZE = Vector(display_size[0], display_size[1])
        self.CENTRAL_POINT = self.SIZE // 2
        self.previous_position = None
        self.position = None
        self.restart()

    def restart(self):
        self.previous_position = Vector()
        self.position = Vector()

    def update(self, delta, target_position):
        self._move_towards(Vector(target_position[0], target_position[1]), delta)

    def get_offset(self, zoom=1):
        return self.position * zoom - self.CENTRAL_POINT

    @property
    def rect(self):
        x, y = self.get_offset()
        return pygame.Rect(
            x,
            y,
            self.SIZE[0],
            self.SIZE[1]
        )

    def _move_towards(self, vector, delta):
        self.position += ((vector - self.position) / self.FOLLOW_DIVISOR) * delta

    def offset_by(self, x, y):
        self.position.x += x
        self.position.y += y


class OffsetCamera:
    """
    Simple version de camara que puede moverse hacia todos los lados
    del plano de la pantalla
    """

    def __init__(self, display_size):
        self.offset_manager = OffsetManager(display_size)

        # Variables para poder mover la camara en base a sus metodos
        self.shake_magnitude = None
        self.shake_end_time = None
        self.velocity = None
        self.restart()

    def restart(self):
        self.offset_manager.restart()
        self.shake_magnitude = Vector()
        self.shake_end_time = 0
        self.velocity = Vector()

    def shake(self, ms_duration, magnitude_x, magnitude_y):
        """Shake hace un movimiento impredecible y aleatorio"""
        self.shake_magnitude = Vector(magnitude_x, magnitude_y)
        self.shake_end_time = pygame.time.get_ticks() + ms_duration

    def push(self, velocity_vector):
        """La velocidad hace que la camara se mueva suavemente"""
        if isinstance(velocity_vector, Vector):
            self.velocity = velocity_vector
        else:
            self.velocity = Vector(velocity_vector[0], velocity_vector[1])

    def set_camera_offset(self, x, y):
        self.offset_manager.position.x = x
        self.offset_manager.position.y = y

    def update(self, **kwargs):
        if "target_position" in kwargs:
            self.offset_manager.update(kwargs["dt"], kwargs["target_position"])

        self.velocity = self.velocity.normalized() * (self.velocity.get_length() * (1 - kwargs["dt"] * 0.3))
        self.offset_manager.position += self.velocity * kwargs["dt"]

        if self.shake_end_time > kwargs["clock_ticks"]:
            self.offset_manager.offset_by(
                randint(-self.shake_magnitude.x, self.shake_magnitude.x),
                randint(-self.shake_magnitude.y, self.shake_magnitude.y)
            )

    @property
    def offset(self):
        return self.offset_manager.get_offset()

    @property
    def rect(self):
        return self.offset_manager.rect
