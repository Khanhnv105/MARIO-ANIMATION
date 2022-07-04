from .quad_tree_object import QuadTreeObject


class Collideable(QuadTreeObject):

    """
    Implementacion de QuadTreeObject para poder
    usar el QuadTree con cualquier tipo de forma
    a traves de los metodos collides() y collision()
    """

    def __init__(self, collisions_manager, rectangle):
        super().__init__(collisions_manager, rectangle)

    def collides(self, other) -> bool:
        pass

    def collision(self, other) -> None:
        """
        Metodo que se llama para
        las tratar las colisiones
        entre todos los objetos
        dinamicos
        """
        pass
