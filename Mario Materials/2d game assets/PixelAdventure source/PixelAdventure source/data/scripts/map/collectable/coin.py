from random import random

from data.scripts.map.collectable.collectable import Collectable
from data.scripts.particles.GameParticle import GameParticle
from data.scripts.particles.colored_particle import ColoredParticle
from data.scripts.utils import dynamic_animation_creation


class Coin(Collectable):
    def __init__(self, group, pos, coin_type="Gold"):
        super().__init__(
            collideable_group=group,
            center_position=pos,
            animation_data=dynamic_animation_creation(
                images_path=f"data/Assets/Free/Items/Coin/{coin_type}",
                delay=6,
                images_scale=2
            ),
            value=5
        )
        self.DELAY = 200
        self.last_time = 0

    def update(self, **kwargs) -> None:
        super().update(**kwargs)
        if self.last_time < kwargs["clock_ticks"]:
            self.last_time = kwargs["clock_ticks"] + self.DELAY
            ColoredParticle(
                self.group.particles_manager,
                self.rectangle.center,
                ((random() - 0.5) , 0),
                self.image.get_at(
                    (
                        self.image.get_width() // 2,
                        self.image.get_height() // 2
                    )
                ),
                frames=30,
                max_radius=5
            )

    def deleting(self, scene):
        GameParticle(
            self.group.particles_manager,
            self.rectangle.center,
            "data/Assets/Free/particles/FruitCollected"
        )


