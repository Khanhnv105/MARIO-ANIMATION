import pytmx


class Layer(pytmx.TiledTileLayer):
    def __init__(self, parent, node):
        super().__init__(parent, node)