import pygame

from .collideable_entity import CollideableEntity
from .entities_group import EntitiesGroup
from ..collisions.collisions_manager import CollisionsManager


class CollideableEntitiesGroup(EntitiesGroup):
    """
    Grupo que cuenta con un QuadTree y es compatible con
    la ColldableEntity class y subclases.
    """

    def __init__(self, game_scene, map_size):
        super().__init__(game_scene)
        self.collisions_manager = CollisionsManager(map_size)
        self.static_objects = []
        self.dynamic_objects = []

    def clear(self):
        self.static_objects.clear()
        self.dynamic_objects.clear()
        super().clear()

    def add(self, entity: CollideableEntity) -> None:
        super().add(entity)
        if entity.mode == "static":
            self.static_objects.append(entity)
            self.collisions_manager.add_static_object(entity)
        else:
            self.dynamic_objects.append(entity)

    def delete(self, entity: CollideableEntity) -> None:
        super().delete(entity)
        if entity.mode == "dynamic":
            self.dynamic_objects.remove(entity)
        else:
            self.static_objects.remove(entity)

    def update(self, **kwargs):
        super().update(**kwargs)
        self.collisions_manager.update(objects=self.dynamic_objects)
        self.change_visible_dict(self._get_visible_entities(kwargs["display_rect"]))

    def draw(self, surface: pygame.Surface, offset=(0, 0)):
        super().draw(surface, offset)
        # self.collisions_manager.quad_tree.draw(surface, thickness=4, offset=offset)
        # self.collisions_manager.static_quad_tree.draw(surface, color=(250, 50, 50), offset=offset)

    def _get_visible_entities(self, display_rect):
        """
        Este metodo retorna todas las entidades que se encuenten visibles
        usando tanto el Quad Tree estatico como el dinamico.
        Display rect es el rectangulo que representa a la posicion de la
        pantalla en el juego
        """
        dynamic_visible = self.collisions_manager.quad_tree.query(display_rect)
        static_visible = self.collisions_manager.static_quad_tree.query(display_rect)

        if dynamic_visible and static_visible:
            return dynamic_visible + static_visible

        if dynamic_visible:
            return dynamic_visible

        if static_visible:
            return static_visible

        return []