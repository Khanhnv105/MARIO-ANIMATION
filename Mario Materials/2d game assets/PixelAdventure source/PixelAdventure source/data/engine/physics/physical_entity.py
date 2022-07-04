from data.engine.math.vector import Vector


class PhysicalEntity:

    """
    Clase que tiene las propiedades
    basicas para poder realizar las
    interacciones entre las entidades
    del juego
    """

    def __init__(self, position, velocity):
        self.position = Vector(position[0], position[1])
        self.velocity = Vector(velocity[0], velocity[1])
        self.acceleration = Vector()

    def push(self, vector) -> None:
        if type(vector) == Vector:
            self.velocity += vector
        else:
            self.velocity += Vector(vector[0], vector[1])

    def distance_to(self, other) -> float:
        return (self.position - other.position).length

    def get_vector_to(self, other) -> Vector:
        if issubclass(other.__class__, PhysicalEntity):
            return self.position - other.position
        elif issubclass(other.__class__, Vector):
            return self.position - other

    def accelerate(self, vector):
        if isinstance(vector, Vector):
            self.acceleration += vector
        else:
            self.acceleration.x += vector[0]
            self.acceleration.y += vector[1]

    def update_physics(self, delta):
        self.update_velocity(delta)
        self.position += self.velocity * delta

    def update_velocity(self, delta):
        self.velocity += self.acceleration * delta
        self.acceleration.x = 0
        self.acceleration.y = 0

    def update_x_pos(self, delta):
        self.position.x += self.velocity.x * delta

    def update_y_pos(self, delta):
        self.position.y += self.velocity.y * delta

    def push_towards(self, other, magnitude):

        """
        Reinicia la velocidad y empuja a la entidad
        hacia el punto deseado con la magnitud
        pasada por parametro
        """

        if isinstance(other, Vector):
            normalized = (self.position - other).normalized()
        else:
            normalized = (self.position - other.position).normalized()

        self.velocity = normalized * magnitude