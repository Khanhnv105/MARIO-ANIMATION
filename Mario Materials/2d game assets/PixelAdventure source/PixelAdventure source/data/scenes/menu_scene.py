import os
from random import randint

import pygame

from data.engine.UI.constants import CLICKED_EVENT
from data.engine.UI.container.KeyControllableFrame import KeyControllableFrame
from data.engine.UI.elements.key_controllable_button import KeyControllableButton
from data.engine.UI.manager import UI_Manager
from data.engine.camera.offset_camera import OffsetCamera
from data.engine.json.json_management import get_data
from data.engine.management.scene import Scene
from data.engine.math.vector import Vector
from pygame.locals import *

from data.scripts.moving_background import MovingBackground
from data.scripts.ui.double_label import DoublePixelartLabel
from data.scripts.ui.level_button import LevelButton
from data.scripts.ui.text_button import TextButton
from data.scripts.ui.toggle_button import ToggleButton
from data.transitions.DoorTransition import DoorTransition
from data.transitions.transition import MainTransition


def load_UI(width, height):
    title_label = DoublePixelartLabel("Title label", "Pixel Adventure", 9, "White", "Black", (width // 2, 200),
                                      centered=True)
    play_button = KeyControllableButton(
        name="Play",
        position=(width // 2, height // 1.5),
        image_path="data/Assets/Free/Menu/Buttons/blue/play.png",
        image_scale=4,
        center=True
    )

    thanks_button = KeyControllableButton(
        name="Thanks",
        position=(10, 40),
        image_path="data/Assets/Free/Menu/Buttons/Achievements.png",
        image_scale=2,
        center=False
    )

    play_button.selected = True
    quit_button = KeyControllableButton(
        name="Quit",
        position=(50, height - 100),
        image_path="data/Assets/Free/Menu/Buttons/Close.png",
        image_scale=4
    )
    settings_button = KeyControllableButton(
        name="Settings",
        position=(width - 184, height - 188),
        image_path="data/Assets/Free/Menu/Buttons/Settings.png",
        image_scale=4
    )
    levels_button = KeyControllableButton(
        name="Levels",
        position=(width - 284, height - 188),
        image_path="data/Assets/Free/Menu/Buttons/Levels.png",
        image_scale=4
    )
    x = 700
    y = height * 1.6
    music_toggler_button = ToggleButton("Music toggle", "Music", (150, y), "Black")
    sfx_toggler_button = ToggleButton("SFX toggle", "SFX", (150, music_toggler_button.rect.bottom + 10), "Black")
    settings_label = DoublePixelartLabel("Settings label", "Settings", 6, "Black", "White", (width // 2, height * 1.4),
                                         centered=True)
    levels_font = DoublePixelartLabel("Levels label", "Levels", 6, "Black", "White", (width * 1.5, 100), centered=True)
    increase_music_volime = TextButton("Increase Music Volume", "+", (x, y), "Black")
    music_volume_button = TextButton("Music Volume button", "1000000000000000", (x + 40, y), "Black")
    music_volume_button.set_selectable(False)

    decrease_music_volume = TextButton("Decrease Music Volume", "-",
                                       (x + 40 + music_volume_button.font.get_width() + 24, y), "Black")

    sfx_volume_button = TextButton("SFX Volume button", "1000000000000000", (x + 40, y + 100), "Black")
    sfx_volume_button.set_selectable(False)

    increase_sfx_volime = TextButton("Increase SFX Volume", "+", (x, y + 100), "Black")
    decrease_sfx_volume = TextButton("Decrease SFX Volume", "-",
                                     (x + 40 + sfx_volume_button.font.get_width() + 24, y + 100), "Black")

    """Cargo todos los botones de los niveles en base 
    a sus estados guardados en el archivo levels.json
    """
    BUTTONS_PATH = "data/Assets/Free/Menu/Levels"
    x = 1200
    y = 200
    col = 0
    buttons = []

    levels_data = get_data("data/Assets/config/levels.json")

    for i, name in enumerate(os.listdir("data/Assets/Free/Menu/Levels/Unlocked")):

        if i == len(os.listdir("data/Assets/maps")) - 1:
            break

        locked_path = BUTTONS_PATH + f"/Locked/{name}"
        unlocked_path = BUTTONS_PATH + f"/Unlocked/{name}"
        name = "Level-" + name[:-4]

        btn = LevelButton(
            name=name,
            position=(x, y),
            path_unlocked=unlocked_path,
            path_locked=locked_path,
            image_scale=8,
            points=levels_data[name]["Best points"] if levels_data[name]["Completed"] else None,
            unlocked=levels_data[name]["Unlocked"]
        )
        buttons.append(btn)
        x += btn.width + 10
        col += 1

        if col > 4:
            col = 0
            y += btn.height + 10
            x = 1200

    back_levels = KeyControllableButton(
        name="Back levels",
        position=(1200, 10),
        image_path="data/Assets/Free/Menu/Buttons/Back.png",
        image_scale=4
    )
    back_settings = KeyControllableButton(
        name="Back settings",
        position=(10, height * 1.3),
        image_path="data/Assets/Free/Menu/Buttons/Back.png",
        image_scale=4
    )

    return [
               title_label,
               play_button,
               quit_button,
               settings_button,
               levels_button,
               levels_font,
               back_levels,
               back_settings,
               music_toggler_button,
               sfx_toggler_button,
               settings_label,
               increase_sfx_volime,
               decrease_sfx_volume,
               sfx_volume_button,
               music_volume_button,
               decrease_music_volume,
               increase_music_volime,
                thanks_button
           ] + buttons


MUSIC_EVENT = pygame.USEREVENT + 100


class Menu(Scene):
    def __init__(self, director):
        super().__init__(director)

        self.refresh_UI()

        path = "data/Assets/Free/Background/Big Scale"
        bgs = os.listdir(path)
        self.background = MovingBackground(path + f"/{bgs[randint(0, len(bgs) - 1)]}")
        self.offset = Vector()

        self.camera = OffsetCamera(self.director.DISPLAY_SIZE)
        self.camera_central_pos = self.director.DISPLAY_CENTER.copy()

        self.menu_velocity = Vector(0, 0)

    def refresh_UI(self):
        root = KeyControllableFrame((0, 0, self.director.DISPLAY_SIZE[0], self.director.DISPLAY_SIZE[1]))
        root.put(*load_UI(self.director.DISPLAY_SIZE[0], self.director.DISPLAY_SIZE[1]))
        self.ui_manager = UI_Manager(root)

        self.ui_manager.root.elements_dict["Music Volume button"].set_text(
            f"Music Volume {int(pygame.mixer.music.get_volume() * 100)}")
        self.ui_manager.root.elements_dict["SFX Volume button"].set_text(
            f"SFX Volume {int(self.director.sfx.volume * 100)}")

    def on_event(self, event) -> None:
        if event.type == KEYDOWN:
            self.ui_manager.handle_key_pressed(event)
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                self.director.sfx.play("Action Misc 4.wav")

        elif event.type == CLICKED_EVENT:

            if event.NAME == "Play":
                self._play_level(self._get_last_level())
                self.director.music.fade(500)
                self.director.sfx.play("Action Misc 12.wav")

            elif event.NAME == "Thanks":
                self.director.start_transition(DoorTransition, "EndScene")


            elif event.NAME == "Quit":
                self.director.terminate()
            else:
                self.director.sfx.play("Action Misc 1.wav")

            if event.NAME == "Levels":
                self.camera_central_pos.x = self.director.DISPLAY_SIZE[0] + self.director.DISPLAY_CENTER[0]
                self.ui_manager.root.select("Level-01")

            elif event.NAME == "Settings":
                self.camera_central_pos.y = self.director.DISPLAY_SIZE[1] + self.director.DISPLAY_CENTER[1]
                self.ui_manager.root.select("Back settings")

            elif event.NAME == "Back settings":
                self.camera_central_pos.y = self.director.DISPLAY_CENTER[1]
                self.ui_manager.root.select("Settings")

            elif event.NAME == "Back levels":
                self.camera_central_pos.x = self.director.DISPLAY_SIZE[0] / 2
                self.ui_manager.root.select("Settings")

            elif event.TYPE == "LevelButton":
                self._play_level(event.NAME)

            elif event.NAME == "Increase Music Volume":
                volume = pygame.mixer.music.get_volume() + 0.05
                if volume > 1:
                    volume = 1
                self.ui_manager.root.elements_dict["Music Volume button"].set_text(f"Music Volume {int(volume * 100)}")
                pygame.mixer.music.set_volume(volume)

            elif event.NAME == "Decrease Music Volume":
                volume = pygame.mixer.music.get_volume() - 0.05

                if volume < 0:
                    volume = 0
                self.ui_manager.root.elements_dict["Music Volume button"].set_text(f"Music Volume {int(volume * 100)}")
                pygame.mixer.music.set_volume(volume)

            elif event.NAME == "Increase SFX Volume":
                volume = self.director.sfx.volume + 0.05
                if volume > 1:
                    volume = 1
                self.ui_manager.root.elements_dict["SFX Volume button"].set_text(f"SFX Volume {int(volume * 100)}")
                self.director.sfx.set_volume(volume)

            elif event.NAME == "Decrease SFX Volume":
                volume = self.director.sfx.volume - 0.05

                if volume < 0:
                    volume = 0
                self.ui_manager.root.elements_dict["SFX Volume button"].set_text(f"SFX Volume {int(volume * 100)}")
                self.director.sfx.set_volume(volume)

            elif event.NAME == "SFX toggle":
                self.director.sfx.turn_on() if event.ELEMENT.get_state() else self.director.sfx.turn_off()

            elif event.NAME == "Music toggle":
                self.director.music.unpause() if event.ELEMENT.get_state() else self.director.music.pause()

        elif event.type == MUSIC_EVENT:
            self.offset.y += 4

    def on_update(self, dt: float, mouse: tuple) -> None:
        self.offset.y += self.menu_velocity.y - self.offset.y * 0.01
        ticks = pygame.time.get_ticks()
        self.ui_manager.update(
            dt=dt,
            mouse=mouse,
            clock_ticks=ticks
        )

        add = self.ui_manager.root.selected_element.rect.center
        target = self.camera_central_pos + Vector(0, add[1] - self.director.DISPLAY_CENTER[1]) / 5
        self.camera.update(
            dt=dt,
            clock_ticks=ticks,
            mouse=mouse,
            target_position=target
        )
        self.background.update(dt)

    def on_draw(self, surface: pygame.Surface, mouse: tuple) -> None:
        camera_offset = self.camera.offset
        final_offset = camera_offset + self.offset

        surface.fill((0, 0, 0))
        self.background.draw(surface)
        self.ui_manager.draw(surface, final_offset)

    def on_load(self):
        self.refresh_UI()
        pygame.time.set_timer(MUSIC_EVENT, 800)
        self.director.music.load_tracks(["data/Assets/music/menu.mp3"])
        self.director.music.play()

    def on_quit(self):
        pygame.time.set_timer(MUSIC_EVENT, 0)
        self.director.music.fade()

    def on_terminate(self):
        pass

    def _play_level(self, level_name):

        if level_name == "tutorial":
            self._play_tutorial()
            return

        """Cambia la escena y abre el nivel con el nombre pasado por parametro"""
        self.director.scenes["LevelScene"].future_load(level_name)
        self.director.start_transition(DoorTransition, "LevelScene")

    def _get_last_level(self):
        """
        Lee el archivo levels.json buscando cual es el
        ultimo nivel desbloqueado y lo retorna, este metodo
        se usa cuando se presiona el boton Play, dado a que
        el mismo envia al jugador al ultimo nivel desbloqueado
        """
        levels_data = get_data("data/Assets/config/levels.json")
        last_level = None
        for level in levels_data:
            if not levels_data[level]["Unlocked"]:
                break
            last_level = level

        if last_level is None:
            return "tutorial"

        return last_level

    def _play_tutorial(self):
        self.director.start_transition(DoorTransition, "TutorialScene")
