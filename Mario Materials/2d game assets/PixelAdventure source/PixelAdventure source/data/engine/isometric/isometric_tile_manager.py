import math
from random import randint

import pygame
import pytmx

from .core import mouse_to_cartesian
from .isometric_tile import IsometricTile
from ..management.scene import Scene
from ..path_calculator.a_star_path_finding import AStarPathFinding
from ..tile.tile_set_loader import load_tile


class IsometricTilesManager:
    def __init__(self, scene: Scene, map_path: str, scroll: tuple, zoom: float, scale=3):
        self.scene = scene
        self.scale = scale
        self.tiles = {}
        self.visible_tiles = {}
        self.tiles_images = []
        self.TILES_IMAGES = []

        self.tiled_map = pytmx.load_pygame(map_path)

        self.grid = []
        for y in range(self.tiled_map.height):
            self.grid.append([])
            for x in range(self.tiled_map.width):
                self.grid[y].append(0)

        for layer in self.tiled_map:
            for tile in layer.tiles():
                self.grid[tile[1]][tile[0]] = 1
            break

        # Ancho y alto de Grid
        self.TILE_SIZE = (
            int(self.tiled_map.tilewidth * self.scale),
            int(self.tiled_map.tileheight * self.scale)
        )

        self.GRID_SIZE = self.tiled_map.width, self.tiled_map.height

        self.load_tiles(scroll, zoom)

        self.over_image = load_tile("assets/sprites-natural/hovered_animation/over_tile1.png", scale, None)
        img = pygame.image.load("assets/sprites-natural/hovered_animation/over_tile1.png")
        self.over_image = pygame.transform.scale(
            img,
            (
                int(img.get_width() * scale),
                int(img.get_height() * scale)
            )
        )
        self.binary_grid = []
        self.set_binary_grid()
        self.path_finder = AStarPathFinding(self.binary_grid)

    def set_binary_grid(self):

        """
        Actualiza el array binario en el cual se basa el PathFinding del player.
        Asume que el layer 0 define los bordes del mapa por lo que los agrega como bordes.
        Y tambien asume que en layer[1] se encuentran las paredes y principales objetos para
        colisionar
        """

        # Posibles estados de los nodos
        COLLIDEABLE = 1
        NON_COLLIDEABLE = 0
        # Layers los cuales se toman en cuenta para la colision
        COLLIDEABLE_LAYERS_INDEXES = [1]
        BASE_LAYER_INDEX = 0
        # Nombre de los layers
        LAYERS_NAMES = [layer.name for layer in self.tiled_map.layers]

        # grid toda inicializada como COLLIDEABLE
        grid = [[COLLIDEABLE for _ in range(self.tiled_map.width)] for _ in range(self.tiled_map.height)]

        """
        Busco todos los nodos 'base' o del 'piso' del layer correspondiente
        en sus posiciones establezco a grid para que no se pueda colisionar
        """
        for position in self.tiles[LAYERS_NAMES[BASE_LAYER_INDEX]]:
            x = position[0] + BASE_LAYER_INDEX
            y = position[1] + BASE_LAYER_INDEX
            grid[y][x] = NON_COLLIDEABLE

        """Busco los nodos con los cuales se puede colisionar y actualizo grid"""
        for index in COLLIDEABLE_LAYERS_INDEXES:

            layer_name = LAYERS_NAMES[index]
            for position in self.tiles[layer_name]:
                x = position[0] + index
                y = position[1] + index

                if x < len(grid[0]) and y < len(grid):
                    grid[y][x] = COLLIDEABLE

        self.binary_grid = grid

    def get_display_rect(self):
        return pygame.Rect(
            0, 0,
            self.scene.director.SIZE[0],
            self.scene.director.SIZE[1]
        )

    def load_tiles(self, scroll, zoom):
        self.tiles.clear()
        self.visible_tiles.clear()
        self.tiles_images = []

        display_rect = self.get_display_rect()

        for layer in self.tiled_map:

            self.tiles[layer.name] = {}
            self.visible_tiles[layer.name] = {}

            for x, y, image in layer.tiles():

                # Si es que es una nueva imagen
                if image not in self.tiles_images:
                    image = pygame.transform.scale(
                        image,
                        (
                            int(image.get_width() * self.scale),
                            int(image.get_height() * self.scale)
                        )
                    ).convert_alpha()
                    self.tiles_images.append(image)

                tile = IsometricTile(
                    x_grid_pos=x,
                    y_grid_pos=y,
                    z_grid_pos=randint(0, 1),
                    images=self.tiles_images,
                    image_index=self.tiles_images.index(image),
                    grid_size=self.TILE_SIZE,
                    zoom=zoom,
                    scroll=scroll,
                    display_rect=display_rect
                )
                self.tiles[layer.name][x, y] = tile
                if tile.visible:
                    self.visible_tiles[layer.name][x, y] = tile

        self.TILES_IMAGES = self.tiles_images.copy()

    def zoom_changed(self, scroll, zoom):
        self.tiles_images.clear()
        for image in self.TILES_IMAGES:
            self.tiles_images.append(
                pygame.transform.scale(
                    image,
                    (
                        int(image.get_width() * zoom),
                        int(image.get_height() * zoom)
                    )
                )
            )
        self.scroll_changed(scroll, zoom)

    def scroll_changed(self, scroll, zoom):
        """
        Reinicia la lista de tiles visibles,
        crea de nuevo cada uno de los layers
        y verifica la visibilidad de cada uno
        de los IsometricTiles()
        """

        display_rect = self.get_display_rect()
        self.visible_tiles = {}

        for layer in self.tiles:
            self.visible_tiles[layer] = {}
            for position, tile in self.tiles[layer].items():
                tile.camera_moved(scroll, zoom, display_rect)
                if tile.visible:
                    self.visible_tiles[layer][position] = tile

    def update(self, dt, mouse, scroll):
        for layer in self.visible_tiles:
            for position, tile in self.visible_tiles[layer].items():
                tile.update(dt=dt)

        self.position = mouse_to_cartesian(
            mouse,
            scroll,
            self.TILE_SIZE[0],
            self.TILE_SIZE[1]
        )
        if self.position in self.tiles["ground"]:
            self.tiles["ground"][self.position].mouse_over = True

    def draw(self, surface):
        """Dibujo capa a capa cada uno de los tiles visibles"""

        for layer in self.visible_tiles:
            for position in self.visible_tiles[layer]:
                self.visible_tiles[layer][position].draw(surface)
    
        if self.position in self.tiles["ground"]:
            surface.blit(
                self.over_image,
                self.tiles["ground"][self.position].display_position
            )

    def draw_grid(self, surface):
        """Dibujo capa a capa cada uno de los tiles visibles"""
        w = h = 10
        for y, row in enumerate(self.binary_grid):
            for x, number in enumerate(row):
                if number:
                    pygame.draw.rect(surface, (100, 100, 100), (x * w, y * h, w, h))
                else:
                    pygame.draw.rect(surface, (0, 0, 0), (x * w, y * h, w, h))

                pygame.draw.rect(surface, (112, 112, 112), (x * w, y * h, w, h), 1)
