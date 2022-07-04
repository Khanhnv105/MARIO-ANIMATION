import pygame

from .container import Container
from pygame.locals import *

from ..elements.button import Button


class KeyControllableFrame(Container):
    """
    Frame que se controla unicamente mediante
    teclas, para esto al agregar los elementos
    crea un grid map para poder seleccionar
    los elementos con mayor facilidad
    """

    def __init__(self, rect):
        super().__init__(rect)
        self.selected_element = None

    def add(self, other):
        super().add(other)

        if not hasattr(other, "selected"):
            return

        if other.selected:
            self.selected_element = other

    def select(self, name):
        for element in self:
            if element.NAME == name:
                self.set_selected(element, False)

    def set_selected(self, selected_element, check_visibility=True):

        if self.selected_element:
            self.selected_element.set_selected(False)

        self.selected_element = selected_element
        self.selected_element.set_selected(True)
        for element in self:
            if element.NAME != self.selected_element.NAME and issubclass(element.__class__, Button):
                element.set_selected(False)

    def key_pressed(self, event):
        key = event.key
        x_mod = 0
        y_mod = 0
        if key == K_LEFT:
            x_mod = -1
        elif key == K_RIGHT:
            x_mod = 1
        elif key == K_UP:
            y_mod = -1
        elif key == K_DOWN:
            y_mod = 1

        if y_mod:
            self.y_displacement(y_mod)
        elif x_mod:
            self.x_displacement(x_mod)

        # Button pressed
        if key == K_RETURN or key == K_c:
            self.selected_element.pressed()

    def y_displacement(self, direction):
        """
        Busca el elemento con el valor de Y mas cercano al
        previo en base a la direccion que se tome
        """
        actual_y = self.selected_element.rect.y
        selected_element = None
        closest_distance = float("inf")
        distance = lambda p1, p2: ((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1])) ** 0.5
        visible_elements = self._get_visible_buttons()

        # Baja
        if direction == 1:
            next_y = float("inf")
            for element in visible_elements:

                if not self._selectable_element(element):
                    continue

                dist = distance(element.rect.center, self.selected_element.rect.center)
                if actual_y < element.rect.y < next_y or (dist < closest_distance and actual_y < element.rect.y):
                    closest_distance = dist
                    selected_element = element
                    next_y = element.rect.y

        # Sube
        else:
            next_y = 0
            for element in visible_elements:

                if not self._selectable_element(element):
                    continue

                dist = distance(element.rect.center, self.selected_element.rect.center)
                if actual_y > element.rect.y > next_y or (dist < closest_distance and actual_y > element.rect.y):
                    closest_distance = dist
                    selected_element = element
                    next_y = element.rect.y

        if selected_element:
            self.set_selected(selected_element)

    def x_displacement(self, direction):
        """
                Busca el elemento con el valor de Y mas cercano al
                previo en base a la direccion que se tome
                """

        closest_distance = float("inf")
        actual_x = self.selected_element.rect.x
        selected_element = None
        distance = lambda p1, p2: ((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1])) ** 0.5
        visible_elements = self._get_visible_buttons()
        # Derecha
        if direction == 1:
            next_x = float("inf")
            for element in visible_elements:

                if not self._selectable_element(element):
                    continue

                dist = distance(element.rect.center, self.selected_element.rect.center)
                if actual_x < element.rect.x < next_x or (dist < closest_distance and actual_x < element.rect.x):
                    closest_distance = dist
                    selected_element = element
                    next_x = element.rect.x

        # Sube
        else:
            next_x = 0
            for element in visible_elements:

                if not self._selectable_element(element):
                    continue

                dist = distance(element.rect.center, self.selected_element.rect.center)
                if actual_x > element.rect.x > next_x or (dist < closest_distance and actual_x > element.rect.x):
                    closest_distance = dist
                    selected_element = element
                    next_x = element.rect.x

        if selected_element:
            self.set_selected(selected_element)

    def _selectable_element(self, element):
        if not issubclass(element.__class__, Button):
            return

        if not element.selectable:
            return

        return True

    def _get_visible_buttons(self):
        return [element for element in self if
                issubclass(element.__class__, Button) and self._is_element_visible(element)]

    def _is_element_visible(self, element):
        rect = pygame.Rect(
            self.rect.x + element.rect.x - self.last_offset.x,
            self.rect.y + element.rect.y - self.last_offset.y,
            element.rect.w,
            element.rect.h
        )
        return self.rect.colliderect(rect)
