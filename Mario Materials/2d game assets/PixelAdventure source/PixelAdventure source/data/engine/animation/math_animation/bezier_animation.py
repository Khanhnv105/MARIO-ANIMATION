class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y


# Retorna la posicion en base al tiempo [Bezier Cubic Curve]
def calculate_cubic(p0, p1, p2, p3, t):
    x = (p0.x * (1 - t) ** 3) + (3 * p1.x * t * (1 - t) ** 2) + (3 * p2.x * t ** 2 * (1 - t) + p3.x * t ** 3)
    y = (p0.y * (1 - t) ** 3) + (3 * p1.y * t * (1 - t) ** 2) + (3 * p2.y * t ** 2 * (1 - t) + p3.y * t ** 3)
    return x, y


# Retorna la posicion en base al tiempo [Bezier Cuadratic Curve]
def calculate_cuadratic(p0, p1, p2, t):
    x = (1 - t) ** 2 * p0.x + 2 * t * (1 - t) * p1.x + t ** 2 * p2.x
    y = (1 - t) ** 2 * p0.y + 2 * t * (1 - t) * p1.y + t ** 2 * p2.y
    return x, y


class BezierAnimation:
    TIME_VEL = 0.02

    def __init__(self, p1, p2, start_point=(0, 0), end_point=(1, 1), mult_vel=1, start_on=True):
        self.TIME_VEL *= mult_vel
        self.p0 = Point(start_point[0], start_point[1])
        self.p1 = Point(p1[0], p1[1])
        self.p2 = Point(p2[0], p2[1])
        self.p3 = Point(end_point[0], end_point[1])

        self.running = start_on
        self.position = (0, 0)
        self.t = 0

    def set_speed(self, speed):
        self.TIME_VEL = 0.02 * speed

    def stop(self):
        self.running = False
        self.t = 0

    def move(self, delta_time_multiplied):
        if self.running:
            self.t += self.TIME_VEL * delta_time_multiplied
            if self.t > 1:
                self.t = 1
                self.running = False

            self.position = calculate_cubic(self.p0, self.p1, self.p2, self.p3, self.t)

    def restart_animation(self):
        self.running = True
        self.t = 0

    # Retorna el valor de Y en base a la variable del tiempo
    def get_value(self):
        return self.position[1]

    # Retorna la posicion en base al tiempo
    def get_pos(self, mult=1):
        return self.position[0] * mult, self.position[1] * mult
