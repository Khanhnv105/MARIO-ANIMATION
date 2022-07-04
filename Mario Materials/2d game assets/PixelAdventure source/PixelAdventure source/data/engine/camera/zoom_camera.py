import pygame

from data.engine.animation.math_animation.bezier_animation import BezierAnimation
from data.engine.camera.offset_camera import OffsetCamera

ZOOM_TARGET_ACHIEVED = pygame.USEREVENT + 1


class ZoomController:
    def __init__(self, initial_zoom=1):
        self.BASE_ZOOM = initial_zoom
        self.zoom = initial_zoom
        self.bounce_zoom_animation = BezierAnimation(
            (.49, .93), (.05, 1.04), end_point=(1, 0), start_on=False, mult_vel=2
        )
        self.max_zoom = 1
        self.get_back = False

        self.zoom_frames = None
        self.zoom_target = None
        self.zoom_delta = 0
        self.camera_focus = False
        self.get_back_after_zoom = True

    def restart(self):
        self.max_zoom = 1
        self.get_back = False

        self.zoom_frames = None
        self.zoom_target = None
        self.zoom_delta = 0
        self.camera_focus = False
        self.get_back_after_zoom = True
        self.zoom = self.BASE_ZOOM

    def bounce(self, max_zoom, time):
        self.bounce_zoom_animation.set_speed(time)
        self.max_zoom = max_zoom - self.BASE_ZOOM
        self.bounce_zoom_animation.restart_animation()

    def zoom_at(self, zoom_time, zoom_target, get_back_after_zoom=True):
        self.zoom_frames = zoom_time
        self.zoom_target = zoom_target
        self.camera_focus = True
        self.zoom_delta = zoom_target - self.zoom
        self.get_back_after_zoom = get_back_after_zoom

    def zoom_out_from(self, zoom):
        self.get_back = True
        self.zoom = zoom

    def update(self, dt):
        # Bounce animation
        if self.bounce_zoom_animation.running:
            self.bounce_zoom_animation.move(dt)
            self.zoom = self.BASE_ZOOM + self.bounce_zoom_animation.get_value() * self.max_zoom

        elif self.camera_focus:
            self.zoom += (self.zoom_delta / self.zoom_frames) * dt
            if self.zoom >= self.zoom_target:
                self.zoom = self.zoom_target
                self.camera_focus = False
                pygame.event.post(
                    pygame.event.Event(
                        ZOOM_TARGET_ACHIEVED, {}
                    )
                )
                if self.get_back_after_zoom:
                    self.get_back = True


        if self.get_back:
            if self.zoom > 1:
                self.zoom -= 0.01 * dt
            else:
                self.zoom = 1
                self.get_back = False


class ZoomCamera(OffsetCamera):
    def __init__(self, display_size):
        self.zoom_controller = ZoomController()

        super().__init__(display_size)

    def zoom_out_from(self, zoom):
        self.zoom_controller.zoom_out_from(zoom)

    def restart(self):
        super().restart()
        self.zoom_controller.restart()

    def update(self, **kwargs):
        super().update(**kwargs)
        self.zoom_controller.update(kwargs["dt"])

    def bounce(self, max_zoom, speed=1):
        self.zoom_controller.bounce(max_zoom, speed)

    def zoom_at(self, zoom_frames, zoom_target, get_back=True):
        """
        Este metodo hace zoom a un punto en un tiempo especifico
        y con un valor de zoom maximo al cual llega en ese tiempo
        """
        self.zoom_controller.zoom_at(zoom_frames, zoom_target, get_back)

    def set_zoom(self, zoom):
        if not self.zoom_controller.get_back:
            self.zoom_controller.zoom = zoom

    def get_zoom(self):
        return self.zoom_controller.zoom
