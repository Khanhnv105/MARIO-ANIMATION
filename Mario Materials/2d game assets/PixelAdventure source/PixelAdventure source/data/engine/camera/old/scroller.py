import pygame


class Scroll:
    FOLLOW_DIVISOR = 20

    def __init__(self, display_size, ratio):
        self.DISPLAY_SIZE = display_size
        self.WIDTH, self.HEIGHT = int(display_size[0] * ratio), int(display_size[1] * ratio)
        self.activated = False
        self.previus_position = [0, 0]  # Posicion el la cual se hizo click
        self.x, self.y = 0, 0
        self.locked = False
        self.central_point = self.WIDTH // 2, self.HEIGHT // 2
        self.last_frame_position = self.x, self.y
        self.old_position = 0, 0

    def reset_position(self):
        self.x, self.y = -self.WIDTH // 2, -self.HEIGHT // 2

    def update_to_new_ratio(self, ratio: float, display_size):

        """
        Actualiza el valor de la posicion central respecto a la pantalla
        """

        self.WIDTH, self.HEIGHT = int(display_size[0] * ratio), int(display_size[1] * ratio)
        self.central_point = self.WIDTH // 2, self.HEIGHT // 2

    # Verifica si es que esta bloqueado o no y si es asi entonces sigue al objeto
    def update(self, pos, dt_mult):
        self._move_towards(pos, dt_mult)

    def _move_towards(self, locked_object_pos, dt_mult):
        if locked_object_pos:
            self.x += (locked_object_pos[0] - self.x - self.WIDTH / 2 + self.central_point[
                0]) / self.FOLLOW_DIVISOR * dt_mult
            self.y += (locked_object_pos[1] - self.y - self.HEIGHT / 2 + self.central_point[
                1]) / self.FOLLOW_DIVISOR * dt_mult

    # Activa el SCROLL
    def start(self):
        self.activated = True
        # Posición donde hacemos click
        self.previus_position = pygame.mouse.get_pos()

    def stop(self, zoom):
        self.activated = False
        m = pygame.mouse.get_pos()
        self.x += (self.previus_position[0] - m[0]) / zoom
        self.y += (self.previus_position[1] - m[1]) / zoom

        self.previus_position = m

    def get_scroll(self, zoom):

        if self.activated:
            mouse = pygame.mouse.get_pos()

            x = (self.previus_position[0] - mouse[0]) / zoom + self.x
            y = (self.previus_position[1] - mouse[1]) / zoom + self.y

            return int(x * zoom) - self.central_point[0], int(y * zoom) - self.central_point[1]

        else:
            return int(self.x * zoom) - self.central_point[0], int(self.y * zoom) - self.central_point[1]
