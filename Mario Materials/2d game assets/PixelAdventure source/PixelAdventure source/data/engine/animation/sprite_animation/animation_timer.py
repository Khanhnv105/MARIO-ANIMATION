class AnimationTimer:
    """
    Clase que se encarga de cambiar el indice
    para iterar por las imagenes que forman la animacion
    """

    def __init__(self, images_list_length: int, delay=30, cycle_mode="REPEAT"):

        """
        @images_list_length: Largo de la lista de imagenes
        @delay: Tiempo que tarda en cambiar de indice
        @cycle_mode: Una vez terminada la animacion se usa la
                     configuracion cycle_mode.
                        - REPEAT: Reinicia la animacion
                        - BOUNCE: Hace la inversa al terminar
        """

        # if images_list_length <= 1:
        #    raise Exception(f"La animacion debe de tener mas que {images_list_length} frames")

        self._CYCLE_MODE = cycle_mode.upper()
        self._DELAY = delay

        self._LIST_LAST_INDEX = images_list_length - 1
        self._actual_index = 0
        self._frame_time_left = delay
        self._mult = 1
        self._running = True

    def update(self, dt):

        """
        Reduce el tiempo restante del frame y si es que
        se acaba entonces cambia el indice del frame actual
        """

        if self.is_running():
            self._frame_time_left -= dt

            if self._frame_time_left <= 0:
                self._frame_time_left = self._DELAY
                self._actual_index += 1 * self._mult

                if self.out_of_bounds():
                    if self._CYCLE_MODE == "REPEAT":
                        self._actual_index = 0

                    elif self._CYCLE_MODE == "BOUNCE":
                        self._mult *= -1
                        if self._actual_index > self._LIST_LAST_INDEX:
                            self._actual_index = self._LIST_LAST_INDEX
                        else:
                            self._actual_index = 0

                    elif self._CYCLE_MODE == "END":
                        self.stop()

    def out_of_bounds(self) -> bool:
        """
        Si es que el indice actual pertenece al conjunto
        de los indicesde la lista de imagenes
        """
        return (
                self._actual_index > self._LIST_LAST_INDEX
                or self._actual_index < 0
        )

    def get_image_index(self) -> int:
        return self._actual_index

    def get_cycle_mode(self):
        return self._CYCLE_MODE

    def reset(self):
        self._actual_index = 0
        self._frame_time_left = self._DELAY
        self._mult = 1
        self._running = True

    """
    Estos dos metodos solamente van a ser usados en 
    el caso de que la animacion tenga un solo ciclo
    """

    def is_running(self):
        return self._running

    def run(self):
        self._running = True

    def stop(self):
        self._running = False
        self._actual_index = 0
