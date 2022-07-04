from typing import List, Tuple
import os
import pygame

from ..image.editor import scale_image, crop_image


def load_tile(path, scale, colorkey):
    """Carga un unico tile"""
    tile = pygame.image.load(path)

    if scale != 1:
        tile = scale_image(tile, scale).convert_alpha()
    if colorkey:
        tile.set_colorkey(colorkey)

    return tile


def load_tileset(
        path: str,
        columns: int,
        rows: int,
        tile_width: int,
        tile_height: int,
        colorkey: Tuple[int, int, int] = (255, 255, 255),
        scale: float = 1,
        starting_pos: Tuple[int, int] = (0, 0)
) -> List[List[pygame.Surface]]:
    """
    Retorna una lista de imagenes recortadas del tileset
    @param -> path: Ruta relativa en la cual se encuentra el set
    @param -> tile_size: Tamaño de las imagenes
    @param -> starting_pos: Posicion desde la cual se empieza
                            a recortar el tileset
    @param -> split_rows: Se usa en el caso de que se quiera
                          obtener diferentes listas, separando
                          las filas
    @param -> split_columns: split_rows pero con las columnas
    """

    tileset = pygame.image.load(path)
    tiles = []

    for y in range(rows):
        tiles.append([])
        for x in range(columns):

            cropped_image = crop_image(
                tileset,
                pygame.Rect(
                    starting_pos[0] + x * tile_width,
                    starting_pos[1] + y * tile_height,
                    tile_width,
                    tile_height
                )
            )

            scaled_image = scale_image(cropped_image, scale).convert_alpha()
            if colorkey:
                scaled_image.set_colorkey(colorkey)

            tiles[y].append(scaled_image)

    return tiles


def load_folder(path: str, colorkey=(255, 255, 255), scale=1, sorted_images=False, image_extension=".png") -> List[pygame.Surface]:
    """
    Carga todas las imagenes ubicadas en una carpeta y las retorna.
    En el caso de que sean ordenadas las imagenes deben llamarse
    por numeros, por ejemplo: 1.png, 2.png.
    """

    if sorted_images:
        # Ordena la lista numericamente, para eso borra el prefijo

        images_numbers = sorted([int(name.replace(image_extension, "")) for name in os.listdir(path)])
        images = []
        for image_number in images_numbers:
            image = load_tile(path + f"/{image_number}{image_extension}", scale, colorkey)
            images.append(image)

        return images

    else:
        # Carga todas las imagenes en la
        # carperta in importar el orden
        images = []
        for image_name in os.listdir(path):
            image = load_tile(path + f"/{image_name}", scale, colorkey)
            images.append(image)

        return images
