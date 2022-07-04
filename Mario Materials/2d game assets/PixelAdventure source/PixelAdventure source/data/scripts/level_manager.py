import pygame
import pytmx

from data.engine.image.editor import scale_image, get_clip
from .collideable_group_particles import CollideableGroupWithParticles
from .entities import *
from .map.map_interactive.wind import Wind
from .players.player_state import PlayerState
from .text import Text


class LevelManager:
    """
    Level manager se encarga de cargar los mapas y luego
    todas las entidades con sus propiedades especificas
    y posiciones.
    """

    def __init__(self, scene, level_name: str):
        self.scene = scene

        self.player = None
        self.map = None
        self.background = None
        self.group = None
        self.map_path = None
        self.player_state = None

        self._load_map(level_name)

        self.game_surface = pygame.Surface(self.scene.director.DISPLAY_SIZE).convert()
        self.game_speed = 1
        self.game_slow = 1

    def key_down(self, event):
        self.group.key_down(event)

    def key_up(self, event):
        self.group.key_up(event)

    def player_dead_event(self, event):
        self.player_state.dead()

    def update(self, **kwargs):

        self.group.update(
            dt=kwargs["dt"] * self.game_speed * self.game_slow,
            player_dt=kwargs["dt"] * self.game_speed,
            clock_ticks=kwargs["clock_ticks"],
            gravity_acceleration=10,
            keys=pygame.key.get_pressed(),
            display_rect=self.scene.camera.rect
        )
        self.background.update(kwargs["dt"])
        self.player_state.update(self.player, **kwargs)

    def draw(self, surface, offset, zoom):
        self.background.draw(self.game_surface)

        self.group.draw(self.game_surface, offset, rect=False)
        self.player_state.draw(self.game_surface, offset)
        # Si es que hay zoom se recorta una parte de la imagen y se la 
        # extiende para simular zooom
        if zoom != 1:
            SIZE = self.scene.director.DISPLAY_SIZE
            div = SIZE / zoom
            width, height = int(div.x), int(div.y)

            x = self.player.position.x - width / 2 - offset[0]
            y = self.player.position.y - height / 2 - offset[1]

            if x + width > SIZE.x:
                x = SIZE.x - width
            elif x < 0:
                x = 0
            if y < 0:
                y = 0
            elif y + height > SIZE.y:
                y = SIZE.y - height

            rect = pygame.Rect(x, y, width, height)
            image = pygame.transform.scale(get_clip(self.game_surface, rect), SIZE)
            surface.blit(image, (0, 0))

        else:
            surface.blit(self.game_surface, (0, 0))

    def _load_map(self, name):
        """
        Carga el mapa deade el archivo .tmx y crea todas las entidades
        y Tiles con sus respectivas propiedades. Ademas crea el
        jugador y busca su posicion inicial de respawn
        """
        self.map_path = f"data/Assets/maps/{name}.tmx"
        self.LEVEL_NUMBER = name[-2:]
        self.background = MovingBackground("data/Assets/Free/Background/Big Scale/Pink.png")
        self.map = pytmx.load_pygame(self.map_path)
        GRID_SIZE = self.map.tilewidth * self.scene.scale
        self.group = CollideableGroupWithParticles(self.scene, (self.map.width * GRID_SIZE, self.map.height * GRID_SIZE))
        self.group.update_not_visible(False)

        def get_position(image, x, y):
            """
                Retorna la posicion superior izquierda del
                rect, dado a que Tiled trabaja con al inferior
                izquierda
                """
            y += 1
            sub_y = image.get_height() / GRID_SIZE
            return x * GRID_SIZE, (y - sub_y) * GRID_SIZE

        def get_points(obj):
            """Retorna la lista de puntos del objeto"""
            return [(point.x * self.scene.scale, point.y * self.scene.scale) for point in obj.as_points]

        def get_rect(obj):
            """
            En el caso de que el poligono sea un rectangulo
            se usa este metodo para obtener el rectangulo en
            base a los puntos
            """
            points = get_points(obj)
            return pygame.Rect(points[0][0], points[0][1], points[2][0] - points[0][0], points[1][1] - points[0][1])

        for i, layer in enumerate(self.map):

            if isinstance(layer, pytmx.TiledTileLayer):

                for x, y, image in layer.tiles():
                    """Obtengo las propiedades del tile"""
                    properties = self.map.get_tile_properties(x, y, i)
                    scaled_image = scale_image(image, self.scene.scale)
                    top_left_position = get_position(scaled_image, x, y)

                    object_type = properties["type"]
                    if object_type == "Spike":
                        Spike(self.group, top_left_position, side=properties["side"])

                    elif object_type == "Start":
                        Start(self.group, top_left_position)

                    elif object_type == "End":
                        End(self.group, top_left_position)

                    elif object_type == "Checkpoint":
                        CheckPoint(self.group, top_left_position)

                    elif object_type == "Arrow":
                        Arrow(
                            self.group,
                            top_left_position,
                            arrow_type=properties["arrow_type"],
                            side=properties["side"]
                        )

                    elif object_type == "Text":
                        Text(
                            self.group,
                            top_left_position,
                            scaled_image
                        )


                    elif object_type == "Trampoline":
                        Trampoline(self.group, top_left_position, direction=properties["direction"])

                    elif object_type == "Fruit":
                        Fruit(self.group, top_left_position, properties["fruit_type"])

                    elif object_type == "Coin":
                        Coin(self.group, top_left_position, properties["coin_type"])

                    elif object_type == "Gem":
                        Gem(self.group, top_left_position, properties["gem_type"])

                    elif object_type == "PassableBottomTile":
                        PassableBottomTile(self.group, top_left_position, scaled_image, layer=0)

                    elif object_type == "AnimatedTile":
                        AnimatedTile(self.group, top_left_position, properties["animated_type"])

                    else:
                        StaticTile(self.group, top_left_position, scaled_image, layer=i)

            elif isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    top_left_position = obj.x * self.scene.scale, obj.y * self.scene.scale
                    if obj.type == "Player":
                        player_type = "Virtual Guy" if not hasattr(obj, "player_type") else obj.player_type
                        self.player = NinjaFrog(self.group, player_type, top_left_position, top_left_position)

                    elif obj.type == "MovingSaw":
                        start_index = 0 if not hasattr(obj, "start_index") else obj.start_index
                        MovingSaw(self.group, *get_points(obj), draw_path=obj.draw_path, start_index=start_index)

                    elif obj.type == "Fruit":
                        Fruit(self.group, top_left_position, "Apple")

                    elif obj.type == "Pendulum":
                        EnemyPendulum(self.group, top_left_position, obj.length * self.scene.scale)

                    elif obj.type == "Head":
                        HeadEnemy(self.group, top_left_position, get_points(obj), obj.head_type, obj.start_point_index)

                    elif obj.type == "Wind":
                        Wind(self.group, get_rect(obj))

            elif isinstance(layer, pytmx.TiledImageLayer):
                name = layer.source.split("/")[-1]
                path = f"data/Assets/Free/Background/Big Scale/{name}"
                self.background = MovingBackground(
                    pygame.image.load(path).convert()
                )

        self.player_state = PlayerState(self.player, self.player.position)
