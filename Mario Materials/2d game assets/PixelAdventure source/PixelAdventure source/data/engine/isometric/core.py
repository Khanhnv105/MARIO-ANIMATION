import math
from typing import *


def cartesian_to_isometric(
        cartesian_x: float,
        cartesian_y: float
) -> Tuple[float, float]:
    """Dada una posicion cartesiana retorna la posicion isometrica"""
    return (
        cartesian_x - cartesian_y,
        (cartesian_x + cartesian_y) / 2
    )


def isometric_to_cartesian(
        isometric_x: float,
        isometric_y: float
) -> Tuple[float, float]:
    """Dada una posicion isometrica retorna la cartesiana"""
    return (
        (2 * isometric_y + isometric_x) / 2,
        (2 * isometric_y - isometric_x) / 2
    )


def get_isometric_tile_fit_position(
        isometric_x,
        isometric_y,
        tile_x_gap,
        tile_y_gap
) -> Tuple[float, float]:
    """
    Retorna la posicion isometrica de
    tal forma que los tiles encajen
    """
    return (
        (isometric_x // tile_x_gap) * tile_x_gap,
        (isometric_y // tile_y_gap) * tile_y_gap
    )


def mouse_to_cartesian(
        mouse: Tuple[int, int],
        scroll: Tuple[float, float],
        grid_width: int,
        grid_height: int
) -> Tuple[int, int]:
    """
    Retorna la posicion del mouse en un sistema cartesiano,
    teniendo en cuenta que la posicion del mouse se encuentra
    en un sistema isometrico
    """
    return (
        math.floor(
            ((mouse[1] + scroll[1]) / grid_height) +
            ((mouse[0] - grid_height + scroll[0]) / grid_width)
        ),
        math.floor(
            ((mouse[1] + scroll[1]) / grid_height) -
            ((mouse[0] - grid_height + scroll[0]) / grid_width)
        )
    )
