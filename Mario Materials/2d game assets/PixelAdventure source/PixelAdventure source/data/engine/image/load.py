import os

import pygame

from data.engine.image.editor import scale_image, crop_image
from data.engine.tile.tile_set_loader import load_folder, load_tileset


def load(path: str, colorkey=None, scale=None, convert=False):
    image = pygame.image.load(path)
    if scale:
        image = scale_image(image, scale)
    if colorkey:
        image.set_colorkey(colorkey)
    if convert:
        return image.convert()

    return image.convert_alpha()

def load_images_set(path: str, single_width: int, single_height: int, colorkey=None, scale=None, convert=False):
    set = pygame.image.load(path)

    set_width = set.get_width()
    set_height = set.get_height()

    rows = set_height // single_height
    columns = set_width // single_width

    images = []

    for row in range(rows):
        images.append([])
        for col in range(columns):

            rect = pygame.Rect(col * single_width, row * single_height, single_width, single_height)
            image = crop_image(set, rect)

            if scale:
                image = pygame.transform.scale(image, (int(single_width * scale), int(single_height * scale)))

            if colorkey:
                image.set_colorkey(colorkey)

            if convert:
                image = image.convert()

            images[-1].append(image)

    return images


def transform_set_to_folder(path: str, single_width: int, single_height: int, colorkey=None, scale=None, convert=False):
    images = load_images_set(path, single_width, single_height, colorkey, scale, convert)
    folder_name = path.split("/")[-1][:-4]

    folder_location = path.replace(path.split("/")[-1], folder_name)
    os.mkdir(folder_location)
    for row in images:
        for i, image in enumerate(row):
            pygame.image.save(image, folder_location + f"/{i}.png")

