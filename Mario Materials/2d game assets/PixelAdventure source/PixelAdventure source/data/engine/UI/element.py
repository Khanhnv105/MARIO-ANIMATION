import pygame

from data.engine.UI.constants import CLICKED_EVENT


class Element:
    def __init__(self, name, rect):
        self.rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
        self.NAME = name

    def __eq__(self, other):
        return self.NAME == other.NAME

    def added(self, frame):
        pass

    def update(self, **kwargs):
        pass

    def draw(self, surface, top_left_root):
        pass

    def _get_data(self) -> dict:
        """Metodo que retorna la informacion que luego va a ser visible en el evento"""
        return {
            "ELEMENT": self,
            "NAME": self.NAME,
            "TYPE": self.__class__.__name__
        }

    def _post_clicked(self):
        event = pygame.event.Event(CLICKED_EVENT, self._get_data())
        pygame.event.post(event)

    def pressed(self):
        """Metodo que llama el frame una vez que el boton se presione"""
        pass
