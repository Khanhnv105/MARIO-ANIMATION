import math
from math import sin

import pygame

from data.engine.math.vector import Vector


class MovingBackground:
    """
    Simple clase que contiene una imagen y a travez de
    esta hace como si el fondo se moviera, se puede
    declarar cualquier direccion, pero solamente
    se puede mover en un solo eje a la vez
    """

    def __init__(self, image, x_axis=0, y_axis=-1, sin_wave_movement=False):
        self.sin_wave = sin_wave_movement
        if x_axis != 0 and y_axis != 0:
            raise Exception(f"Only one of the axis will be allowed to move: x={x_axis}, y={y_axis}")

        if isinstance(image, pygame.Surface):
            self.image = image
        elif isinstance(image, str):
            self.image = pygame.image.load(image).convert()

        self.offset_y = 0
        self.offset = Vector()
        self.velocity = Vector(x_axis, y_axis)
        self.direction = "UP"
        self.BASE_VELOCITY = Vector(x_axis, y_axis)

        if y_axis > 0:
            self.direction = "DOWN"

        if x_axis < 0:
            self.direction = "LEFT"

        elif x_axis > 0:
            self.direction = "RIGHT"

    def push(self, magnitude):
        """Aumenta la velocidad de movimiento del fondo temporalmente"""
        if magnitude < 1:
            magnitude = 1

        if self.direction == "UP":
            self.velocity.y = -magnitude

        elif self.direction == "DOWN":
            self.velocity.y = magnitude

        elif self.direction == "LEFT":
            self.velocity.x = -magnitude

        else:
            self.direction.x = magnitude

    def update(self, dt):
        add = self.velocity * dt

        self.velocity *= 0.95

        if self.sin_wave:
            sinval = sin(pygame.time.get_ticks() / 400)
            if sinval > 0:
                sinval *= 2
            add *= sinval

        self.offset += add

        if self.direction == "UP" or self.direction == "DOWN":

            if abs(self.offset.y) > self.image.get_height():
                self.offset = Vector()

            if abs(self.velocity.y) <= abs(self.BASE_VELOCITY.y):
                self.velocity.y = self.BASE_VELOCITY.y

        elif self.direction == "LEFT" or self.direction == "RIGHT":

            if abs(self.offset.x) > self.image.get_width():
                self.offset = Vector()

            if abs(self.velocity.x) <= abs(self.BASE_VELOCITY.x):
                self.velocity.x = self.BASE_VELOCITY.x

    def draw(self, surface):

        if self.direction == "UP":

            pos1 = 0, int(self.offset.y)
            pos2 = 0, int(self.offset.y + self.image.get_height())

        elif self.direction == "DOWN":

            pos1 = 0, int(self.offset.y)
            pos2 = 0, int(self.offset.y - self.image.get_height())

        elif self.direction == "LEFT":
            pos1 = int(self.offset.x), 0
            pos2 = int(self.offset.x) + self.image.get_width(), 0

        else:
            pos1 = int(self.offset.x), 0
            pos2 = int(self.offset.x) - self.image.get_width(), 0

        surface.blit(self.image, pos1)
        surface.blit(self.image, pos2)
