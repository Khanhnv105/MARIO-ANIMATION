from data.engine.physics.physical_entity import PhysicalEntity


class RectangularPhysicalEntity(PhysicalEntity):

    """
    Clase que cuenta con las fisicas basicas y
    ademas agrega la posibilidad de tener un rectangulo,
    con sus respectivas funciones para poder localizar
    el objeto tanto desde el centro como desde cualquiera
    de las los bordes del rectangulo, si errores
    """

    def __init__(self, rectangle, position=(0, 0), velocity=(0, 0)):
        super().__init__(position, velocity)
        self.collisions_rectangle = rectangle
        self.set_center_pos(position[0], position[1])

    def push(self, vector, constrain_x=None, constrain_y=None, constrain_magnitude=None) -> None:
        super().push(vector)
        self.constrain_velocity(constrain_x, constrain_y, constrain_magnitude)

    def constrain_velocity(self, constrain_x=None, constrain_y=None, constrain_magnitude=None):

        """
        Metodo que puede limitar tanto los valores escalares de las componentes
        color el de la magnitud del vector. Es indiferente del signo, por lo que
        todos los parametros tienen que ser positivos
        """

        if constrain_magnitude:
            self.velocity.constrain(constrain_magnitude)

        else:
            if constrain_x:
                if abs(self.velocity.x) > constrain_x:
                    self.velocity.x = self.velocity.x / abs(self.velocity.x) * constrain_x

            if constrain_y:
                if self.velocity.y > constrain_y:
                    self.velocity.y = self.velocity.y / abs(self.velocity.y) * constrain_x

    def set_bottom_pos(self, bottom):
        self.collisions_rectangle.bottom = bottom
        self.position.y = self.collisions_rectangle.centery

    def set_top_pos(self, top):
        self.collisions_rectangle.top = top
        self.position.y = self.collisions_rectangle.centery

    def set_left_pos(self, left):
        self.collisions_rectangle.left = left
        self.position.x = self.collisions_rectangle.centerx

    def set_right_pos(self, right):
        self.collisions_rectangle.right = right
        self.position.x = self.collisions_rectangle.centerx

    def set_center_pos(self, x, y):
        self.set_center_x(x)
        self.set_center_y(y)

    def set_center_x(self, x):
        self.position.x = x
        self.collisions_rectangle.centerx = x

    def set_center_y(self, y):
        self.position.y = y
        self.collisions_rectangle.centery = y
