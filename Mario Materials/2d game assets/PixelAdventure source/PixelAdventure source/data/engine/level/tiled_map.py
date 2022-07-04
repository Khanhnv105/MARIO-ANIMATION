import pygame
import pytmx

from ..tile.tile import Tile


class TiledMap:
    def __init__(self, tmx_file_path: str):
        self.tmx_file_path = None
        self._map = None

        # Tiles storage
        self.tiles = {}
        self.visible_tiles = []
        self.tiles_images = []
        self.TILES_IMAGES = []

        # Loading tiles
        self.load_tiles(tmx_file_path)

    def load_tiles(self, path):
        self.tmx_file_path = path
        self._map = pytmx.load_pygame(path)
        self.tiles = {}
        for layer in self._map:
            self.tiles[layer] = []

            for x, y, image in layer.tiles():
                if image not in self.tiles_images:
                    self.tiles_images.append(image)

                self.tiles[layer].append(
                    Tile(
                        x_grid_pos=x,
                        y_grid_pos=y,
                        images=self.tiles_images,
                        image_index=self.tiles_images.index(image)
                    )
                )
        self.TILES_IMAGES = self.tiles_images.copy()
        self.visible_tiles = {}
        display_surface = pygame.display.get_surface()
        display_rect = pygame.Rect(0, 0, display_surface.get_width(), display_surface.get_height())
        for layer in self.tiles:

            self.visible_tiles[layer] = []

            for tile in self.tiles[layer]:
                if tile.is_visible(display_rect):
                    self.visible_tiles[layer].append(tile)

    def zoom_changed(self, scroll, zoom, display_rect):

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
        self.scroll_changed(scroll, zoom, display_rect)

    def scroll_changed(self, scroll, zoom, display_rect):
        """Cuando cambia el scroll"""

        self.visible_tiles = {}
        for layer, tiles in self.tiles.items():
            self.visible_tiles[layer] = []
            for tile in tiles:
                tile.camera_moved(scroll, zoom, self.tiles_images)
                if tile.is_visible(display_rect):
                    self.visible_tiles[layer].append(tile)

    def update(self, zoom, scroll):
        for layer in self.visible_tiles:
            for tile in self.visible_tiles[layer]:
                tile.update(images=self.tiles_images, zoom=zoom, scroll=scroll)

    def draw(self, surface):
        for layer in self.visible_tiles:
            for tile in self.visible_tiles[layer]:
                tile.draw(surface)
