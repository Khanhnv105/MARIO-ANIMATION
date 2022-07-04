import math
import os
from random import randint

from data.engine.UI.constants import CLICKED_EVENT
from data.engine.UI.container.KeyControllableFrame import KeyControllableFrame
from data.engine.UI.elements.key_controllable_button import KeyControllableButton
from data.engine.VFX.particles_manager import ParticlesManager
from data.engine.animation.math_animation.bezier_animation import BezierAnimation
from data.engine.image.draw import apply_filter
from data.engine.json.json_management import get_data, write
from data.engine.management.scene import Scene
from data.engine.UI.manager import UI_Manager
import pygame

from data.engine.math.vector import Vector
from data.scripts.particles.confetti import Confetti
from data.scripts.ui.double_label import DoublePixelartLabel
from data.transitions.transition import MainTransition


def get_root(size, actual_level_number):
    """
    The last level number parameter is used to check if there is any next level to play
    """

    LAST_LEVEL_NUMBER = len(os.listdir("data/Assets/maps")) - 1

    labels_x = size[0] // 1.65
    buttons_y = size[1] * 0.75
    labels_color = "White"
    frame = KeyControllableFrame(pygame.Rect(0, 0, size[0], size[1]))

    # BUTTONS
    next_level_button = KeyControllableButton(
        name="Next level",
        position=(labels_x + 200, buttons_y),
        image_path="data/Assets/Free/Menu/Buttons/Next.png",
        image_scale=4
    )

    re_play_level_button = KeyControllableButton(
        name="Re play",
        position=(labels_x + 100, buttons_y),
        image_path="data/Assets/Free/Menu/Buttons/Restart.png",
        image_scale=4
    )
    if LAST_LEVEL_NUMBER == actual_level_number:
        next_level_button.set_selectable(False)
        re_play_level_button.set_selected(True)
    else:
        next_level_button.set_selected(True)
        frame.put(next_level_button)

    previous_level_button = KeyControllableButton(
        name="Previous level",
        position=(labels_x, buttons_y),
        image_path="data/Assets/Free/Menu/Buttons/Previous.png",
        image_scale=4
    )

    quit_button = KeyControllableButton(
        name="Quit",
        position=(100, 100),
        image_path="data/Assets/Free/Menu/Buttons/Back.png",
        image_scale=4
    )

    # LABELS
    level_passed_label = DoublePixelartLabel(
        name="Passed level label",
        text="Passed level",
        scale=6,
        color1="White",
        color2="Black",
        pos=(size[0] // 3, 100),
        offset=3
    )

    time_label = DoublePixelartLabel(
        name="Time label",
        text="Time Taken: 17:30",
        scale=3,
        color1=labels_color,
        color2="Black",
        pos=(labels_x, 250),
        offset=3
    )
    attempts_label = DoublePixelartLabel(
        name="Attempts label",
        text="Attempts: 300",
        scale=3,
        color1=labels_color,
        color2="Black",
        pos=(labels_x, 300),
        offset=3
    )
    points_label = DoublePixelartLabel(
        name="Points label",
        text="Points: 300",
        scale=3,
        color1=labels_color,
        color2="Black",
        pos=(labels_x, 350),
        offset=3
    )

    frame.put(
        re_play_level_button,
        previous_level_button,
        level_passed_label,
        attempts_label,
        time_label,
        points_label,
        quit_button
    )

    return frame


PARTICLE_EVENT = pygame.USEREVENT + 10
MAX_LEVEL = 50


class LevelPassedScene(Scene):
    def __init__(self, director):
        super().__init__(director)
        self.background = pygame.Surface(self.director.DISPLAY_SIZE)
        self.ui_manager = None
        self.offset = Vector()
        self.bezier = BezierAnimation((0.2, 0.6), (0.6, 1.3))
        self.particles_manager = ParticlesManager(self)

    def on_event(self, event) -> None:

        if event.type == pygame.KEYDOWN:
            self.ui_manager.handle_key_pressed(event)

        elif event.type == PARTICLE_EVENT:
            Confetti(
                manager=self.particles_manager,
                position=(
                    randint(0, self.director.DISPLAY_SIZE[0]),
                    -10
                )
            )
        elif event.type == CLICKED_EVENT:
            if event.NAME == "Quit":
                self.director.start_transition(MainTransition, "Menu")
                self.director.sfx.play("Kick.wav")

            elif event.NAME == "Re play":
                self.director.start_transition(MainTransition, "LevelScene")
                self.director.sfx.play("Action Misc 12.wav")

            else:
                self.director.sfx.play("Action Misc 1.wav")

            if event.NAME == "Previous level":
                level = self._get_level("PREVIOUS")
                self.director.scenes["LevelScene"].future_load(level)
                self.director.start_transition(MainTransition, "LevelScene")

            elif event.NAME == "Next level":
                level = self._get_level("NEXT")
                self.director.scenes["LevelScene"].future_load(level)
                self.director.start_transition(MainTransition, "LevelScene")

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
        self.director.scenes["LevelScene"].on_draw(self.background, (0, 0))
        self.background = apply_filter(self.background, (0, 0, 0, 100))
        self.background.convert()
        self.offset.x = -self.director.DISPLAY_SIZE[0]
        self.bezier.restart_animation()
        pygame.time.set_timer(PARTICLE_EVENT, 30)

        time_taken = self.director.scenes["LevelScene"].clock.get_time()
        points = self.director.scenes["LevelScene"].level_manager.player_state.player_points
        deaths = self.director.scenes["LevelScene"].level_manager.player_state.deaths
        self.ui_manager = UI_Manager(
            get_root(self.director.DISPLAY_SIZE, self.director.scenes["LevelScene"].get_level_number()))
        self.ui_manager.root.elements_dict["Time label"].set_text(f"Time taken: {time_taken}")
        self.ui_manager.root.elements_dict["Points label"].set_text(f"Points: {points}")
        self.ui_manager.root.elements_dict["Attempts label"].set_text(f"Attempts: {deaths + 1}")

        self._save_data(
            time_taken=time_taken,
            deaths=deaths,
            points=points
        )

    def on_quit(self):
        pygame.time.set_timer(PARTICLE_EVENT, 0)

    def _save_data(self, **kwargs):

        """
        Metodo que se encarga de actualizar toda la informacion del
        nivel en caso de ser necesario y desbloquea el siguiente nivel
        """

        PATH = "data/Assets/config/levels.json"
        levels_data = get_data(PATH)
        level_name = self.director.scenes["LevelScene"].map_name

        # Guardo las estadisticas del nivel recien jugado
        previous_time = levels_data[level_name]["Time record"]
        if previous_time is None or kwargs["time_taken"] < previous_time:
            levels_data[level_name]["Time record"] = kwargs["time_taken"]

        levels_data[level_name]["Total deaths"] += kwargs["deaths"]
        previous_points = levels_data[level_name]["Best points"]
        if kwargs["points"] > previous_points:
            levels_data[level_name]["Best points"] = kwargs["points"]

        next_level = self._get_level("NEXT")

        if next_level in levels_data:
            levels_data[next_level]["Unlocked"] = True

        write(PATH, levels_data)

    def _get_level(self, direction):
        """
        Retorna el nombre del nivel dependiendo del parametro direction
        En el caso de que el nivel sea mayor que el maximo
        o menor que el minimo se retorna None
        """
        actual_level_name = self.director.scenes["LevelScene"].map_name

        add = 1 if direction == "NEXT" else -1

        next_number = int(actual_level_name[-2:]) + add
        if next_number <= MAX_LEVEL:

            if next_number < 10:
                return f"Level-0{next_number}"
            else:
                return f"Level-{next_number}"
