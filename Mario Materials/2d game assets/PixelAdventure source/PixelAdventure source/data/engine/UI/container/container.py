import pygame

from data.engine.math.vector import Vector


class Container:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
        self.elements = []
        self.elements_dict = {}
        self.last_offset = Vector()

    def __iter__(self):
        return iter(self.elements)

    def add(self, other):
        self.elements.append(other)
        if other.NAME in self.elements_dict:
            raise Exception("Repeated element NAME attribute")
        self.elements_dict[other.NAME] = other
        other.added(self)

    def put(self, *elements):
        for element in elements:
            self.add(element)

    def update(self, **kwargs):
        for element in self:
            element.update(**kwargs)

    def draw(self, surface, offset=(0, 0)):
        self.last_offset = offset
        top_left = self.rect.x - offset[0], self.rect.y - offset[1]

        for element in self:
            element.draw(surface, top_left)
