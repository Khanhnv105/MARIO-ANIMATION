import pygame

from .animation_timer import AnimationTimer
from data.engine.json.json_management import get_data
from data.engine.tile.tile_set_loader import load_folder


class AnimationsController:
    """
        Clase que se encarga de organizar y controlar todas
        las  animaciones de una entidad. Estas animaciones se
    cargan desde un archivo .json el cual contiene todas las
    especificaciones de todas las animaciones de la entidad.

        Una animacion se activa cuando las otras animaciones
    de mayor jerarquia no cumplen con su condicion y esta
    animacion si lo hace.

        En el caso de que ninguna animación cumpla con sus
    condiciones se va a recurrir a la animacion impresindible
    llamada "IDLE"

    """

    def __init__(self, animations):
        """
        El parametro animations puede ser un dict con toda la informacion
        de la animacion o el path para que se busque la animacion guaradada
        en el disco

        Formato de la animacion. Toda animacion debe
        tener un IDLE agregado al final del archivo
        {
            "Jump Animation": {
                "delay": 30,
                "cycle_mode": "REPEAT",
                "images_path": "assets/..",
                "conditions": ["on_air", "moving left"],
                "images_colorkey": None,
                "images_scale": 1
            },
            "IDLE": ...
        }
        """

        self.actual_animation = "IDLE"
        self.special_running_animation = None
        self.ANIMATIONS = {}
        if type(animations) == str:
            self._load_animations(get_data(animations))

        else:
            self._load_animations(animations)


    def is_running(self, animation_name):
        return self.ANIMATIONS[animation_name]["timer"].is_running()

    def stop(self, animation_name):
        self.ANIMATIONS[animation_name]["timer"].stop()

    def get_image_from_animation(self, animation_name: str, index: int):
        """Retorna la imagen de cualquier animacion y frame del mismo"""
        return self.ANIMATIONS[animation_name]["images"][index]

    def get_image(self) -> pygame.Surface:
        """Retorna la imagen de la animacion actual"""
        images = self.ANIMATIONS[self.actual_animation]["images"]
        actual_image_index = self.ANIMATIONS[self.actual_animation]["timer"].get_image_index()
        return images[actual_image_index]


    def restart_animation(self, animation):
        self.ANIMATIONS[animation]["timer"].reset()

    def start_animation(self, end_animation_name):
        """
        Inicia una animacion del tipo end y la termina, sin importar
        que las condiciones de las otras animaciones se cumplan
        """
        timer = self.ANIMATIONS[end_animation_name]["timer"]
        if timer.get_cycle_mode() != "END":
            raise Exception("The start animation is only compatible with END cycle mode Timers")
        timer.reset()
        self.special_running_animation = end_animation_name

    def update(self, dt, **kwargs):

        """
        Loop por cada una de las animaciones, si es que
        se cumplen las condiciones de la animacion entonces se la
        usa y se la guarda como activa. Caso contrario se
        usa la animacion IDLE.
        """

        if self.special_running_animation is not None:
            self.ANIMATIONS[self.special_running_animation]["timer"].update(dt)
            self.actual_animation = self.special_running_animation

            if not self.is_running(self.special_running_animation):
                self.stop(self.special_running_animation)
                self.special_running_animation = None
                self.actual_animation = "IDLE"
        else:

            self.actual_animation = "IDLE"

            for animation in self.ANIMATIONS:

                if animation != "IDLE":

                    if self._check_conditions(self.ANIMATIONS[animation]["conditions"], kwargs):
                        self.ANIMATIONS[animation]["timer"].update(dt)

                        # Si es que se cambia de animacion se reinician las otras
                        if animation != self.actual_animation:
                            for other_animation in self.ANIMATIONS:

                                timer = self.ANIMATIONS[other_animation]["timer"]
                                if other_animation != animation and timer.get_cycle_mode() != "END":
                                    timer.reset()

                        self.actual_animation = animation
                        break

            if self.actual_animation == "IDLE":
                self.ANIMATIONS["IDLE"]["timer"].update(dt)

    def _check_conditions(self, conditions: list, conditions_state: dict):

        """
        Retorna si es que se cumplen todas las condiciones
        que requiere la animacion para ser ejecutada
        """

        states = {}
        for condition in conditions:
            states[condition] = conditions_state[condition]

        return all(list(states.values()))

    def _load_animations(self, animations_data: dict):

        """Carga todas las animaciones del dict"""

        for animation_name, data in animations_data.items():
            # Imagenes de la animacion
            images = load_folder(
                path=data["images_path"],
                colorkey=data["images_colorkey"],
                scale=data["images_scale"],
                sorted_images=True
            )

            # Timer que controla el ciclo de la animacion
            timer = AnimationTimer(
                len(images),
                data["delay"],
                data["cycle_mode"]
            )

            if data["cycle_mode"] == "END":
                timer.stop()

            self.ANIMATIONS[animation_name] = {
                "images": images,
                "timer": timer
            }

            if animation_name != "IDLE":
                # Condicion que debe de cumplirse
                # para usar la animacion
                self.ANIMATIONS[animation_name]["conditions"] = data["conditions"]

        if "IDLE" not in self.ANIMATIONS:
            raise Exception("Siempre tiene que haber una animacion IDLE")

        if not self.ANIMATIONS:
            raise Exception("Instancia de AnimationController sin animaciones")
