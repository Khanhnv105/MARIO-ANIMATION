from data.engine.UI.elements.pixelart.pixelart_font import PixelartFont
from data.scripts.ui.text_button import TextButton


class ToggleButton(TextButton):
    """
    Boton que le agrega al texto el estado del mismo
    tiene dos estados On - Off
    """
    def __init__(self, name, text, pos, color, start_on=True):
        self.state = not start_on
        self.BASE_TEXT = text
        super().__init__(name, text, pos, color)

        self._toggle_state()

    def _toggle_state(self):
        self.state = not self.state
        text = self.BASE_TEXT + (" - On" if self.state else " - Off")
        self.font = PixelartFont(text, 2, f"data/Assets/Free/Menu/Text/Text (Black) (8x10).png", 8, 10)
        self._render_image()

    def get_state(self) -> bool:
        return self.state

    def pressed(self):
        super().pressed()
        self._toggle_state()

    def draw(self, surface, top_left_root):
        super().draw(surface, top_left_root)
