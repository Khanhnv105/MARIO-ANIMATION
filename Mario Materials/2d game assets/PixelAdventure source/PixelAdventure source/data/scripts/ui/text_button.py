from data.engine.UI.elements.key_controllable_button import KeyControllableButton
from data.engine.UI.elements.pixelart.pixelart_font import PixelartFont
import pygame


class TextButton(KeyControllableButton):
    def __init__(self, name, text, pos, color):
        self.font = PixelartFont(text, 2, f"data/Assets/Free/Menu/Text/Text ({color}) (8x10).png", 8, 10)
        self._render_image()

        super().__init__(name, pos, "", 1, load_image=False)

    def set_text(self, text: str):
        self.font.set_text(text)
        self._render_image()

    def _render_image(self):
        left = pygame.transform.scale(pygame.image.load("data/Assets/Free/Menu/Base Button/left.png"), (8, 80))
        right = pygame.transform.scale(pygame.image.load("data/Assets/Free/Menu/Base Button/right.png"), (8, 80))

        surface = pygame.Surface(
            (
                left.get_width() + right.get_width() + self.font.get_width(),
                left.get_height()
            ),
            pygame.SRCALPHA
        )
        middle = pygame.image.load("data/Assets/Free/Menu/Base Button/middle.png")
        width = surface.get_width() - (left.get_width() + right.get_width())
        middle = pygame.transform.scale(middle, (width, surface.get_height()))

        surface.blit(middle, (left.get_width(), 0))
        surface.blit(left, (0, 0))
        surface.blit(right, (surface.get_width() - right.get_width(), 0))
        surface.blit(self.font, (surface.get_width() // 2 - self.font.get_width() // 2, surface.get_height() // 2 - self.font.get_height() // 2))
        self.image = surface.convert_alpha().copy()
        self.IMAGE = self.image.copy()