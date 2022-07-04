from data.engine.animation.sprite_animation.single_animation_controller import SingleAnimationController
from data.engine.entity.image_collideable_entity import ImageCollideableEntity
from data.engine.math.vector import Vector
from data.scripts.map.enemies.enemy import Enemy
from data.scripts.utils import dynamic_animation_creation


class Spike(ImageCollideableEntity, Enemy):

    def __init__(self, group, position, side="bottom"):
        self.animator = SingleAnimationController(dynamic_animation_creation(f"data/Assets/Free/Traps/Spikes/idle_{side}", images_scale=2, delay=6))
        super().__init__(group, position, self.animator.get_image(), mode="static", layer=1)

    def get_position(self):
        return Vector(self.rectangle.center[0], self.rectangle.center[1])

    def update(self, **kwargs) -> None:
        self.animator.update(kwargs["dt"])
        self.image = self.animator.get_image()

    def draw(self, surface, offset=(0, 0)):
        surface.blit(
            self.image,
            (
                self.rectangle.x - offset[0],
                self.rectangle.y - offset[1]
            )
        )
