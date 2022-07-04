from .particles_manager import ParticlesManager
from ..math.vector import Vector


class Particle:
    """
    Clase base de particula la cual
    determina las propiedades indispensables
    de la misma
    """

    def __init__(self, manager: ParticlesManager, position, layer=0):
        self._layer = layer
        self._manager = manager
        self._manager.add(self)
        self.position = Vector(position[0], position[1])
        self.image = None

    def get_layer(self) -> int:
        return self._layer

    def destroy(self):
        self._manager.destroy(self)

    def update(self, **kwargs):
        pass

    def draw(self, surface, offset=(0, 0)):
        pass