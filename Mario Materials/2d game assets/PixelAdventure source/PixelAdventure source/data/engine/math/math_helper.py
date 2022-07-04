from math import pi, atan


def distance(p1, p2):
    """
    Retorna la distancia entre dos puntos
    """
    return ((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))**0.5


def get_cartesian_angle(x, y):
    """
    Retorna la tangente del punto en un supuesto
    sistema cartesiano, esta función convierte los
    ángulos negativos o incorrectos que retorna la
    tangente en ángulos correctos en un sistema radial
    """

    if x > 0 and y > 0:  # Primer cuadrante
        return atan(y / x)

    # Segundo, tercer cuadrante tienen la misma solución
    if (x < 0 and y > 0) or (x < 0 and y < 0):
        return atan(y / x) + pi

    if x > 0 and y < 0:
        return atan(y / x) + pi * 2

    # En el caso de que X = 0
    if x == 0:
        # Ángulo recto
        if y > 0:
            return pi / 2
        # Angulo recto opuesto
        return pi * 1.5

    # En el caso de que Y = 0
    if y == 0:
        # Ángulo nulo
        if x > 0:
            return 0
        # Ángulo llano
        return pi
