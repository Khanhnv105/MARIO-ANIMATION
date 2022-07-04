from data.engine.collisions.collideable import Collideable
from data.engine.entity.entity import Entity


class CollideableEntity(Entity, Collideable):
    """
    CollideableEntity es una clase compatible
    con el QuadTree y CollisionsManager,
    la cual basa sus coliisones en rectangulos.
    """

    def __init__(self, group, rectangle, visible=True, layer=0, mode="dynamic"):
        self.mode = mode
        Collideable.__init__(self, group.collisions_manager, rectangle)
        Entity.__init__(self, group, visible=visible, layer=layer)

    def collides(self, other) -> bool:
        """Colision de rectangulos"""
        return self.rectangle.colliderect(other.rectangle)

    def query(self, rectangle):
        """Retorna todos los objetos con los cuales colisione el rectangulo"""
        return self.collisions_manager.quad_tree.query(rectangle)
