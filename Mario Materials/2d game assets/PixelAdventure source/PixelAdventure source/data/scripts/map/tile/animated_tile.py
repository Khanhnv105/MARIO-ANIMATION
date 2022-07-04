from data.engine.animation.sprite_animation.single_animation_controller import SingleAnimationController
from data.scripts.map.tile.static_tile import Tile, StaticTile
from data.scripts.utils import dynamic_animation_creation


class AnimatedTile(StaticTile):
    def     __init__(self, group, top_left, animated_type):
        if animated_type == "Floating":
            path = "data/Assets/Free/Traps/Falling Platforms/On (32x10)"
        self.animator = SingleAnimationController(
            dynamic_animation_creation(
                delay=5,
                images_path=path,
                images_scale=2
            )
        )

        super().__init__(group, top_left, self.animator.get_image())

    def update(self, **kwargs) -> None:
        super().update(**kwargs)
        self.animator.update(kwargs["dt"])
        self.image = self.animator.get_image()
