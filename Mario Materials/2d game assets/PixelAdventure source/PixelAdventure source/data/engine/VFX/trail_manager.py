from .utils.functions import simulation_to_display_position
import pygame


def reduce_line_tail(last_point: list, other: list, reduce_factor: float) -> list:
    """
    Retorna la posicion del punto aproximada
    por cierto factor: reduce_factor
    """

    dx = last_point[0] - other[0]
    dy = last_point[1] - other[1]
    distance = (dx * dx + dy * dy) ** 0.5
    new_distance = distance - reduce_factor
    if new_distance > 0:
        return [
            other[0] + (dx / distance) * new_distance,
            other[1] + (dy / distance) * new_distance
        ]
    return other


class TrailManager:
    """
    Clase que se encarga de dibujar y actializar todos los
    trails de todos los objetos
    """

    def __init__(self, trail_lenght: int, update_delay=10):
        self.TRAIL_LENGHT = trail_lenght
        self.UPDATE_DELAY = update_delay

        # Lista que guarda los trails de todos los objetos
        self.trail_positions = []

        # Diccionario ID: Trail de todos los objetos visibles
        # Las posiciones que contiene son en base a la camara
        self.visible = {}

        self.last_trail_update = 0

    def change_lenght(self, trail_lenght: int):
        """
        Cambia la cantidad de posiciones que
        se guardan para dibujar el trail
        """
        self.TRAIL_LENGHT = trail_lenght
        lenght = len(self.trail_positions)
        trail_positions = []
        for index in range(lenght):
            trail_positions.append(
                [
                    self.trail_positions[index][0]
                    for _ in range(self.TRAIL_LENGHT)
                ]
            )
        self.trail_positions = trail_positions.copy()

    def clear(self):
        self.trail_positions = []
        self.visible = {}
        self.last_trail_update = 0

    def recalculate_trails(self, zoom, scroll, objects):

        """
        Re-Calcula las posiciones de los trails visibles.
        Se debe de usar cuando la camara se mueve o hace
        zoom
        """

        visiblesid = [ID for ID in self.visible if self.visible[ID]]
        for ID in visiblesid:
            index = objects[ID].get_list_index()
            self.visible[ID] = [
                simulation_to_display_position(self.trail_positions[index][i], scroll, zoom)
                for i in range(self.TRAIL_LENGHT)
            ]

    def update(
            self,
            actual_positions,
            visible_trailed_objs: list,
            objects: dict,
            simulation_time: float,
            zoom,
            scroll
    ) -> None:
        # Actual positions es la lista con todas las posiciones de los objetos
        """Actualizo el trail cada 100ms"""
        if simulation_time > self.last_trail_update + self.UPDATE_DELAY:
            self.last_trail_update = simulation_time

            # Agrego todas las posiciones de los objetos sin importar sin estan visibles
            for index, trail_single_object in enumerate(self.trail_positions):
                trail_single_object.pop(0)
                trail_single_object.append(
                    [
                        actual_positions[index][0],
                        actual_positions[index][1]
                    ]
                )

            # Agrego la posicion a la lista de visibles
            for ID in visible_trailed_objs:
                self.visible[ID].append(
                    simulation_to_display_position(
                        objects[ID].pos, scroll, zoom
                    )
                )

            # Borra las posiciones iniciales
            for ID, trail in self.visible.items():
                if trail:
                    self.visible[ID].pop(0)

    def new_visible_object(self, zoom, scroll, object_ID: int, object_index: int):

        """
        Siempre que aparezca un objeto nuevamente se crea
        la lista con las posiciones previas del mismo
        """
        self.visible[object_ID] = [
            simulation_to_display_position(
                self.trail_positions[object_index][index],
                scroll,
                zoom
            )
            for index in range(self.TRAIL_LENGHT)
        ]

    def add_trail(self, object_id, object_position, N):

        """
        Agrega un nuevo trail con la posicion del objeto pasado por parametro,
        manteniendo el resto de los trails en sus posiciones
        """

        previus_list = self.trail_positions.copy()
        previus_list.append(
            [(int(object_position[0]), int(object_position[1])) for _ in range(self.TRAIL_LENGHT)]
        )

        self.trail_positions = list(
            [previus_list[i][iteration] for iteration in range(self.TRAIL_LENGHT)] for i in range(N)
        )
        self.visible[object_id] = [(int(object_position[0]), int(object_position[1])) for _ in range(self.TRAIL_LENGHT)]

    def remove_trail(self, ID, previus_index: dict, trailed_objects: list):

        """
        Borra un trail de la lista que contiene todos los trails.
        Esta lista debe actualizarse en base al nuevo indice de
        los objetos
        """

        positions_list = self.trail_positions.copy()

        self.trail_positions = []
        for index, obj in enumerate(trailed_objects):
            # Guardo todas las posiciones del objeto en la nueva lista
            self.trail_positions.append(
                positions_list[previus_index[obj.ID]]
            )

        # Se borra definitivamente la lista que
        # contiene los posibles puntos visibles
        del self.visible[ID]

    def draw(self, surface, objects: dict):

        if not self.visible:
            return

        # Solamente dibuja los trails actualmente visibles
        for ID, lines in self.visible.items():

            if lines:
                pygame.draw.lines(
                    surface,
                    objects[ID].trail_color,
                    False,

                    lines + [
                        [
                            int(objects[ID].display_position[0]),
                            int(objects[ID].display_position[1])
                        ]
                    ],

                    5
                )