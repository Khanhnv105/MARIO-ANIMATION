import pygame

from data.engine.UI.element import Element
from data.engine.image.load import load


class Button(Element):
    def __init__(self, name, position, image_path, image_scale=1, colorkey=None, center=False, load_image=True):
        self.selectable = True
        if load_image:
            self.image = load(image_path, colorkey, image_scale)

        if center:
            rect = pygame.Rect(
                position[0] - self.image.get_width() // 2,
                position[1] - self.image.get_height() // 2,
                self.image.get_width(),
                self.image.get_height()
            )
        else:

            rect = pygame.Rect(
                position[0],
                position[1],
                self.image.get_width(),
                self.image.get_height()
            )
        super().__init__(name, rect)

    def set_selectable(self, state):
        self.selectable = state

    @property
    def width(self):
        return self.image.get_width()

    @property
    def height(self):
        return self.image.get_height()

    def draw(self, surface, top_left_root):
        pos = self.rect.x + top_left_root[0], self.rect.y + top_left_root[1]
        surface.blit(self.image, pos)

    def pressed(self):
        self._post_clicked()
