from math import sin

import pygame
from pygame.sprite import Sprite

from data.engine.UI.elements.button import Button
from data.engine.tile.tile_set_loader import load_tile


def get_rgb(direction: float, alpha=255):
    return pygame.Color(
        int((1 + sin(direction)) * 0.5 * 255),
        int((1 + sin(direction + 2)) * 0.5 * 255),
        int((1 + sin(direction + 4)) * 0.5 * 255),
        alpha
    )


class KeyControllableButton(Button):
    """
    KeyControllableButton es un tipo de boton
    diseñado especificamente para que sea
    interactauble mediante las teclas, es decir
    que no tiene un metodo para hacer colisiones
    con el mouse
    """
    selected = False

    def __init__(
            self,
            name: str,
            position,
            image_path,
            image_scale=1,
            colorkey=None,
            center=False,
            load_image=True
    ):
        Button.__init__(
            self,
            name,
            position,
            image_path,
            image_scale,
            colorkey,
            center,
            load_image
        )
        self.IMAGE = self.image.copy()

    def update(self, **kwargs):
        if self.selected and self.selectable:
            self.apply_filter(self.IMAGE, kwargs["clock_ticks"] / 100)

    def set_selected(self, state: bool):
        self.selected = state
        if not state:
            self.image = self.IMAGE.copy()

    def draw(self, surface, top_left_root):
        super().draw(surface, top_left_root)

    def apply_filter(self, base, amount, rgb=True):
        """Applies a filter color to the surface obtained from the image mask"""
        self.image = base.copy()
        self.image.blit(
            pygame.mask.from_surface(self.image).to_surface(
                setcolor=get_rgb(amount, alpha=150) if rgb else rgb,
                unsetcolor=(0, 0, 0, 0)
            ),
            (0, 0)
        )