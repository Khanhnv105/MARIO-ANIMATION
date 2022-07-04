import pygame
from .entity import Entity
from .input_entity import InputEntity


def sorted_dict(dictionaty: dict, reversed_keys: bool):
    """
    Ordena al diccionario en base a las keys y
    lo retorna, manteniendo los elementos de cada una
    de las keys
    """

    if reversed_keys:
        keys = reversed(sorted(dictionaty.keys()))
    else:
        keys = sorted(dictionaty.keys())

    return {key: dictionaty[key] for key in keys}


class EntitiesGroup:
    """
    Clase para organizar todas las entidades
    que interactuan en el juego.
    Funcionalidades:
        - Layers: Simplemente el orden en el que se dibujan
          tambien se puede usar para colisiones, de tal forma
          que el diccionario de entidades se re-organiza
        - Las entidades tienen la capacidad de acceder a
          el diccionario pasado en __init__ cuando se eliminan
        - Lista que guarda las entidades visibles
        - Capacidad de las entidades de cambiar su estado de
          visibilidad dentro de su propio metodo update
    """

    def __init__(self, scene):
        self._all_entities = []
        self._entities = {}
        self._visible_entities = {}
        self._entities_with_input = []
        self.game_scene = scene
        self._update_not_visible = True

    def update_not_visible(self, state):
        self._update_not_visible = state

    def __len__(self):
        return len(self._all_entities)

    def __repr__(self):
        return f"<{self.__class__.__name__} ({len(self)} entities)>"

    def __bool__(self):
        return len(self) > 0

    def __iter__(self):
        return iter(self._all_entities)

    def clear(self):
        self._all_entities = []
        self._entities = {}
        self._visible_entities = {}
        self._entities_with_input = []

    def key_down(self, event):
        for entity in self._entities_with_input:
            entity.check_key_down(event)

    def key_up(self, event):
        for entity in self._entities_with_input:
            entity.check_key_up(event)

    def key_held(self):
        for entity in self._entities_with_input:
            entity.check_hey_held()

    def change_visible_dict(self, visible_entities_list):

        """
        Borra el diccionatio de entidades que estaban visibles
        en la iteracion anterior y agrega las nuevas, las que
        si estan visibles actualmente. Estas son pasadas
        en forma de lista a traves parametro
        """

        for layer in self._visible_entities:
            for entity in self._visible_entities[layer]:
                entity.set_visible(False)

        new_dict = {}
        for entity in visible_entities_list:
            entity.set_visible(True)
            layer = entity.get_layer()
            if layer not in new_dict:
                new_dict[layer] = []
            new_dict[layer].append(entity)

        self._visible_entities = new_dict

    def visible_entities_len(self) -> int:
        """Retorna la cantidad de entidades visibles"""
        return sum([len(self._visible_entities[layer]) for layer in self._visible_entities])

    def get_entities_list(self) -> list:
        """Retorna una lista que contiene todas las entidades"""
        return self._all_entities

    def get_entities_layered(self, sort=False, reversed_keys=False):
        """Retorna un dict de todas las entidades con la posibilidad de ordenar sus keys"""
        if sort:
            return sorted_dict(self._entities, reversed_keys)
        return self._entities

    def get_visible_entities_list(self):
        lists = (list(self.get_visible_entities_layered().values()))
        final_list = []
        for l in lists:
            final_list += l
        return final_list

    def get_visible_entities_layered(self, sort=False, reversed_keys=False) -> dict:

        """
        Retorna las entidades visibles. Si es que el parametro sort es True los
        indices del diccionario se ordenan. En el caso de que reversed_keys
        los indices se retornan de la siguiente manera [0, 1, 2, 3, 4], caso contrario
        se rotorna como [4, 3, 2, 1]
        """
        if sort:
            return sorted_dict(self._visible_entities, reversed_keys)
        return self._visible_entities

    def get_entities_from_layer(self, layer: int) -> list:
        """Retorna todas las entidades de un layer especifico"""
        return self._entities[layer]

    def change_layer(self, entity: Entity, layer: int) -> None:
        """Cambia la entidad de layer"""
        previus_layer = entity.get_layer()
        self._remove_entity_from_layer(entity, previus_layer)
        self._add_entity_to_layer(entity, layer)

    def switch_layer(self, layer1: int, layer2: int) -> None:
        """Cambia las entidades de dos layers"""
        layer1_entities = self.get_entities_from_layer(layer1)
        layer2_entities = self.get_entities_from_layer(layer2)
        self._change_layer_list(layer1, layer2_entities)
        self._change_layer_list(layer2, layer1_entities)

    def empty(self) -> None:
        """Vacia todas las listas"""
        self._all_entities.clear()
        self._entities.clear()
        self._visible_entities.clear()

    def set_visible(self, visible: bool, entity: Entity) -> None:

        """
        Metodo para cambiar el estado de visibilidad.
        Simplemente agrega o elimina la entidad de la
        lista de entidades visibles
        """
        layer = entity.get_layer()

        # Si es que la entidad no esta en la lista de visibles
        if entity not in self._visible_entities[layer]:

            if visible:
                self._visible_entities[layer].append(entity)

        # Si es que si esta en la lista de visibles
        # y ademas quiere borrarse de la misma
        elif not visible:
            self._visible_entities[layer].remove(entity)

    def add(self, entity: Entity) -> None:
        """Agrega una nueva entidad al grupo"""

        layer = entity.get_layer()

        # Si es que no existen listas en el layer
        # entonces las crea
        if layer not in self._entities:
            self._entities[layer] = []
            self._visible_entities[layer] = []

        self._add_entity_to_layer(entity, layer)
        self._all_entities.append(entity)

        if issubclass(entity.__class__, InputEntity):
            self._entities_with_input.append(entity)

    def delete(self, entity: Entity) -> None:
        """
        Borra la entidad, pasando por parametro
        toda la informacion con acceso al juego
        """
        entity.deleting(self.game_scene)
        self._remove_entity_from_layer(entity, entity.get_layer())
        self._all_entities.remove(entity)

        if entity in self._entities_with_input:
            self._entities_with_input.remove(entity)

    def update(self, **kwargs):
        """Actualiza todas las entidades"""

        self.key_held()

        if self._update_not_visible:
            for entity in self._all_entities:
                entity.update(**kwargs)
        else:
            for layer in self._visible_entities:
                for entity in self._visible_entities[layer]:
                    entity.update(**kwargs)

    def draw(self, surface: pygame.Surface, offset=(0, 0)):

        """
        Solamente dibuja las entidades
        que se encuentren visibles. Dibuja
        en base a los layers, de tal forma
        que el layer con el valor mas alto
        se dibuja primero y el de menor valor
        se dibuja ultimo
        """
        for layer in self.get_visible_entities_layered(sort=True):
            for entity in self._visible_entities[layer]:
                entity.draw(surface, offset)

    def _remove_entity_from_layer(self, entity: Entity, layer: int):

        """Borra la entidad de las listas del layer"""
        self._entities[layer].remove(entity)

        if entity in self._visible_entities[layer]:
            self._visible_entities[layer].remove(entity)

    def _add_entity_to_layer(self, entity: Entity, layer: int):

        """Agrega la entidad al layer"""
        self._entities[layer].append(entity)

        if entity.is_visible():
            self._visible_entities[layer].append(entity)

        entity.set_layer(layer)

    def _change_layer_list(self, layer, entities):
        """
        Cambia la lista de entidades del layer
         por la pasada por parametro
         """
        self._entities[layer] = entities
        self._visible_entities[layer] = entities

        for entity in entities:
            entity.set_layer(layer)
