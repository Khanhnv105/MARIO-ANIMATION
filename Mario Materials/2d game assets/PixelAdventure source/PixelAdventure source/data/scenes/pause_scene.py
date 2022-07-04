import math
from data.engine.UI.constants import CLICKED_EVENT
from data.engine.UI.container.KeyControllableFrame import KeyControllableFrame
from data.engine.UI.elements.key_controllable_button import KeyControllableButton
from data.engine.VFX.particles_manager import ParticlesManager
from data.engine.animation.math_animation.bezier_animation import BezierAnimation
from data.engine.image.draw import apply_filter
from data.engine.management.scene import Scene
from data.engine.UI.manager import UI_Manager
import pygame
from data.engine.math.vector import Vector
from data.scripts.ui.double_label import DoublePixelartLabel
from data.scripts.ui.text_button import TextButton
from data.transitions.transition import MainTransition


def get_root(size):
    frame = KeyControllableFrame(pygame.Rect(0, 0, size[0], size[1]))
    resume_button = KeyControllableButton(
        name="Resume",
        position=(size[0] // 2, size[1] // 2),
        image_path="data/Assets/Free/Menu/Buttons/Play.png",
        image_scale=4
    )

    resume_button.set_selected(True)
    re_play_level_button = KeyControllableButton(
        name="Re play",
        position=(size[0] // 2 + 100, size[1] // 2),
        image_path="data/Assets/Free/Menu/Buttons/Restart.png",
        image_scale=4
    )

    quit_button = KeyControllableButton(
        name="Quit",
        position=(100, 100),
        image_path="data/Assets/Free/Menu/Buttons/Back.png",
        image_scale=4
    )

    # LABELS
    level_paused_label = DoublePixelartLabel(
        name="Pause label",
        text="Level paused",
        scale=6,
        color1="White",
        color2="Black",
        pos=(size[0] // 3, 100),
        offset=3
    )

    x = 100
    y = size[1] * 0.65

    increase_music_volume = TextButton("Increase Music Volume", "+", (x, y), "Black")
    music_volume_button = TextButton("Music Volume button", "Music volume: 100", (x + 40, y), "Black")
    music_volume_button.set_selectable(False)

    decrease_music_volume = TextButton("Decrease Music Volume", "-",
                                       (x + 40 + music_volume_button.font.get_width() + 24, y), "Black")

    sfx_volume_button = TextButton("SFX Volume button", "Music volume: 100", (x + 40, y + 100), "Black")
    sfx_volume_button.set_selectable(False)

    increase_sfx_volime = TextButton("Increase SFX Volume", "+", (x, y + 100), "Black")
    decrease_sfx_volume = TextButton("Decrease SFX Volume", "-",
                                     (x + 40 + sfx_volume_button.font.get_width() + 24, y + 100), "Black")

    frame.put(
        resume_button,
        re_play_level_button,
        level_paused_label,
        quit_button,
        increase_music_volume,
        music_volume_button,
        decrease_music_volume,
        sfx_volume_button,
        increase_sfx_volime,
        decrease_sfx_volume

    )
    return frame


PARTICLE_EVENT = pygame.USEREVENT + 10


class PauseScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.background = pygame.Surface(self.director.DISPLAY_SIZE)
        self.ui_manager = UI_Manager(get_root(self.director.DISPLAY_SIZE))
        self.offset = Vector()
        self.bezier = BezierAnimation((0.2, 0.6), (0.6, 1.3))
        self.particles_manager = ParticlesManager(self)

    def on_event(self, event) -> None:

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                self.director.change_scene("LevelScene")
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                self.director.sfx.play("Action Misc 4.wav")

            self.ui_manager.handle_key_pressed(event)

        elif event.type == CLICKED_EVENT:
            if event.NAME == "Quit":
                self.director.start_transition(MainTransition, "Menu")
                self.director.sfx.play("Kick.wav")

            elif event.NAME == "Resume":
                self.director.change_scene("LevelScene")
                self.director.sfx.play("Action Misc 12.wav")

            else:
                self.director.sfx.play("Action Misc 1.wav")

            if event.NAME == "Re play":
                self.director.scenes["LevelScene"].restart()
                self.director.start_transition(MainTransition, "LevelScene")
                self.director.sfx.play("Action Misc 12.wav")

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

    def on_update(self, dt: float, mouse: tuple) -> None:
        ticks = pygame.time.get_ticks()
        self.ui_manager.update(
            dt=dt,
            mouse_pos=mouse,
            clock_ticks=ticks
        )
        self.particles_manager.update(
            dt=dt,
            mouse_pos=mouse,
            clock_ticks=ticks
        )
        if self.bezier.running:
            self.bezier.move(dt)
            value = self.bezier.get_value()
            self.offset.x = (1 - value) * -self.director.DISPLAY_SIZE[0]
        self.offset.y = math.sin(ticks / 800) * 10

    def on_draw(self, surface: pygame.Surface, mouse: tuple) -> None:
        surface.blit(
            self.background,
            (0, 0)
        )
        self.ui_manager.draw(surface, self.offset)
        self.particles_manager.draw(surface, (0, 0))

    def on_load(self):
        self.ui_manager.root.elements_dict["Music Volume button"].set_text(
            f"Music Volume {int(pygame.mixer.music.get_volume() * 100)}")
        self.ui_manager.root.elements_dict["SFX Volume button"].set_text(
            f"SFX Volume {int(self.director.sfx.volume * 100)}")
        self.director.scenes["LevelScene"].on_draw(self.background, (0, 0))
        self.background = apply_filter(self.background, (0, 0, 0, 100))
        self.background.convert()
        self.offset.x = -self.director.DISPLAY_SIZE[0]
        self.bezier.restart_animation()
