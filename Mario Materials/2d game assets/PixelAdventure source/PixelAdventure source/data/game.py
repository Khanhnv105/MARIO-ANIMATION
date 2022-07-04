
import pygame

from .engine.json.json_management import get_data, write
from .engine.management.director import Director
from .engine.sound.music import Music
from .engine.sound.sfx import SFX
from .scenes.end_scene import EndScene
from .scenes.level_passed_scene import LevelPassedScene
from .scenes.level_scene import LevelScene
from .scenes.menu_scene import Menu
from .scenes.pause_scene import PauseScene
from .scenes.tutorial_scene import TutorialScene


class Game(Director):
    def __init__(self):
        super().__init__(
            display_size=(int(64 * 18), int(64 * 10)),
            fps=144,
            show_performance=True,
            resizable=True,
            scaled=True
        )
        pygame.mouse.set_visible(False)

        self.sfx = SFX("data/Assets/SFX", 0)
        self.music = Music(0)
        self.add_scene(LevelScene, Menu, LevelPassedScene, PauseScene, TutorialScene, EndScene)
        self.start_scene("Menu")
        data = get_data("data/Assets/config/configurations.json")
        pygame.mixer.music.set_volume(data["Music"] / 100)
        self.sfx.set_volume(data["SFX"] / 100)

    def update(self, dt, mouse):
        super().update(dt, mouse)
        self.music.update(dt=dt, mouse=mouse)

    def on_terminate(self):
        super().on_terminate()

        data = get_data("data/Assets/config/configurations.json")
        data["Music"] = int(pygame.mixer.music.get_volume() * 100)
        data["SFX"] = int(self.sfx.volume * 100)
        write("data/Assets/config/configurations.json", data)