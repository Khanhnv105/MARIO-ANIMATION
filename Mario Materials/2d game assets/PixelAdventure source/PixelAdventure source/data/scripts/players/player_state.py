import math

import pygame

from data.engine.math.vector import Vector
from data.scripts.particles.circular_particle import CircularParticle


def outlined_circle(surface, color1, color2, x, y, radius):
    pygame.draw.circle(
        surface,
        color2,
        (int(x), int(y)),
        radius + 3
    )
    pygame.draw.circle(
        surface,
        color1,
        (int(x), int(y)),
        radius
    )


class SpawnVFX:
    """Clase que representa a la animacion que aparece cuando el jugador muere"""
    DISTANCE = 500
    CIRCLES_VELOCITY = 25

    def __init__(self, amount, color, min_distance=30):
        self.AMOUNT = amount
        self.COLOR = color
        self.MIN_DISTANCE = min_distance

        # Variables para controlar spawn VFX
        self.angle_offset = 0
        self.circles_distance_step = 0
        self.base_distance = self.DISTANCE

        self.step = 0
        self.end_pos = Vector()
        self.position = Vector()

    def ended(self):
        return self.step >= 1

    def set_spawn_pos(self, pos):
        self.end_pos = pos

    def restart(self, respawn_position):
        self.base_distance = self.DISTANCE
        self.step = 0
        self.end_pos = respawn_position

    def lerp(self, other):
        return other + (self.end_pos - other) * self.step

    def decrease_circle(self, player_pos, **kwargs):
        """Reduce el radio del circulo, con rotacion incluida"""
        self.angle_offset += 0.07 * kwargs["dt"]
        self.circles_distance_step += 0.2 * kwargs["dt"]
        self.base_distance -= self.CIRCLES_VELOCITY * kwargs["dt"]

        if self.base_distance < self.MIN_DISTANCE:
            self.base_distance = self.MIN_DISTANCE

        self.position = self.lerp(player_pos)

    def update_step(self, player_pos, dt):
        self.step += 10 / (self.end_pos.get_distance(player_pos)) * dt

    def increase_circle(self, **kwargs):
        """Hace que los circulos vuelvan a su posicion original progresivamente"""
        self.base_distance += self.CIRCLES_VELOCITY * kwargs["dt"] / 4
        if self.base_distance > self.DISTANCE:
            self.base_distance = self.DISTANCE
        self.angle_offset += 0.1 * kwargs["dt"]

    def draw(self, surface, offset):
        if not self.base_distance < self.DISTANCE:
            return

        circles = 10
        radius = self.base_distance + (math.sin(self.circles_distance_step) + 1) / 2 * 18
        for a in range(0, 360, 360 // circles):
            angle = math.radians(a) + self.angle_offset

            distance = radius

            x = math.cos(angle) * distance + self.position.x - offset.x
            y = math.sin(angle) * distance + self.position.y - offset.y
            outlined_circle(
                surface,
                (255, 255, 255),
                (0, 0, 0),
                x,
                y,
                (1 - (self.base_distance / self.DISTANCE)) * 7.5
            )


class PlayerState:
    """
    Clase que controla la cantidad de muertes, respawn, collectables, y fin del nivel
    """
    PLAYER_RESPAWN_DELAY = 1500

    def __init__(self, player, spawn_pos):
        self.player = player
        self.player_points = 0
        self.player_fruits_collected = {}
        self.player_spawn = Vector(spawn_pos[0], spawn_pos[1])
        self.player_dead_image = self.player.animations_controller.get_image_from_animation("HIT", 1)
        self.death_pos = Vector()

        self.respawn_time = None
        self.respawn()
        self.is_dead = False
        self.particle_time = True

        # Variables para controlar spawn VFX
        self.circle = SpawnVFX(10, (255, 255, 255))
        self.circle_on = False
        self.deaths = 0
        self.win = False

    def update(self, player, **kwargs):
        self.player = player

        if self.is_dead:

            self.circle.decrease_circle(self.player.position, **kwargs)

            if not self.player.animations_controller.is_running("HIT"):
                player.disable()
                if not self.circle_on:
                    self.player.play_sound("Transport Down.wav")
                    self.circle_on = True
                if self.respawn_time < kwargs["clock_ticks"]:

                    self.circle.update_step(self.player.position, kwargs['dt'])
                    if self.circle.ended():
                        self.respawn()

                if self.particle_time:
                    self.particle_time = False
                    CircularParticle(
                        self.player.group.particles_manager,
                        self.player.position,
                        100,
                        (255, 255, 255)
                    )

        else:
            self.circle.increase_circle(**kwargs)

    def won(self):
        self.win = True

    def change_respawn(self, pos):
        self.player_spawn = Vector(pos[0], pos[1])

    def collected(self, points):
        self.player_points += points

    def respawn(self):
        self.player.play_sound("Magic Spell 1.wav")
        self.player.set_center_pos(self.player_spawn.x, self.player_spawn.y)
        self.respawn_time = None
        self.is_dead = False
        self.player.dead = False
        self.player.enable()

    def dead(self):
        if not self.is_dead:
            self.deaths += 1
            self.circle.restart(self.player_spawn.copy())
            self.circle_on = False
            self.respawn_time = pygame.time.get_ticks() + self.PLAYER_RESPAWN_DELAY
            self.is_dead = True
            self.particle_time = True
            self.player.group.game_scene.camera.zoom_at(60, 1.4)

    def draw(self, surface, offset):
        self.circle.draw(surface, offset)
