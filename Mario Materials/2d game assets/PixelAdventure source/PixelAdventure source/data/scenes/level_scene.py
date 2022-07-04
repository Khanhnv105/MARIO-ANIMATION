import math
from random import randint

import pygame

from data.engine.UI.container.KeyControllableFrame import KeyControllableFrame
from data.engine.UI.elements.pixelart.pixelart_font import PixelartFont
from data.engine.UI.elements.pixelart.pixelart_label import PixelartLabel
from data.engine.UI.manager import UI_Manager
from data.engine.camera.zoom_camera import ZoomCamera, ZOOM_TARGET_ACHIEVED
from data.engine.management.scene import Scene
from data.engine.math.vector import Vector
from data.scripts.clock import Clock
from data.scripts.level_manager import LevelManager
from data.scripts.particles.text_particle import TextParticle
from data.scripts.players.base_player import PLAYER_COLLECTABLE, PLAYER_DEAD, PLAYER_CHECKPOINT, PLAYER_WIN
from data.transitions.DoorTransition import DoorTransition


def get_root(display_size):
    frame = KeyControllableFrame(pygame.Rect(0, 0, display_size[0], display_size[1]))
    font = PixelartFont("10:11", 2, "data/Assets/Free/Menu/Text/Text (White) (8x10).png", 8, 10)
    time_label = PixelartLabel(
        "Time label",
        "00:00",
        1,
        "White",
        (
            display_size[0] // 2 - font.get_width() // 2,
            font.get_height()
        )
    )
    frame.put(time_label)

    return frame


class LevelScene(Scene):
    def __init__(self, director):
        super().__init__(director)

        self.scale = 2
        self.zoom = 2
        self.offset = 0, 0

        self.camera = ZoomCamera(self.director.DISPLAY_SIZE)
        self.level_manager = None
        self.map_name = None

        self.ui_manager = UI_Manager(get_root(self.director.DISPLAY_SIZE))
        self.ui_offset = Vector()
        self.clock = Clock()
        self.running_level = False

    def on_event(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                self.director.change_scene("PauseScene")

            self.level_manager.key_down(event)

        elif event.type == pygame.KEYUP:
            self.level_manager.key_up(event)

        elif event.type == ZOOM_TARGET_ACHIEVED:
            if self.level_manager.player_state.win:
                self.running_level = False
                if self.get_level_number() != 10:
                    self.director.change_scene("LevelPassedScene")
                else:
                    self.director.start_transition(DoorTransition, "EndScene")

        elif event.type == PLAYER_COLLECTABLE:
            TextParticle(
                f"+{event.points}",
                self.level_manager.group.particles_manager,
                event.position,
                color=event.color
            )
            self.director.sfx.play(f"Coin {randint(1, 6)}.wav")
            self.level_manager.player_state.collected(event.points)

        elif event.type == PLAYER_DEAD:
            self.director.sfx.play(f"Hit {randint(1, 5)}.wav")
            self.level_manager.player_dead_event(event)

        elif event.type == PLAYER_CHECKPOINT:
            self.level_manager.player_state.change_respawn(event.position)

        elif event.type == PLAYER_WIN:
            self.camera.zoom_at(60, 2.5, get_back=False)
            self.director.sfx.play("Beam Up.wav")
            self.level_manager.player_state.won()

    def on_update(self, dt: float, mouse: tuple) -> None:

        ticks = pygame.time.get_ticks()
        self.camera.update(
            target_position=self._get_offset(),
            dt=dt,
            clock_ticks=ticks
        )

        self.ui_manager.update(
            dt=dt,
            mouse_pos=mouse,
            clock_ticks=ticks
        )

        if self.running_level:
            self.level_manager.update(dt=dt, clock_ticks=ticks, mouse_pos=Vector(mouse[0], mouse[1]))

        self.clock.update(clock_ticks=ticks)
        self.ui_manager.root.elements_dict["Time label"].set_text(self.clock.get_time())
        self.ui_offset.y = math.sin(ticks / 500) * 10

    def on_draw(self, surface: pygame.Surface, mouse: tuple) -> None:
        self.offset = self.camera.offset
        self.zoom = self.camera.get_zoom()
        self.level_manager.draw(surface, self.offset, self.zoom)
        self.ui_manager.draw(surface, self.ui_offset)

    def on_load(self):
        if not self.running_level:
            self.restart()

        else:
            self.clock.resume()

    def on_quit(self):
        self.director.music.fade(500)

    def _get_offset(self):
        w = 36 * 16 * self.scale
        h = 20 * 16 * self.scale
        dungeon = (
            int(self.level_manager.player.position.x / w) * 2 + 1,
            int(self.level_manager.player.position.y / h) * 2 + 1
        )
        return (
            self.director.DISPLAY_CENTER[0] * dungeon[0] + 32,
            self.director.DISPLAY_CENTER[1] * dungeon[1] + 32
        )

    def restart(self):
        self.clock.restart()
        self.camera.restart()
        self.camera.set_camera_offset(self.director.DISPLAY_CENTER.x, self.director.DISPLAY_CENTER.y)
        self.level_manager = LevelManager(self, self.map_name)
        self.director.music.load_tracks([f"data/Assets/music/songs/{divmod(self.get_level_number(), 7)[1]}.mp3"])
        self.director.music.play()
        self.running_level = True
        self.camera.zoom_out_from(2.5)

    def future_load(self, map):
        self.map_name = map
        self.running_level = False

    def get_level_number(self) -> int:
        return int(self.level_manager.LEVEL_NUMBER)
