import pygame

from data.engine.animation.sprite_animation.animations_controller import AnimationsController
from data.engine.entity.collideable_entity import CollideableEntity
from data.scripts.particles.text_particle import TextParticle
from data.scripts.players.base_player import PLAYER_CHECKPOINT


class CheckPoint(CollideableEntity):
    """
    Checkpoint es una clase que se encarga de activar
    las banderas en caso de que el jugador pase por estas
    si es asi entonces se lanza un evento el cual acutaliza
    la posicion de respawn del Jugador
    """

    def __init__(self, group, position):
        self.animator = AnimationsController("data/Assets/animations/checkpoint.json")
        self.image = self.animator.get_image()
        self.collected = False
        rectangle = pygame.Rect(position[0], position[1], self.image.get_width(), self.image.get_height())
        super().__init__(group, rectangle, layer=1)

    def collision(self, other) -> None:
        if other.__class__.__base__.__name__ == "BasePlayer" and not self.collected:
            self.animator.start_animation("CREATING")
            self.collected = True

            pygame.event.post(
                pygame.event.Event(
                    PLAYER_CHECKPOINT,
                    {
                        "position":
                            (
                                self.rectangle.centerx,
                                self.rectangle.centery
                            )
                    }
                )
            )
            self.group.game_scene.director.sfx.play("Coin Total Win.wav")
            TextParticle("Checkpoint!", self.group.particles_manager, other.position)

    def update(self, **kwargs) -> None:
        self.animator.update(dt=kwargs["dt"], creating=False, collected=self.collected)
        self.image = self.animator.get_image()

    def draw(self, surface, offset=(0, 0)):
        surface.blit(
            self.image,
            (
                self.rectangle.x - offset[0],
                self.rectangle.y - offset[1]
            )
        )
