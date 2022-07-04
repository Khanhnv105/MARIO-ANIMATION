from data.engine.UI.element import Element
from data.engine.UI.elements.pixelart.pixelart_label import PixelartLabel


class DoublePixelartLabel(Element):
    """Label que tiene otra por debajo"""
    def __init__(
            self,
            name,
            text,
            scale,
            color1,
            color2,
            pos,
            centered=False,
            offset=5
    ):
        self.offset = offset
        self.label1 = PixelartLabel(
            name + "label1",
            text,
            scale,
            color1,
            pos,
            centered
        )
        self.label2 = PixelartLabel(
            name + "label2",
            text,
            scale,
            color2,
            (
                pos[0] + self.offset,
                pos[1] + self.offset
            ),
            centered
        )
        super().__init__(
            name,
            (
                pos[0],
                pos[1],
                self.label2.font.get_width() + self.offset,
                self.label2.font.get_height() + self.offset,
            )
        )
    def set_text(self, text):
        self.label1.set_text(text)
        self.label2.set_text(text)

    def draw(self, surface, top_left_root):
        self.label2.draw(surface, top_left_root)
        self.label1.draw(surface, top_left_root)