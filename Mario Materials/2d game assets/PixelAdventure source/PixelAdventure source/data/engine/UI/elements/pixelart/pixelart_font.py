import pygame

from data.engine.image.editor import scale_image, crop_image


class PixelartFont(pygame.Surface):
    """Single line Font, pixelart"""

    def __init__(self, text, scale, font_path, single_width, single_height, fill_color=None):
        self._text = text
        self._path = font_path
        self._CHARACTER_WIDTH = single_width
        self._CHARACTER_HEIGHT = single_height
        self._single_width = single_width * scale
        self._single_height = single_height * scale
        self._scale = scale
        self._fill_color = fill_color
        self._SET = pygame.image.load(font_path).convert_alpha()
        self._set = scale_image(self._SET, self._scale)

        size = self._single_width * len(text), self._single_height
        if not fill_color:
            super().__init__(size, pygame.SRCALPHA)
        else:
            super().__init__(size)

        self.set_text(text)

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text

        if self._fill_color:
            self.fill(self._fill_color)
        else:
            self.fill((0, 0, 0))
            self.set_colorkey((0, 0, 0))

        self._render()

    def blit_centered(self, surface, central_position):
        surface.blit(
            self,
            (
                central_position[0] - self.get_width() // 2,
                central_position[1] - self.get_height() // 2
            )
        )

    def _render(self):
        """Retorna una imagen en base al texto"""

        order = {
            "A": (0, 0), "B": (1, 0), "C": (2, 0),
            "D": (3, 0), "E": (4, 0), "F": (5, 0),
            "G": (6, 0), "H": (7, 0), "I": (8, 0),
            "J": (9, 0), "K": (0, 1), "L": (1, 1),
            "M": (2, 1), "N": (3, 1), "O": (4, 1),
            "P": (5, 1), "Q": (6, 1), "R": (7, 1),
            "S": (8, 1), "T": (9, 1), "U": (0, 2),
            "V": (1, 2), "W": (2, 2), "X": (3, 2),
            "Y": (4, 2), "Z": (5, 2), "0": (0, 3),
            "1": (1, 3), "2": (2, 3), "3": (3, 3),
            "4": (4, 3), "5": (5, 3), "6": (6, 3),
            "7": (7, 3), "8": (8, 3), "9": (9, 3),
            ".": (0, 4), ",": (1, 4), ":": (2, 4),
            "?": (3, 4), "!": (4, 4), "(": (5, 4),
            ")": (6, 4), "+": (7, 4), "-": (8, 4),
            " ": (9, 2)
        }

        for index, word in enumerate(self._text):
            x, y = order[word.upper()]
            rect = pygame.Rect(
                x * self._CHARACTER_WIDTH,
                y * self._CHARACTER_HEIGHT,
                self._CHARACTER_WIDTH,
                self._CHARACTER_HEIGHT
            )
            self.blit(
                scale_image(
                    crop_image(
                        self._SET, rect
                    ),
                    self._scale
                ),
                (
                    index * self._single_width,
                    0
                )
            )
