import pygame
import pytmx

from ..tile.tile import Tile
import math

from ...constants import MAPS_PATH


def get_visible_positions(scroll, zoom, tiles_size, display_size):
    """Retorna todas las posiciones de los tiles visibles"""
    top_left_corner = (scroll[0] / zoom) // tiles_size[0], (scroll[1] / zoom) // tiles_size[1]

    amount_visible_x = math.ceil((display_size[0] / zoom) / tiles_size[0])
    amount_visible_y = math.ceil((display_size[1] / zoom) / tiles_size[1])

    visible = []

    for x in range(amount_visible_x + 1):
        for y in range(amount_visible_y + 1):
            visible.append((top_left_corner[0] + x, top_left_corner[1] + y))

    return visible


def get_start_end_visible(scroll, zoom, tiles_size, display_size):
    """Retorna todas las posiciones de los tiles visibles"""
    top_left_corner = (scroll[0] / zoom) // tiles_size[0], (scroll[1] / zoom) // tiles_size[1]

    amount_visible_x = math.ceil((display_size[0] / zoom) / tiles_size[0]) + 1
    amount_visible_y = math.ceil((display_size[1] / zoom) / tiles_size[1]) + 1

    return top_left_corner, (top_left_corner[0] + amount_visible_x, top_left_corner[1] + amount_visible_y)


class TilesManager:
    def __init__(self, scene, map: str, scroll: tuple, zoom: float, scale=1):
        self.scene = scene
        self.scale = scale
        self.tiles = {}
        self.visible_tiles = {}
        self.tiles_images = []
        self.TILES_IMAGES = []
        self.visible_positions = []
        self.tiled_map = pytmx.load_pygame(MAPS_PATH + map)

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
        self.set_binary_grid()

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

    def load_tiles(self, scroll, zoom):
        self.tiles.clear()
        self.visible_tiles.clear()
        self.tiles_images = []

        for layer in self.tiled_map:

            self.tiles[layer.name] = {}

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
                tile = Tile(x_grid_pos=x, y_grid_pos=y, image=image)
                self.tiles[layer.name][x, y] = tile

        self.scroll_changed(scroll, zoom)

        self.TILES_IMAGES = self.tiles_images.copy()

    def scroll_changed(self, scroll, zoom):
        """
        Reinicia la lista de tiles visibles,
        crea de nuevo cada uno de los layers
        y verifica la visibilidad de cada uno
        de los Tiles()
        """
        visible_positions = get_visible_positions(scroll, zoom, self.TILE_SIZE, self.scene.director.DISPLAY_SIZE)
        # wvisible_rect = get_start_end_visible(scroll, zoom, self.TILE_SIZE, self.scene.director.DISPLAY_SIZE)
        # Si es que ahora se pueden ver mas tiles
        if visible_positions != self.visible_positions:

            self.visible_tiles = {}

            for layer in self.tiles:
                self.visible_tiles[layer] = {}
                visible_in_layer = [position for position in visible_positions if position in self.tiles[layer]]

                for visible_position in visible_in_layer:
                    self.visible_tiles[layer][visible_position] = self.tiles[layer][visible_position]
                    self.tiles[layer][visible_position].scroll_changed(scroll, zoom)
                    self.tiles[layer][visible_position].zoom_changed(scroll, zoom)

            self.visible_positions = visible_positions

        # Si es que los tiles son los mismos que antes
        else:
            for layer in self.visible_tiles:
                for tile in self.visible_tiles[layer].values():
                    tile.scroll_changed(scroll, zoom)

    def zoom_changed(self, scroll, zoom):
        self.scroll_changed(scroll, zoom)

    def update(self, dt, mouse, scroll):
        pass

    def draw(self, surface):
        """Dibujo capa a capa cada uno de los tiles visibles"""

        for layer in self.visible_tiles:
            for position in self.visible_tiles[layer]:
                self.visible_tiles[layer][position].draw(surface)
