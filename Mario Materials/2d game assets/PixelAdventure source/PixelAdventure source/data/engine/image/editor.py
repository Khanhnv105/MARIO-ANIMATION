import pygame


def get_image_outlined(img, outline_color=(255, 255, 255)):
    """
    Retorna la imagen con un outline de un
    pixel del color determinado por parametro
    """

    mask = pygame.mask.from_surface(img)
    mask_outline = mask.outline()
    mask_surf = pygame.Surface(img.get_size())
    mask_surf.set_colorkey((0, 0, 0))

    for pixel in mask_outline:
        mask_surf.set_at(pixel, outline_color)

    new_surface = pygame.Surface((img.get_width() + 2, img.get_height() + 2), pygame.SRCALPHA)

    new_surface.blit(mask_surf, (0, 1))
    new_surface.blit(mask_surf, (2, 1))
    new_surface.blit(mask_surf, (1, 0))
    new_surface.blit(mask_surf, (1, 2))
    new_surface.blit(img, (1, 1))

    return new_surface.convert_alpha()


def scale_image(image: pygame.Surface, scale: float) -> pygame.Surface:
    """Retorna la imagen escalada por un factor 'scale' """

    return pygame.transform.scale(
        image,
        (
            int(image.get_width() * scale),
            int(image.get_height() * scale)
        )
    )


def get_clip(image, rectangle, transparency=False):
    """Retorna una seccion reducida en base al rectangulo de la surface"""
    if not transparency:
        new_surface = pygame.Surface((rectangle.w, rectangle.h))
    else:
        new_surface = pygame.Surface((rectangle.w, rectangle.h), pygame.SRCALPHA)

    new_surface.blit(
        image,
        (
            -rectangle.x,
            -rectangle.y
        )
    )
    return new_surface.convert() if not transparency else new_surface.convert_alpha()


def crop_image(tileset: pygame.Surface, rect) -> pygame.Surface:
    """
    #Recorta cierta porcion del tileset y retorna la imagen

    image = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    for inside_rect_x in range(rect[2]):
        for inside_rect_y in range(rect[3]):
            pos = inside_rect_x + rect.x, inside_rect_y + rect.y
            image.set_at((inside_rect_x, inside_rect_y), tileset.get_at(pos))

    return image'"""
    return get_clip(tileset, rect, True)

