from data.engine.animation.sprite_animation.animations_controller import AnimationsController


class SwordAnimationsController(AnimationsController):
    def __init__(self, animations_json_path: str):
        super().__init__(animations_json_path)

    def update(self, dt, **kwargs):

        # Si es que la animacion actual esta corriendo
        if self.ANIMATIONS[self.actual_animation]["timer"].is_running():
            self.ANIMATIONS[self.actual_animation]["timer"].update(dt)
        else:
            self.actual_animation = "IDLE"

    def start_animation(self, animation_name: str) -> None:

        """
        Frena a la animacion anterior, en el caso de que
        haya una animacion no IDLE e inicia la nueva animacion
        """

        if self.actual_animation != "IDLE":
            self.ANIMATIONS[self.actual_animation]["timer"].stop()
        self.actual_animation = animation_name
        self.ANIMATIONS[self.actual_animation]["timer"].run()

    def running_animation(self) -> bool:
        """
        Retorna si es que hay alguna animacion la cual
        no sea IDLE
        """
        return self.actual_animation != "IDLE"
