import pygame


def draw_centered(surface, image, position):
    surface.blit(
        image,
        (
            position[0] - image.get_width() // 2,
            position[1] - image.get_height() // 2
        )
    )

def apply_filter(image, color):
    final_image = image.copy()
    filter_color = pygame.Color(color[0], color[1], color[2], color[3])
    surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    surface.fill(filter_color)

    blitted = final_image.copy()
    blitted.blit(surface, (0, 0))

    for x in range(image.get_width()):
        for y in range(image.get_height()):
            color = image.get_at((x, y))
            if color[3]:
                final_image.set_at((x, y), blitted.get_at((x, y)))

    return final_image