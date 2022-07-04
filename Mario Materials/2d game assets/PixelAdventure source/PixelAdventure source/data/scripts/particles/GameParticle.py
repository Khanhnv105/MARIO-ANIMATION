from data.engine.VFX.particle import Particle
from data.engine.animation.sprite_animation.single_animation_controller import SingleAnimationController
from data.engine.utils import draw_centered
from data.scripts.utils import dynamic_animation_creation


class GameParticle(Particle):

    def __init__(self, manager, position, images_path, size=2):
        super().__init__(manager, position=position, layer=3)
        self.animation = SingleAnimationController(
            dynamic_animation_creation(
                delay=4,
                cycle_mode="END",
                images_path=images_path,
                images_scale=size
            )
        )
        self.image = self.animation.get_image()

    def update(self, **kwargs):
        self.animation.update(kwargs["dt"])
        if not self.animation.is_running():
            self.destroy()

        self.image = self.animation.get_image()

    def draw(self, surface, offset=(0, 0)):
        draw_centered(
            surface,
            self.image,
            (
                self.position.x - offset[0],
                self.position.y - offset[1]
            )
        )
