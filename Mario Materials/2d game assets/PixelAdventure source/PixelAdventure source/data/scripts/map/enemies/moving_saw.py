import math
from math import sin

import pygame

from data.engine.animation.sprite_animation.single_animation_controller import SingleAnimationController
from data.engine.entity.image_collideable_entity import ImageCollideableEntity
from data.engine.math.vector import Vector
from data.engine.utils import draw_centered
from data.scripts.map.enemies.enemy import Enemy


class MovingSaw(ImageCollideableEntity, Enemy):
    """
    MovingSaw es una entidad la cual se mueve por todas las
    posiciones pasadas por parametro progresivamente
    """

    def __init__(self, group, *points, draw_path=True, start_index=0):
        self.animation = SingleAnimationController("data/Assets/animations/saw/on.json")
        image = self.animation.get_image()

        super().__init__(group, points[0], image, layer=-2)

        # Lista con todos los puntos por lo que va a pasar
        self.points = [Vector(point[0], point[1]) for point in points]
        self.actual_point_index = start_index
        self.moving_to_point_index = start_index + 1
        if self.moving_to_point_index > len(self.points) - 1:
            self.moving_to_point_index = len(self.points) - 1

        self.step = 0
        self.velocity = 0.03
        self.normalized_position_step = 0
        self.forward = True
        self.actual_position = Vector()
        self.draw_path = draw_path

    def update(self, **kwargs):
        self.step += self.velocity * kwargs["dt"]
        self.animation.update(dt=kwargs['dt'])

        # Actualizo el valor unitario de la posicion
        normalized_ratio_position = (sin(self.step) + 1) / 2

        # Cuando se acerca mucho al siguiente punto
        # cambia el target a el punto siguiente
        if normalized_ratio_position > 0.95:
            self.normalized_position_step = 0
            self.step = math.pi * 3 / 2
            self.actual_point_index = self.moving_to_point_index
            self.moving_to_point_index = self.moving_to_point_index + 1

            if self.moving_to_point_index > len(self.points) - 1:
                self.moving_to_point_index = 0
        else:
            self.normalized_position_step = normalized_ratio_position

        # En base al sentido del eje X se rota o no la imagen
        p1 = self.points[self.actual_point_index]
        p2 = self.points[self.moving_to_point_index]
        self.forward = p1.x < p2.x

        # Update posicion
        self.actual_position = self._get_actual_position()

        # Cambio de imagen
        self.image = self.animation.get_image()
        if self.forward:
            self.image = pygame.transform.flip(self.image, True, False)

        self.update_data()
        self.rectangle.x = self.actual_position.x - self.rectangle.w // 2
        self.rectangle.y = self.actual_position.y - self.rectangle.h // 2

    @property
    def position(self):
        return self.actual_position

    def get_position(self):
        return self.position

    def draw(self, surface, offset=(0, 0)):
        if self.draw_path:
            if len(self.points) > 2:
                # Dibujo todos los puntos que forman la trayectoria
                for i in range(len(self.points)):

                    if i + 1 > len(self.points) - 1:
                        self.draw_points(surface, self.points[-1], self.points[0], offset)

                    else:
                        self.draw_points(surface, self.points[i], self.points[i + 1], offset)
            else:
                self.draw_points(surface, self.points[0], self.points[1], offset)

        draw_centered(
            surface,
            self.image,
            (
                self.actual_position.x - offset[0],
                self.actual_position.y - offset[1]
            )
        )


    def draw_points(self, surface, p1, p2, offset, points_distance=15, points_radius=3):
        dist = p2 - p1
        length = dist.length
        amount = int(length / points_distance)

        norm = dist.normalized()

        for i in range(amount):
            distance = points_distance * i
            pos = norm * distance
            pygame.draw.circle(
                surface,
                (50, 50, 50),
                pos + p1 - offset,
                points_radius
            )

    def _get_actual_position(self):
        """Retorna la posicion del centro de la cierra"""
        final_position = self.points[self.moving_to_point_index]
        initial_position = self.points[self.actual_point_index]
        distance = final_position - initial_position
        magnitude = self.normalized_position_step * distance.get_length()
        return distance.normalized() * magnitude + initial_position
