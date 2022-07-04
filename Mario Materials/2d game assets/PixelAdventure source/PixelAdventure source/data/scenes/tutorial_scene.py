import math
from random import randint

import pygame

from data.engine.UI.elements.pixelart.pixelart_label import PixelartLabel
from data.engine.camera.offset_camera import OffsetCamera
from data.engine.color.HSV import ColorHSV
from data.engine.entity.collideable_entities_group import CollideableEntitiesGroup
from data.engine.json.json_management import write, get_data
from data.engine.management.scene import Scene
from data.engine.math.vector import Vector
from data.engine.tile.tile_set_loader import load_tile
from data.scripts.collideable_group_particles import CollideableGroupWithParticles
from data.scripts.map.tile.static_tile import StaticTile
from data.scripts.players.NinjaFrog import NinjaFrog
from data.transitions.transition import MainTransition

EVENT = pygame.USEREVENT + 1


class TutorialScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.images = [
        ]
        self.tutorial_image = load_tile(
            "data/Assets/Free/Menu/turorial/NinjaFrog.png", 4, None
        )
        self.title = PixelartLabel("Title", "How to play", 7, "White", (100, 40))
        self.press_any = PixelartLabel("Prees", "Press enter to continue.  ", 2, "White", (100, 600))
        self.press_any_dots = 1
        self.color = (0, 0, 0)
        self.offset = Vector()
        self.group = CollideableGroupWithParticles(self, (10, 10))
        self.player = NinjaFrog(self.group, "Ninja Frog", (0, 0))
        self.offset_sin = 0

        def get_image(w, h):
            surface = pygame.Surface((w, h))
            surface.fill((33, 31, 48))
            return surface

        Y = 550
        StaticTile(self.group, (-self.director.DISPLAY_SIZE[0], Y), get_image(self.director.DISPLAY_SIZE[0] * 2, 300))
        StaticTile(self.group, (-self.director.DISPLAY_SIZE[0] - 1000, -200), get_image(1000, 1000))
        StaticTile(self.group, (self.director.DISPLAY_SIZE[0], -200), get_image(1000, 1000))

        x = -self.director.DISPLAY_SIZE[0]

        while x < self.director.DISPLAY_SIZE[0]:
            h = randint(10, 60)
            w = randint(50, 100)
            StaticTile(self.group, (x, Y - h), get_image(w, h))
            gap = randint(50, 100)
            x += w + gap

        self.camera = OffsetCamera(self.director.DISPLAY_SIZE)

    def on_event(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            self.group.key_down(event)

            if event.key == pygame.K_RETURN:
                PATH = "data/Assets/config/levels.json"
                levels_data = get_data(PATH)
                levels_data["Level-01"]["Unlocked"] = True
                write(PATH, levels_data)
                self.director.scenes["LevelScene"].future_load("Level-01")
                self.director.start_transition(MainTransition, "LevelScene")

        elif event.type == pygame.KEYUP:
            self.group.key_up(event)

        if event.type == EVENT:
            self.press_any_dots += 1

            if self.press_any_dots > 3:
                self.press_any_dots = 1

            self.press_any.set_text("Press enter to continue" + "." * self.press_any_dots)

    def on_update(self, dt: float, mouse: tuple) -> None:
        ticks = pygame.time.get_ticks()
        step = ticks / 700

        sin = lambda step, add: (math.sin(step + add) + 1) / 2

        self.color = (
            int(sin(step, 0) * 255),
            int(sin(step, 2) * 255),
            int(sin(step, 4) * 255)
        )
        self.offset_sin = math.sin(step) * 30
        self.camera.update(
            dt=dt,
            clock_ticks=ticks,
            mouse_pos=mouse,
            target_position=Vector(self.player.position.x, self.director.DISPLAY_CENTER[1])
        )
        self.group.update(
            dt=dt,
            mouse_pos=mouse,
            clock_ticks=ticks,
            player_dt=dt,
            display_rect=pygame.Rect(0, 0, self.director.DISPLAY_SIZE[0], self.director.DISPLAY_SIZE[1])
        )

    def on_load(self):
        pygame.time.set_timer(EVENT, 1000)

    def on_quit(self):
        pygame.time.set_timer(EVENT, 0)

    def on_draw(self, surface: pygame.Surface, mouse: tuple) -> None:

        self.offset = Vector(self.camera.offset.x, self.camera.offset.y + self.offset_sin)

        surface.fill(self.color)

        surface.blit(
            self.tutorial_image,
            (
                100 - self.offset.x * 0.6,
                200 - self.offset.y * 1.2
            )
        )

        self.group.draw(surface, self.offset)

        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (
                0,
                30 - self.offset.y,
                self.director.DISPLAY_SIZE[0],
                100
            )
        )
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (
                0,
                30 - self.offset.y * 0.8 + 110,
                self.director.DISPLAY_SIZE[0],
                10
            )
        )

        self.title.draw(surface, (0, -self.offset.y))
        self.press_any.draw(surface, (0, self.offset.y * 0.4))
