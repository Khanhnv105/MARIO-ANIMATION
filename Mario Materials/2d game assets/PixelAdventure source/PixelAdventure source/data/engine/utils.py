from pygame import Surface
from typing import Tuple


def draw_centered(
        surface: Surface,
        image: Surface,
        position: Tuple[int, int]
):
    surface.blit(
        image,
        (
            position[0] - image.get_width() // 2,
            position[1] - image.get_height() // 2
        )
    )


def game_position_to_display(
        position: Tuple[float, float],
        zoom: float,
        scroll: Tuple[float, float]
) -> Tuple[int, int]:
    """Convierte la posicion de el juego a la posicion de la pantalla
    """

    return (
        int(position[0] * zoom - scroll[0]),
        int(position[1] * zoom - scroll[1])
    )


def display_position_to_game(
        display_position: Tuple[float, float],
        zoom: float,
        scroll: Tuple[float, float]
) -> Tuple[float, float]:
    """Convierte la posicion de la pantalla a la del juego"""

    return (
        display_position[0] / zoom + scroll[0],
        display_position[1] / zoom + scroll[1]
    )
