import os

import pygame
from pygame.locals import *

from data.engine.json.json_management import get_data
from data.engine.management.transition import Transition
from data.engine.math.vector import Vector


class WindowState:
    def __init__(
            self,
            size,
            full_screen=False,
            scaled=False,
            resizable=False,
            caption="",
            icon_path=None
    ):
        if not full_screen:
            self.window = pygame.display.set_mode(size, pygame.RESIZABLE | pygame.SCALED)
        else:
            self.window = pygame.display.set_mode(size, pygame.FULLSCREEN)

        pygame.display.set_caption(caption)
        if icon_path:
            pygame.display.set_icon(pygame.image.load(icon_path))

    def set_fullscreen(self, size, state):
        if state:
            self.window = pygame.display.set_mode(size, pygame.RESIZABLE | pygame.SCALED | pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode(size, pygame.RESIZABLE | pygame.SCALED)


def calculate_milliseconds(frames):
    """
    Retorna la cantidad de milisegundos que deberia
    de tardar cada iteracion del loo para poder lograr
    la cantidad de frames deseada
    """
    return 1 / (frames / 1000)


class Director:
    TARGET_FRAMERATE = 60
    MINIMUM_FRAMES = 30

    def __init__(
            self,
            display_size: tuple,
            fps=60,
            show_performance=False,
            resizable=False,
            scaled=False,
            full_screen=False
    ):
        pygame.mixer.init()
        pygame.init()
        self.DISPLAY_SIZE = Vector(display_size[0], display_size[1])
        self.DISPLAY_CENTER = Vector(display_size[0] // 2, display_size[1] // 2)
        self.FPS = fps
        self.show_performance = show_performance
        self.window_controller = WindowState(
            size=display_size,
            full_screen=full_screen,
            resizable=resizable,
            scaled=scaled
        )

        self.running = False
        self.scenes = {}
        self.actual_scene = None
        self.actual_transition = None
        self.clock = pygame.time.Clock()

        self.delay_update = 0
        self.delay_draw = 0
        self.delay_events = 0
        self.show_delay = 1000
        self.step = 0

    def add_scene(self, *scene_class):
        """Se tiene que pasar la clase de la escena, sin construir"""
        for scene in scene_class:
            self.scenes[scene.__name__] = scene(self)

    def start_scene(self, scene_name):
        self.actual_scene = scene_name
        self.scenes[scene_name].on_load()

    def change_scene(self, scene_name: str):
        """
        Cambia de escena, llamando los metodos
        correspondientes de las escenas involucradas
        """
        self.scenes[self.actual_scene].on_quit()
        self.actual_scene = scene_name
        self.scenes[scene_name].on_load()

    def stop_transition(self):
        self.actual_transition = None

    def start_transition(self, transition_class, next_scene: str):
        """Inicia la transicion hacia la proxima escena"""
        self.actual_transition = transition_class(self, next_scene)
        self.actual_transition.on_load()

    def terminate(self):
        """Termina el programa"""
        self.running = False

    def get_window(self):
        return self.window_controller.window

    def fullscreen(self, state):
        self.window_controller.set_fullscreen(self.DISPLAY_SIZE, state)

    def loop(self):
        self.running = True
        while self.running:
            dt = self.events()
            mouse = pygame.mouse.get_pos()
            self.update(dt, mouse)
            self.draw(mouse)

        self.on_terminate()

    def events(self):
        time_events = pygame.time.get_ticks()

        delta_time = self.clock.tick() if self.FPS is None else self.clock.tick(self.FPS)
        if delta_time > calculate_milliseconds(self.MINIMUM_FRAMES):
            delta_time = 0

        dt = delta_time / 1000 * self.TARGET_FRAMERATE
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

            self.scenes[self.actual_scene].on_event(event)
        self.delay_events = pygame.time.get_ticks() - time_events

        return dt

    def update(self, dt, mouse):
        time_update = pygame.time.get_ticks()
        self.scenes[self.actual_scene].on_update(dt, mouse)
        if self.actual_transition:
            self.actual_transition.on_update(dt, mouse)
        self.delay_update = pygame.time.get_ticks() - time_update

    def draw(self, mouse):
        time_draw = pygame.time.get_ticks()
        self.scenes[self.actual_scene].on_draw(self.get_window(), mouse)
        if self.actual_transition:
            self.actual_transition.on_draw(self.get_window(), mouse)
        pygame.display.flip()
        self.delay_draw = pygame.time.get_ticks() - time_draw

        if self.show_performance and pygame.time.get_ticks() - self.step > self.show_delay:
            self.step = pygame.time.get_ticks() + self.show_delay
            data = "\n\nPerformance\n" \
                   f" - Events {self.delay_events}\n" \
                   f" - Update {self.delay_update}\n" \
                   f" - Draw {self.delay_draw}\n" \
                   f"Total delay: {self.delay_draw + self.delay_update + self.delay_events}\n" \
                   f"FPS: {self.clock.get_fps()}"
            print(data)

    def on_terminate(self):
        for scene in self.scenes.values():
            scene.on_terminate()

