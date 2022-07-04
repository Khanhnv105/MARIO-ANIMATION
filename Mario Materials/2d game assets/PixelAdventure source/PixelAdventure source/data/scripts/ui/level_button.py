from data.engine.UI.elements.key_controllable_button import KeyControllableButton
from data.engine.UI.elements.pixelart.pixelart_font import PixelartFont
from data.engine.tile.tile_set_loader import load_tile


class LevelButton(KeyControllableButton):
    def __init__(self, name, position, path_unlocked, path_locked, image_scale=2, points=None, unlocked=False):
        super().__init__(
            name,
            position,
            path_unlocked,
            image_scale
        )
        self.locked_image = load_tile(path_locked, image_scale, None)
        self.unlocked_image = load_tile(path_unlocked, image_scale, None)
        self.unlocked = unlocked
        self.image = self.unlocked_image if unlocked else self.locked_image
        self.selectable = self.unlocked

        if points:
            surface = PixelartFont(str(points), 2, f"data/Assets/Free/Menu/Text/Text (White) (8x10).png", 8, 10)
            self.unlocked_image.blit(surface, (10, self.image.get_height() - 20 - surface.get_height()))


    def update(self, **kwargs):
        if self.selected:
            self.apply_filter(
                self.unlocked_image if self.unlocked else self.locked_image,
                kwargs["clock_ticks"] / 100
            )

        else:
            self.image = self.unlocked_image if self.unlocked else self.locked_image
