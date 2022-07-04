from data.scripts.map.collectable.collectable import Collectable
from data.scripts.map.collectable.fruit import Fruit
from data.scripts.utils import dynamic_animation_creation


class Gem(Fruit, Collectable):
    def __init__(self, group, pos, gem_type):
        Collectable.__init__(
            self,
            collideable_group=group,
            center_position=pos,
            animation_data=dynamic_animation_creation(
                images_path=f"data/Assets/Free/Items/Gem/{gem_type}",
                delay=6,
                images_scale=2
            ),
            value=10
        )
        self.START_Y = self.rectangle.y
