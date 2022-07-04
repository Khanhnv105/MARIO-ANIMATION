import pygame

from ..entity.entity import Entity
from .core import cartesian_to_isometric
from ..math.vector import Vector


class IsometricEntity(Entity):
    def __init__(
            self,
            grid_x: int,
            grid_y: int,
            tile_width: int,
            entity_width: int,
            entity_height: int,
            groups: pygame.sprite.AbstractGroup,
            image=None
    ):
        super().__init__(
            x=grid_x * tile_width,
            y=grid_y * tile_width,
            width=entity_width,
            height=entity_height,
            groups=groups,
            image=image
        )
        self.display_position = 0, 0
        self.set_draw_method(self.draw_method)

    def update_display_position(self, scroll: tuple, zoom: float):
        isometric = cartesian_to_isometric(self.position.x, self.position.y)
        self.display_position = isometric[0] * zoom - scroll[0], isometric[1] * zoom - scroll[1]

    def draw_method(self, surface):
        surface.blit(
            self.image,
            self.display_position
        )

    def key_pressed(self, keys):
        self.velocity = Vector(0,  0)
        if keys[pygame.K_w]:
            self.velocity.y -= 3
        if keys[pygame.K_s]:
            self.velocity.y += 3
        if keys[pygame.K_d]:
            self.velocity.x += 3
        if keys[pygame.K_a]:
            self.velocity.x -= 3

    def update(self, *args, **kwargs) -> None:
        self.position += self.velocity * kwargs["dt"]
        self.update_display_position(kwargs["scroll"], kwargs["zoom"])
        self.rect.x, self.rect.y = self.display_position
