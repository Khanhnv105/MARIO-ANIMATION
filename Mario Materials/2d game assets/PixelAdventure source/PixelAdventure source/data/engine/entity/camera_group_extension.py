from data.engine.entity.collideable_entities_group import CollideableEntitiesGroup


class CameraCollideableGroup(CollideableEntitiesGroup):
    def draw(self, surface, offset):
        offset_x = offset[0]
        offset_y = offset[1]

        for layer in self.get_visible_entities_layered(sort=True):
            for entity in self._visible_entities[layer]:
                surface.blit(
                    entity.image,
                    (
                            entity.rectangle.x - offset_x,
                            entity.rectangle.y - offset_y
                    )
                )

    """"def update(self, **kwargs):
        for layer in self._visible_entities:
            for entity in self._visible_entities[layer]:
                entity.update(**kwargs)"""

