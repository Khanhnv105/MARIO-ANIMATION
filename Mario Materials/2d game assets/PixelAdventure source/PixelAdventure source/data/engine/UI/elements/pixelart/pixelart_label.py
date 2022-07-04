import pygame
from data.engine.UI.element import Element
from .pixelart_font import PixelartFont


class PixelartLabel(Element):
    def __init__(self, name, text, scale, color, pos, centered=False):
        self.font = PixelartFont(text, scale, f"data/Assets/Free/Menu/Text/Text ({color}) (8x10).png", 8, 10)

        if centered:
            pos = pos[0] - self.font.get_width() // 2, pos[1] - self.font.get_height() // 2

        rect = pygame.Rect(pos[0], pos[1], self.font.get_width(), self.font.get_height())
        super().__init__(name, rect)

    def set_text(self, text):
        self.font.set_text(text)

    def update(self, **kwargs):
        pass

    def draw(self, surface, top_left_root):
        surface.blit(
            self.font,
            (
                self.rect.x + top_left_root[0],
                self.rect.y + top_left_root[1]
            )
        )
