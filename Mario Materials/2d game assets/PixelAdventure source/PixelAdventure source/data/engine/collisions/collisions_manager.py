from .collideable import Collideable
from .quad_tree import QuadTree


class CollisionsManager:
    """
    La clase CollisionsManager ayuda a administrar
    las colisiones, usando un QuadTree de rectangulos
    para lograr la maxima optimizacion posible. Todos
    los objetos que se quieran verificar deben de
    ser una subclase de Collideable
    """

    def __init__(self, map_size):
        self.check_objects = []
        self.quad_tree = QuadTree(0, (0, 0, map_size[0], map_size[1]))
        self.static_quad_tree = QuadTree(0, (0, 0, map_size[0], map_size[1]))

    """Dynamic Quad Tree"""

    def add_object(self, obj):
        self.quad_tree.insert_object(obj.insert_to_quad())

    def check_object(self, obj: Collideable) -> None:
        """
        Se agrega el objeto a la cola de checkeos de
        colisiones, dada a la probabilidad de que el
        mismo colisione
        """
        self.check_objects.append(obj)

    def update(self, **kwargs):
        """
        1 - Si es que hay objetos en la cola de checkeo de colision
        2 - Reinicia el quad
        3 - Inserta todos los objetos nuevamente
        4 - Busca las colisiones de los objetos en check_objects
        5 - Reinicia la lista check_objects dado a que ya se verificaron las colisiones
        """
        if self.check_objects:
            self.quad_tree.clear()

            for obj in kwargs["objects"]:
                self.add_object(obj)

            self._collisions()
        self.check_objects.clear()

    def _collisions(self):

        """
        Itera en todos los objetos de posible colision
        Obtiene los objetos cercanos a el mismo y verifica las
        colisiones, en el caso de que colisionen, se hacen los
        llamados respectivos a sus funciones de colision
        :return:
        """

        for obj in self.check_objects:
            self._single_collision(obj)

    def _single_collision(self, obj: Collideable):
        collisions = self.get_collisions(obj)
        for other in collisions:
            obj.collision(other)
            other.collision(obj)

    def get_collisions(self, obj) -> list:
        """Retorna todas las colisiones con el objeto del parametro"""
        possible_collisions = self.quad_tree.get_possible_collisions(obj)
        if obj in possible_collisions:
            possible_collisions.remove(obj)
        return [other for other in possible_collisions if obj.collides(other)]

    def get_filtered_collisions(self, obj, other_group_class: str):
        """
        Busca las colisiones y solanente retorna a los objetos con los
        que este colisionando que sean de la clase pasada por parametro
        """
        collisions = self.get_collisions(obj)
        return [other for other in collisions if other.__class__.__name__ == other_group_class]

    """Static Quad Tree"""

    def add_static_object(self, obj):
        self.static_quad_tree.insert_object(obj.insert_to_quad())

    def get_static_collisions(self, obj) -> list:
        """Retorna todas las colisiones con el objeto del parametro"""
        possible_collisions = self.static_quad_tree.get_possible_collisions(obj)
        if obj in possible_collisions:
            possible_collisions.remove(obj)
        return [other for other in possible_collisions if obj.collides(other)]

    def get_filtered_static_collisions_by_subclass(self, obj, main_class):
        """Retorna las colisiones con todos los objetos que sean subclase de 'main_class'"""
        collisions = self.get_static_collisions(obj)
        return [other for other in collisions if issubclass(other.__class__, main_class)]

    def get_filtered_static_collisions(self, obj, *other_group_class):
        """
        Busca las colisiones y solanente retorna a los objetos con los
        que este colisionando que sean de la clase pasada por parametro
        """
        collisions = self.get_static_collisions(obj)
        return [other for other in collisions if other.__class__.__name__ in other_group_class]

    def query(self, rect):
        dynamic = self.quad_tree.query(rect)
        static = self.static_quad_tree.query(rect)
        if dynamic and static:
            return dynamic + static
        if dynamic:
            return dynamic
        if static:
            return static

        return []

    def filtered_query_subclass(self, rect, subclass):
        collisions = self.query(rect)
        return [other for other in collisions if issubclass(other.__class__, subclass)]
