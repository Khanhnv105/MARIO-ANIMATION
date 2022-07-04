
import pygame

from data.engine.UI.elements.key_controllable_button import get_rgb
from data.engine.animation.sprite_animation.single_animation_controller import SingleAnimationController
from data.engine.entity.image_collideable_entity import ImageCollideableEntity
from data.engine.math.vector import Vector
from data.scripts.particles.confetti import Confetti
from data.scripts.players.base_player import PLAYER_WIN
from data.scripts.utils import dynamic_animation_creation


class End(ImageCollideableEntity):
    def __init__(self, group, position):
        self.animator = SingleAnimationController(
            dynamic_animation_creation(
                images_path="data/Assets/Free/Items/Checkpoints/End/End (Pressed) (64x64)",
                images_scale=2
            )
        )
        self.image = self.animator.get_image()

        super().__init__(group, position, self.image, layer=1, mode="dynamic")
        self.collected = False

    def collision(self, other) -> None:
        if other.__class__.__base__.__name__ == "BasePlayer" and not self.collected and not other.dead:
            event = pygame.event.Event(
                PLAYER_WIN,
                {
                    "position": Vector(
                        self.rectangle.centerx,
                        self.rectangle.centery
                    )
                }
            )
            pygame.event.post(event)
            self.collected = True
            for _ in range(100):
                Confetti(self.group.particles_manager, self.rectangle.center)

    def update(self, **kwargs) -> None:
        self.animator.update(dt=kwargs["dt"])
        self.apply_filter(self.animator.get_image(), kwargs["clock_ticks"] / 500)

    def apply_filter(self, base, amount):
        """Applies a filter color to the surface obtained from the image mask"""
        self.image = base.copy()
        self.image.blit(
            pygame.mask.from_surface(self.image).to_surface(
                setcolor=get_rgb(amount, alpha=150),
                unsetcolor=(0, 0, 0, 0)
            ),
            (0, 0)
        )

    def draw(self, surface, offset=(0, 0)):
        surface.blit(
            self.image,
            (
                self.rectangle.x - offset[0],
                self.rectangle.y - offset[1]
            )
        )


