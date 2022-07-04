from data.engine.animation.math_animation.bezier_animation import BezierAnimation




class ZoomController:
    MAX_ZOOM = 1000
    MIN_ZOOM = 50
    INITIAL_ZOOM = 100
    STEPS = 20

    AMOUNT_OF_STEPS = 10

    def __init__(self):
        self._zoom = self.INITIAL_ZOOM
        self._steps_left = 0
        self._zoom_factor = 0
        self._zooming = False
        self.animator = BezierAnimation((.17, .67), (.54, 1.41), start_on=False, mult_vel=0.4)
        self.animation_max_zoom = 0
        self.animation_base_zoom = 0

    def start_animation(self, base, max_zoom):
        self.animation_max_zoom = max_zoom - base
        self.animation_base_zoom = base
        self.animator.restart_animation()
        self._zooming = True

    def zooming(self) -> bool:
        return self._zooming

    def set_value(self, val: int):
        if not self._zooming:
            self._zoom = val

    def reset(self):
        self._zoom = self.INITIAL_ZOOM

    def _check_values(self):
        if self._zoom > self.MAX_ZOOM:
            self._zoom = self.MAX_ZOOM

        elif self._zoom < self.MIN_ZOOM:
            self._zoom = self.MIN_ZOOM

    def update(self, dtm):

        if not self.animator.running:
            # Si es que queda zoom por hacer
            if self._steps_left > 0:
                self._zoom += self._zoom_factor * dtm
                self._steps_left -= 1 * dtm
                self._check_values()
            else:
                # Si es que llegamos al ultimo paso por primera vez
                if self._zooming:
                    self._check_values()
                    self._zooming = False

                self._steps_left = 0
        else:
            self.animator.move(dtm)
            self._zoom = self.animation_base_zoom + self.animator.get_value() * self.animation_max_zoom
            self._zooming = self.animator.running

    def zoom_in(self):
        self._zooming = True
        zoom_left = 1.5 * (self._zoom + self._steps_left * abs(self._zoom_factor)) - self._zoom
        self._steps_left = self.AMOUNT_OF_STEPS
        self._zoom_factor = zoom_left / self.STEPS

    def zoom_out(self):
        self._zooming = True
        zoom_left = -1.4 * (self._zoom + self._steps_left * abs(self._zoom_factor)) + self._zoom
        self._steps_left = self.AMOUNT_OF_STEPS
        self._zoom_factor = zoom_left / self.STEPS

    def get_zoom(self, percentage=False):
        return self._zoom / 100 if not percentage else self._zoom
