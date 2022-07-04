from random import randint, random

import pygame

from data.engine.animation.sprite_animation.animations_controller import AnimationsController
from data.engine.entity.image_collideable_entity import ImageCollideableEntity
from data.engine.entity.input_entity import InputEntity
from data.engine.math.vector import Vector
from data.engine.physics.rectangular_physical_entity import RectangularPhysicalEntity
from data.scripts.map.enemies.enemy import Enemy
from data.scripts.map.tile.static_tile import Tile
from data.scripts.particles.colored_particle import ColoredParticle
from data.scripts.particles.GameParticle import GameParticle
from data.scripts.particles.static_circle import StaticCircle


PLAYER_DEAD = pygame.USEREVENT + 5
PLAYER_CHECKPOINT = pygame.USEREVENT + 6
PLAYER_COLLECTABLE = pygame.USEREVENT + 7
PLAYER_WIN = pygame.USEREVENT + 8


class BasePlayer(ImageCollideableEntity, RectangularPhysicalEntity, InputEntity):
    MAX_SPEED = 4
    MAX_JUMP_MAGNITUDE = 15
    JUMP_MAGNITUDE = 10
    DASH_MAGNITUDE = 100
    MAX_JUMPS = 1
    MOVEMENT_SPEED = 10
    PARTICLE_DELAY = 100

    def __init__(
            self,
            group,
            character_type: str,
            position,
            respawn_pos=None,
            input_blocked=False,
            **input_keys

    ):
        self.character = character_type
        self.running = False
        self.jumping = False
        self.falling = False
        self.wall_jumping = False
        self.on_ground = False

        self.MOVING_LEFT = False
        self.MOVING_RIGHT = False

        self.available_jumps = self.MAX_JUMPS
        self._load_animations(character_type)
        if respawn_pos:
            self.respawn_pos = Vector(respawn_pos[0], respawn_pos[1])
        else:
            self.respawn_pos = Vector(position[0], position[1])
        image = self.animations_controller.get_image()
        ImageCollideableEntity.__init__(self, group, position, image, layer=10)

        w_sub_sides = int(self.rectangle.w / 5)
        h_sub_sides = int(self.rectangle.h / 5)

        collisions_rectangle = pygame.Rect(
            self.rectangle.x + w_sub_sides,
            self.rectangle.y + h_sub_sides,
            self.rectangle.w - w_sub_sides * 2,
            self.rectangle.h - h_sub_sides
        )

        RectangularPhysicalEntity.__init__(self, collisions_rectangle, (self.rectangle.x, self.rectangle.bottom))

        InputEntity.__init__(self, input_blocked, **input_keys)
        self.particle_time = 0
        self.add_particle = True
        self.disabled = False
        self.dead = False

        self.footstep_sound = 0

    def key_down(self, name):
        if name == "JUMP":
            self.make_jump()

    def keys_held(self, names):
        if "LEFT" in names:
            self.push((-self.MOVEMENT_SPEED, 0))
            self.constrain_velocity(self.MAX_SPEED)
            self.MOVING_LEFT = True
        if "RIGHT" in names:
            self.push((self.MOVEMENT_SPEED, 0))
            self.constrain_velocity(self.MAX_SPEED)
            self.MOVING_RIGHT = True

        if self.MOVING_RIGHT and self.MOVING_LEFT:
            self.MOVING_RIGHT = self.MOVING_LEFT = False

    def collision(self, other) -> None:
        other_type = type(other).__name__
        if other_type == "Fruit" or other_type == "Coin" or other_type == "Gem":
            other.collected()
            other.delete()

        if not self._already_hit():
            if other_type == "MovingSaw":

                push_magnitude = 3
                distance_vector = self.get_vector_to(other.get_position())
                normalized = distance_vector.normalized() * push_magnitude
                self.velocity = normalized * push_magnitude
                self._hit()
                self.group.game_scene.camera.shake(100, 4, 4)

            elif other_type == "EnemyPendulum":
                distance = self.get_vector_to(other.get_position()).normalized()
                self.velocity += distance * other.velocity * 100
                self.velocity.constrain(self.MAX_JUMP_MAGNITUDE)
                self._hit()

                self.group.game_scene.camera.shake(100, 4, 4)

            elif other_type == "HeadEnemy":
                self.push((self.position - other.get_position()).normalized() * 10)
                self._hit()

    def static_collision(self, static):
        if not self._already_hit():
            static.collision(self)
            if type(static).__name__ == "Spike":
                self.velocity.y = -10
                self._hit()
                self.group.game_scene.camera.shake(90, 0, 4)

    def update(self, **kwargs) -> None:
        if self.disabled:
            return
        delta_tine = kwargs["player_dt"]
        self.future_collision_check()
        self._handle_animations(delta_tine)

        # Velocity reduction via friction coefficients
        if not self.on_ground:
            friction_coefficient = 0.01
        else:
            friction_coefficient = 0.3

        # Gravedad y fuerza de rozamiento
        self.acceleration += Vector(-friction_coefficient * self.velocity.x, 0.5)
        self.update_velocity(delta_tine)
        self._move(delta_tine)

        if self.particle_time < kwargs["clock_ticks"] and self.is_visible():
            self.add_particle = True
            self.particle_time = kwargs["clock_ticks"] + self.PARTICLE_DELAY

        else:
            self.add_particle = False

        self.image = self.animations_controller.get_image()
        if self.MOVING_LEFT:
            self.image = pygame.transform.flip(self.image, True, False).convert_alpha()

        if self.holding_key("LEFT", "RIGHT") and self.footstep_sound < kwargs["clock_ticks"] and self.on_ground:
            self.play_sound(f"Footstep {randint(1, 2)}.wav")
            self.footstep_sound = kwargs["clock_ticks"] + 250

        self._movement_particles()
        self._is_close_radius()

        self.update_data()

    def ground(self):
        self.on_ground = True
        self.available_jumps = 2

    def play_sound(self, name):
        self.group.game_scene.director.sfx.play(name)

    def make_jump(self):
        if self.available_jumps > 0:
            self._jump_sound()
            self.velocity.y = -self.JUMP_MAGNITUDE
            self.on_ground = False
            self.available_jumps = 0
            self.group.game_scene.camera.push(Vector(0, -2))

    def disable(self):
        self.disabled = True
        self.set_visible(False)
        self.block_input()
        self.velocity = Vector()
        self.acceleration = Vector()

    def enable(self):
        self.dead = False
        self.disabled = False
        self.set_visible(True)
        self.activate_input()
        self.restart_key_states()

    def set_center_pos(self, x, y):
        super().set_center_pos(x, y)
        self.rectangle.centerx = x
        self.rectangle.centery = y

    def draw(self, surface, offset=(0, 0)):
        if self.is_visible():
            surface.blit(
                self.image,
                self._get_image_position() - offset
            )

    """
    Private methods
    """

    def _jump_sound(self):
        self.play_sound(f"Jump {randint(1, 4)}.wav")

    def _move(self, dt):

        """
        Se encarga de mover al jugador en base a su entorno
        1 - Verifica las colisiones con los tiles, y acomoda su posicion
        2 - Obtiene todas las colisiones del QuadTree estatico, y llama a
        3 - El metodo respectivo para tratarlas
        """

        previous = self.rectangle.copy()
        self.rectangle = self.collisions_rectangle.copy()
        self.update_x_pos(dt)
        self.set_center_pos(self.position.x, self.position.y)
        collisions = self.collisions_manager.get_filtered_static_collisions_by_subclass(self, Tile)

        for other in collisions:
            self._handle_horizontal_collision(other)

        self.update_y_pos(dt)
        self.set_center_pos(self.position.x, self.position.y)
        collisions = self.collisions_manager.get_filtered_static_collisions_by_subclass(self, Tile)

        ground = False
        for other in collisions:
            state = self._handle_vertical_collision(other)
            if state:
                ground = True

        self.on_ground = ground

        self.rectangle = previous
        collisions = self.collisions_manager.get_static_collisions(self)
        for collision in collisions:
            self.static_collision(collision)

        self.set_center_pos(self.position.x, self.position.y)

    def _handle_horizontal_collision(self, tile):
        tile_type = type(tile).__name__
        if tile_type == "PassableBottomTile": return

        if self.velocity.x:
            # Collides Right
            if self.velocity.x > 0:
                self.set_right_pos(tile.rectangle.left)

            # Collides left
            else:
                self.set_left_pos(tile.rectangle.right)
            self.velocity.x = 0

    def _handle_vertical_collision(self, tile):

        tile_type = type(tile).__name__

        if tile_type == "PassableBottomTile":
            if self.velocity.y > 0 and self.rectangle.bottom - self.velocity.y < tile.rectangle.centery:
                self.ground()
                self.set_bottom_pos(tile.rectangle.top)
                self.velocity.y = 0
                return True
            return

        if self.velocity.y:
            # Collides bottom
            if self.velocity.y > 0:
                self.ground()
                self.set_bottom_pos(tile.rectangle.top)
                self.velocity.y = 0
                return True

            # Collides top
            else:
                self.set_top_pos(tile.rectangle.bottom)
                self.velocity.y = 0

    def _is_close_radius(self):
        if self.dead:
           return
        """
        Metodo que modifica el zoom de la camara y la velocidad del fondo cuando el
        jugador se acera a un enemigo se considera enemigo a toda subclase de Enemy
        """

        background_radius = 200
        zoom_radius = 50
        rect = pygame.Rect(
            self.position[0] - background_radius,
            self.position[1] - background_radius,
            background_radius * 2,
            background_radius * 2
        )
        close_enemies = self.collisions_manager.filtered_query_subclass(rect, Enemy)

        if not close_enemies:
            return
        distance = lambda p1, p2: ((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1])) ** 0.5
        closest_distance = min([distance(self.position, enemy.get_position()) for enemy in close_enemies])

        # Si es que el objeto esta dentro de la circunferencia
        if closest_distance < zoom_radius:
            maximum = 1.1
            minimum = 1
            max_distance = zoom_radius
            zoom = minimum + (max_distance - closest_distance) * (maximum - minimum) / max_distance
            self.group.game_scene.camera.set_zoom(zoom)

        # Dependiendo de la distancia de acelera el movimiendo del fondo
        if closest_distance < background_radius:
            maximum = 6
            minimum = 1
            max_distance = background_radius
            velocity_magnitude = minimum + (max_distance - closest_distance) * (maximum - minimum) / max_distance
            self.group.game_scene.level_manager.background.push(velocity_magnitude)

    def _handle_animations(self, dt):
        """
        Verifica el estado del jugador, y modifica
        las variables para que luego las animaciones
        tengan correspondencia eon el estado del jugador
        """
        self.running = abs(self.velocity.x) > 0.1

        if self.velocity.y < 0 and not self.on_ground:
            self.falling = True
            self.jumping = False

        elif self.velocity.y - 1 > 0 and not self.on_ground:
            self.jumping = True
            self.falling = False

        else:
            self.falling = False
            self.jumping = False
            self.on_ground = True

        self.animations_controller.update(
            dt,
            running=self.running,
            hit=False,
            doublejump=False,
            walljump=self.wall_jumping,
            jump=self.jumping,
            fall=self.falling
        )

    def _movement_particles(self):

        """
        Agrega las particulas,
        Siempre se agrega una particula estatica en la posicion del Player
        y si es que se esta moviendo horizontalmente se agrega una de movimiento
        """

        if self.add_particle:
            if self.on_ground:
                if self.holding_key("LEFT"):

                    ColoredParticle(
                        self.group.particles_manager,
                        (
                            self.collisions_rectangle.right,
                            self.collisions_rectangle.bottom - 10
                        ),
                        Vector(random() * 2, -random() * 4),
                        pygame.Color(240, 240, 240),
                        max_radius=4
                    )

                elif self.holding_key("RIGHT"):

                    ColoredParticle(
                        self.group.particles_manager,
                        (
                            self.collisions_rectangle.left,
                            self.collisions_rectangle.bottom - 10
                        ),
                        Vector(-random() * 2, -random() * 4),
                        pygame.Color(240, 240, 240),
                        max_radius=6
                    )

            StaticCircle(
                self.group.particles_manager,
                self.position,
                (0, 0, 0),
                randint(3, 5)
            )

    def _hit(self):
        if self.dead:
            return
        if self.animations_controller.is_running("DOUBLEJUMP"):
            self.animations_controller.stop("DOUBLEJUMP")

        self.animations_controller.start_animation("HIT")
        GameParticle(
            self.group.particles_manager,
            self.rectangle.center,
            "data/Assets/Free/Main Characters/Desappearing (96x96)"
        )
        for _ in range(50):
            ColoredParticle(
                self.group.particles_manager,
                self.rectangle.center,
                Vector.random(random() * 5),
                self._get_color_from_image()
            )

        event = pygame.event.Event(PLAYER_DEAD, {})
        pygame.event.post(event)
        self.dead = True


    def _already_hit(self):
        return self.animations_controller.is_running("HIT")

    def _get_color_from_image(self):
        """
        Retorna un color de la imagen de forma aleatoria
        """
        found = False
        w = self.image.get_width() - 1
        h = self.image.get_height() - 1
        while not found:
            color = self.image.get_at((randint(1, w), randint(1, h)))
            if color[3]:
                return pygame.Color(color[0], color[1], color[2])

    def _get_image_position(self):
        return Vector(
            self.collisions_rectangle.centerx - self.image.get_width() // 2,
            self.collisions_rectangle.bottom - self.image.get_height()
        )

    def _load_animations(self, character_type: str):
        """
        Metodo que se encarga de cargar las animaciones creando un
        diccionario dinamicamente en base al personaje seleccionado,
        de esta forma no hace falta crear un archivo .json para cada
        uno de los personajes
        """

        images_path = "data/Assets/Free/Main Characters" + "/" + character_type

        animations_data = {
            "WALLJUMP": {
                "delay": 3,
                "cycle_mode": "END",
                "images_path": images_path + "/Wall jump (32x32)",
                "conditions": ["walljump"],
                "images_colorkey": None,
                "images_scale": 2
            },
            "DOUBLEJUMP": {
                "delay": 3,
                "cycle_mode": "END",
                "images_path": images_path + "/Double jump (32x32)",
                "conditions": ["doublejump"],
                "images_colorkey": None,
                "images_scale": 2
            },
            "JUMP": {
                "delay": 3,
                "cycle_mode": "END",
                "images_path": images_path + "/Jump (32x32)",
                "conditions": ["jump"],
                "images_colorkey": None,
                "images_scale": 2
            },
            "FALL": {
                "delay": 3,
                "cycle_mode": "END",
                "images_path": images_path + "/Fall (32x32)",
                "conditions": ["fall"],
                "images_colorkey": None,
                "images_scale": 2
            },
            "RUN": {
                "delay": 3,
                "cycle_mode": "REPEAT",
                "images_path": images_path + "/Run (32x32)",
                "conditions": ["running"],
                "images_colorkey": None,
                "images_scale": 2
            },
            "HIT": {
                "delay": 3,
                "cycle_mode": "END",
                "images_path": images_path + "/Hit (32x32)",
                "conditions": ["hit"],  # ["hit"],
                "images_colorkey": None,
                "images_scale": 2
            },
            "IDLE": {
                "delay": 2,
                "cycle_mode": "REPEAT",
                "images_path": images_path + "/Idle (32x32)",
                "conditions": [],
                "images_colorkey": None,
                "images_scale": 2
            }
        }
        self.animations_controller = AnimationsController(animations_data)
