import pygame


class QuadTreeObject:
    """
    __class__ es un objeto designado para ser
    heredado por cualquier objeto que requiera
    usar un quad tree, en este caso el quad tree
    se basa en rectangulos para verificar las colisiones,
    luego si es que se detecta colision se puede verificar
    si es que realmenete esta sucediendo con el metodo
    collides(self, other)
    """

    def __init__(self, collisions_manager, rectangle):
        """
        The quad tree object is based on rectangles,
        so all the objects of the quad tree might have
        the same origin of coordinates and scale
        """
        self.rectangle = pygame.Rect(
            rectangle[0],
            rectangle[1],
            rectangle[2],
            rectangle[3]
        )
        self.collisions_manager = collisions_manager
        self.collisions_manager.quad_tree.insert_object(self)

    def fits_in_node(self, node_rect) -> bool:
        """
        Retorna si es que el objeto encaja sin sobresalir de los bordes
        de quad tree
        """
        return (
                (node_rect.x <= self.rectangle.x)
                and (self.rectangle.right <= node_rect.right)
                and (node_rect.y <= self.rectangle.y)
                and (self.rectangle.bottom <= node_rect.bottom)
        )

    def does_intersect(self, node_rect) -> bool:
        """
        Retorna si es que el objeto toca algunos de los
        bordes del rectangulo de quad
        :param node_rect:
        :return:
        """
        if not self.rectangle.colliderect(node_rect):
            return False

        return (
                self.intersects_left(node_rect.left)
                or self.intersects_right(node_rect.right)
                or self.intersects_top(node_rect.top)
                or self.intersects_bottom(node_rect.bottom)
        )

    def intersects_left(self, other_left):
        return self.rectangle.x < other_left < self.rectangle.right

    def intersects_right(self, other_right):
        return self.rectangle.x < other_right < self.rectangle.right

    def intersects_top(self, other_top):
        return self.rectangle.y < other_top < self.rectangle.bottom

    def intersects_bottom(self, other_bottom):
        return self.rectangle.y < other_bottom < self.rectangle.bottom

    def future_collision_check(self):
        """Agrega el objeto a la cola de checkeos de colision"""
        self.collisions_manager.check_object(self)

    def insert_to_quad(self):
        """
        Este metodo lo llama la clase CollisionsManager cada
        vez que se itera por el objeto para agregarlo al quad.
        Se puede usar para reestablecer variables
        :return: self, Collideable
        """
        return self
