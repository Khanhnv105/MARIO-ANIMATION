from math import sin
from data.scripts.map.collectable.collectable import Collectable
from data.scripts.particles.GameParticle import GameParticle
from data.scripts.utils import dynamic_animation_creation


class Fruit(Collectable):
    def __init__(self, group, pos, fruit_type):
        super().__init__(
            collideable_group=group,
            center_position=pos,
            animation_data=dynamic_animation_creation(f"data/Assets/Free/Items/Fruits/{fruit_type}", images_scale=2)
        )
        self.START_Y = self.rectangle.y

    def update(self, **kwargs) -> None:
        super().update(**kwargs)
        self.rectangle.y = self.START_Y + sin(self.rectangle.x * 0.01 - self.rectangle.y * 0.001 + kwargs["clock_ticks"] * 0.005) * 15

    def deleting(self, scene):
        GameParticle(
            self.group.particles_manager,
            self.rectangle.center,
            "data/Assets/Free/particles/FruitCollected"
        )
