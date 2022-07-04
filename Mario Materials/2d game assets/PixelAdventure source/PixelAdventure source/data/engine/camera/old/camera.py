from random import randint

import pygame

from .scroller import Scroll
from .zoom_controller import ZoomController
from data.engine.math.vector import Vector


class Camera:
    def __init__(self, ratio, display_size):
        self._scroller = Scroll(display_size=display_size, ratio=ratio)
        self._zoom_controller = ZoomController()
        self.previus_scroll = 0, 0
        self.previus_zoom = 1

        self.shaking = 0
        self.shake_magnitude = Vector()
        self.velocity = Vector()

    def shake(self, duration, shake_magnitude_x, shake_magnitude_y):
        self.shake_magnitude = Vector(shake_magnitude_x, shake_magnitude_y)
        self.shaking = pygame.time.get_ticks() + duration

    def offset_camera(self, x=0, y=0):
        self._scroller.x += x
        self._scroller.y += y

    def zoom_animation(self, base=ZoomController.MIN_ZOOM, max_zoom=100):
        self._zoom_controller.start_animation(base, max_zoom)

    def scroll_by(self, x=0, y=0):
        self._scroller.x += x
        self._scroller.y += y

    def zoom_changed(self):
        return self.previus_zoom != self.get_zoom()

    def scroll_changed(self):
        return self.previus_scroll != self._scroller.get_scroll(self.get_zoom())

    def moved(self) -> bool:

        """
        Retorna si es que la camara se ha movido o lo esta haciendo
        """

        return (
                self.scroll_changed()
                or self.zoom_changed()
                or self.is_zooming()
        )

    def get_zoom_bounds(self):

        """
        Retorna el zoom maximo y el minimo
        """
        return self._zoom_controller.MIN_ZOOM, self._zoom_controller.MAX_ZOOM

    def update_to_new_ratio(self, ratio: float):
        self._scroller.update_to_new_ratio(ratio)

    def push(self, vector):
        self.velocity = vector

    def reset(self):
        self._zoom_controller.reset()
        self._scroller.reset_position()

    def update(self, **kwargs):
        following_pos = kwargs["following_position"] if "following_position" in kwargs else None
        self._scroller.update(following_pos, kwargs["dt"])
        self._zoom_controller.update(kwargs["dt"])

        self._scroller.x += self.velocity.x
        self._scroller.y += self.velocity.y

        self.velocity = self.velocity.normalized() * (self.velocity.get_length() * (1 - kwargs["dt"] * 0.3))

        if self.shaking - kwargs["clock_ticks"] > 0:
            self._scroller.x += randint(-self.shake_magnitude.x, self.shake_magnitude.x)
            self._scroller.y += randint(-self.shake_magnitude.y, self.shake_magnitude.y)

    def is_scrolling(self):
        return self._scroller.activated

    def is_zooming(self) -> bool:
        return self._zoom_controller.zooming()

    def get_scroll(self, update_scroll=False):
        scroll = self._scroller.get_scroll(self.get_zoom())

        if update_scroll:
            self.previus_scroll = scroll

        return Vector(scroll[0], scroll[1])

    def start_scroll(self):
        self._scroller.start()

    def stop_scroll(self):
        self._scroller.stop(self.get_zoom())

    def get_zoom(self, update_zoom=False, percentage=False):

        zoom = self._zoom_controller.get_zoom(percentage)
        if update_zoom:
            self.previus_zoom = zoom
        return zoom

    def set_zoom(self, val: int):
        self._zoom_controller.set_value(val)

    def zoom(self, direction='in'):
        if direction == "in":
            self._zoom_controller.zoom_in()
        else:
            self._zoom_controller.zoom_out()
