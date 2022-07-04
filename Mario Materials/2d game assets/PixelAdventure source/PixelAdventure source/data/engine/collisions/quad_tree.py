from .collideable import Collideable
import pygame
from pygame.rect import Rect


class QuadTree:
    MAX_OBJECTS = 4
    MAX_LEVELS = 10

    def __init__(self, level, rectangle):
        self.level = level
        self.rectangle = Rect(rectangle[0], rectangle[1], rectangle[2], rectangle[3])
        self.divided = False
        self.nodes = []
        self.objects = []

    def clear(self):
        """
        Reinicia todas las listas, tanto la de
        los nodos como la de los objetos
        """
        self.objects.clear()
        for node in self.nodes:
            node.clear()
        self.nodes.clear()

    def get_all_nodes(self, all_nodes_list):
        """
        Retorna una lista con todos los nodos del sistema
        """
        all_nodes_list.append(self.rectangle)
        if len(self.nodes) > 0:
            for node in self.nodes:
                node.getAllNodes(all_nodes_list)
        return all_nodes_list

    def split(self):
        """
        Divide el area del Quad Tree en cuatro regiones
        """
        sub_width = self.rectangle.w // 2
        sub_height = self.rectangle.h // 2
        x = self.rectangle.x
        y = self.rectangle.y

        self.nodes.append(QuadTree(self.level + 1, Rect(x + sub_width, y, sub_width, sub_height)))
        self.nodes.append(QuadTree(self.level + 1, Rect(x, y, sub_width, sub_height)))
        self.nodes.append(QuadTree(self.level + 1, Rect(x, y + sub_height, sub_width, sub_height)))
        self.nodes.append(QuadTree(self.level + 1, Rect(x + sub_width, y + sub_height, sub_width, sub_height)))

    def get_index(self, obj):
        """
        Retorna el cuadrante en el cual se encuentra el objeto
        basado en su posición el el QuadTree
        """
        if len(self.nodes) <= 0:
            return -1
        if obj.fits_in_node(self.nodes[0].rectangle):
            return 0
        elif obj.fits_in_node(self.nodes[1].rectangle):
            return 1
        elif obj.fits_in_node(self.nodes[2].rectangle):
            return 2
        elif obj.fits_in_node(self.nodes[3].rectangle):
            return 3
        else:
            return -1

    def insert_object(self, obj):
        # Check to insert in existing subnodes
        if len(self.nodes) > 0:
            subNodeIndex = self.get_index(obj)
            if subNodeIndex > -1:
                self.nodes[subNodeIndex].insert_object(obj)
                return

        # Add to the parent
        self.objects.append(obj)
        # If exceeds limit then split and add
        if len(self.objects) > self.MAX_OBJECTS:
            if len(self.nodes) == 0 and self.level < self.MAX_LEVELS:
                self.split()

            # Lista en la que se guardan los objetos
            # que van a pertenecer a este quad tree
            newObjects = []
            for objec_t in self.objects:
                subNodeIndex = self.get_index(objec_t)
                if subNodeIndex > -1:
                    self.nodes[subNodeIndex].insert_object(objec_t)
                else:
                    newObjects.append(objec_t)

            self.objects = newObjects

    def query(self, rect, found=None):

        """
        Retorna los puntos que colisionen con
        el rectangulo del parametro
        """

        if type(found) != list:
            found = []

        if not self.rectangle.colliderect(rect):
            return
        else:
            # En caso de que algun punto colisione
            # con el rect entonces lo agrego
            for obj in self.objects:
                #if obj.does_intersect(rect):
                found.append(obj)

            for node in self.nodes:
                node.query(rect, found)

            return found

    def rectangular_collision(self, rectangle):
        possible_collisions = self.query(rectangle)
        return possible_collisions

    def get_possible_collisions(self, collideable: Collideable):
        """
        Retorna una lista de objetos con los cuales
        el objeto del paramentro este posiblemente
        colisionando
        """
        sub_node_index = self.get_index(collideable)
        objects_list = []
        if sub_node_index > -1:
            objects_list.extend(self.objects)
            objects_list.extend(self.nodes[sub_node_index].get_possible_collisions(collideable))
        else:
            objects_list.extend(self.objects)
            if len(self.nodes) > 0:
                for node in self.nodes:
                    if collideable.does_intersect(node.rectangle):
                        objects_list.extend(node.get_possible_collisions(collideable))

        return objects_list

    def draw(self, surface, color=(50, 250, 50), thickness=2, offset=(0, 0)):
        rect = self.rectangle.x - offset[0], self.rectangle.y - offset[1], self.rectangle.w, self.rectangle.h
        pygame.draw.rect(surface, color, rect, thickness)
        for node in self.nodes:
            node.draw(surface, color, thickness, offset)
