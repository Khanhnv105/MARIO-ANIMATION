from typing import List
from pygame.math import Vector2


def display_to_game(display_position, scroll, zoom) -> Vector2:
    return Vector2(
        (display_position[0] + scroll[0]) / zoom,
        (display_position[1] + scroll[1]) / zoom
    )


def game_to_display(simulation_position, scroll, zoom) -> Vector2:
    return Vector2(
        simulation_position[0] * zoom - scroll[0],
        simulation_position[1] * zoom - scroll[1]
    )
