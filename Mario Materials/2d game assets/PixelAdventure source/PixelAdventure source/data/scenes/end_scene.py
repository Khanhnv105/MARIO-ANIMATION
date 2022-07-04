import math

import pygame

from data.engine.UI.elements.pixelart.pixelart_label import PixelartLabel
from data.engine.animation.sprite_animation.single_animation_controller import SingleAnimationController
from data.engine.management.scene import Scene
from data.scripts.utils import dynamic_animation_creation
from data.transitions.DoorTransition import DoorTransition


class EndScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.background = pygame.Surface(self.director.DISPLAY_SIZE)
        img = pygame.image.load("data/Assets/Free/Background/Big Scale/Purple.png")
        self.background.blit(img, (0, 0))
        self.characters_animations = [
            SingleAnimationController(
                dynamic_animation_creation("data/Assets/Free/Main Characters/Ninja Frog/Idle (32x32)")
            ),
            SingleAnimationController(
                dynamic_animation_creation("data/Assets/Free/Main Characters/Mask Dude/Idle (32x32)")
            ),
            SingleAnimationController(
                dynamic_animation_creation("data/Assets/Free/Main Characters/Pink Man/Idle (32x32)")
            ),
            SingleAnimationController(
                dynamic_animation_creation("data/Assets/Free/Main Characters/Virtual Guy/Idle (32x32)")
            )
        ]
        self.label = PixelartLabel("Label", "Thanks for playing!", 6, "White", (100, 200))
        self.label_black = PixelartLabel("Label", "Thanks for playing!", 6, "Black", (100, 200))

        self.developer_label = PixelartLabel("1", "Developed by Franco Yudica", 2, "Black", (director.DISPLAY_SIZE[0] - 500, 40))
        self.date_label = PixelartLabel("1", "From 27-02-2021 to 16-5-2021", 1, "Black", (director.DISPLAY_SIZE[0] - 500, 60))

    def on_event(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            self.director.start_transition(DoorTransition, "Menu")

    def on_update(self, dt: float, mouse: tuple) -> None:
        for animation in self.characters_animations:
            animation.update(dt=dt)


    def on_load(self):
        self.director.music.load_tracks(["data/Assets/music/menu.mp3"])
        self.director.music.play()

    def on_draw(self, surface: pygame.Surface, mouse: tuple) -> None:

        offset = (0, math.sin(pygame.time.get_ticks() / 500) * 40)

        surface.blit(self.background, (0, 0))
        for i, animation in enumerate(self.characters_animations):
            base = animation.get_image()
            image = pygame.transform.scale(base, (base.get_width() * 6, base.get_height() * 6))
            surface.blit(image, (30 + i * (image.get_width() + 30), surface.get_height() - image.get_height()))

        self.label_black.draw(surface, (offset[0], offset[1] * .7))
        self.label.draw(surface, offset)
        self.developer_label.draw(surface, (0, 0))
        self.date_label.draw(surface, (0, 0))