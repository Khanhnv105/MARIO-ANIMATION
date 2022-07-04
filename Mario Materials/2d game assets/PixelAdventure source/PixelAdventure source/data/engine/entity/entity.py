

class Entity:
    """TODO Clase base para tipo de entidad dentro del juego"""

    def __init__(
            self,
            group=None,
            visible=False,
            layer=0
    ):

        self._visible = visible
        self._layer = layer
        self._deleting = False
        if group is not None:
            group.add(self)

        if visible:
            group.set_visible(True, self)

        self.group = group

    def is_visible(self) -> bool:
        return self._visible

    def set_visible(self, state: bool):
        self._visible = state

    def get_layer(self) -> int:
        return self._layer

    def set_layer(self, layer: int) -> None:
        self._layer = layer

    def delete(self):
        
        if not self._deleting:
            self._deleting = True
            """Ejecuta el comando para ser eliminada"""
            self.group.delete(self)

    def deleting(self, scene):
        """
        Ultima llamada a la entidad en la cual se
        pasan por parametro la escena del juego
        para poder acceder a cualquier propiedad.
        Ej:
        Esto puede servir para acceder al manager
        de partuculas o poder alterar cualquier estado
        del juego
        """

    def update(self, **kwargs) -> None:
        """"""

    def draw(self, surface, offset=(0, 0)):
        """"""
