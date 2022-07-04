class Key:
    """
    Contiene el codigo de la Key y ademas
    y nombre para poder hacerle referencia
    mediante un string
    """
    def __init__(self, name, value):
        self.name = name
        self.code = value

    def __eq__(self, other):
        return self.code == other

    def __contains__(self, item):
        return self.code == item


class InputEntity:
    """
    Clase que sirve para que el Input sea llamado desde
    la clase EntitiesGroup, de esta forma el input se
    programa dentro de la clase de la entidad la cual
    sea una subclase de InputEnity. Ademas permite identificar
    a las teglas mediante el keyword del __init__, de esta forma
    ya no se necesita importar los codigos de pygame
    """

    def __init__(self, input_blocked, **kwargs):


        self._keys = []
        for name in kwargs:
            if type(kwargs[name]) == tuple:
                self._keys.append(Key(name, kwargs[name][0]))
                self._keys.append(Key(name, kwargs[name][1]))
            else:
                self._keys.append(Key(name, kwargs[name]))

        #self._keys = [Key(name, value) for name, value in zip(kwargs.keys(), kwargs.values())]

        # Contiene los nombres asignados a las teclas
        self._held = []
        self._blocked = input_blocked

    def restart_key_states(self):
        self._held.copy()

    """Metodos principales a ser sobreescribidos"""
    def keys_held(self, names):
        pass

    def key_down(self, name):
        pass

    def key_up(self, name):
        pass

    """Metodos para controlar si la entidad puede recibir input o no"""
    def block_input(self):
        self._blocked = True

    def activate_input(self):
        self._blocked = False

    """Metodos a ser llamados por el Group """
    def check_key_up(self, event):
        # Key up puede ser usado incluso cuando el input
        # este bloqueado
        if event.key in self._keys:
            # Si es que se suelta la tecla y la misma estaba en
            # la lista de presionadas entonces se quita
            name = self._get_key_name(event.key)
            if name in self._held:
                self._held.remove(name)

            self.key_up(name)

    def check_key_down(self, event):
        if not self._blocked:
            if event.key in self._keys:
                # Se agrega la tecla
                name = self._get_key_name(event.key)
                self._held.append(name)
                self.key_down(name)

    def check_hey_held(self):
        if not self._blocked:
            self.keys_held(self._held)

    def holding_key(self, *name):
        if self._blocked:
           return False

        for key_name in self._held:
            for n in name:
                if key_name == n:
                    return True
        return False

    def _get_key(self, code):
        return [key for key in self._keys if code == key.code][0]

    def _get_key_name(self, code):
        return self._get_key(code).name

