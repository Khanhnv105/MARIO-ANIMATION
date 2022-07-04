from math import sin, cos, pi
from data.engine.math.vector import Vector


class Pendulum:
    def __init__(self, position, length, start_angle=pi / 2.5, adjust=0.4):
        self.length = length
        self.position = Vector(position)
        self.angular_velocity = 0
        self.angle = start_angle
        self.delta_adjust = adjust

    def update(self, **kwargs):
        angular_acceleration = -kwargs["gravity_acceleration"] * sin(self.angle) * kwargs["dt"] * 0.002 * self.delta_adjust
        self.angular_velocity += angular_acceleration * kwargs["dt"] * self.delta_adjust
        self.angle += self.angular_velocity * kwargs["dt"] * self.delta_adjust

    def _get_pendulum_position(self):
        return Vector(
            self.position.x + sin(self.angle) * self.length,
            self.position.y + cos(self.angle) * self.length
        )

    def draw(self, surface):
        pass
