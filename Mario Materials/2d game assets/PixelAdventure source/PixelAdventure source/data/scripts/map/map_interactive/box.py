from data.engine.animation.sprite_animation.animations_controller import AnimationsController
from data.engine.entity.image_collideable_entity import ImageCollideableEntity


class Box(ImageCollideableEntity):
    def __init__(self, group, position, box_type: int = 1):
        self.animator = AnimationsController(self._load_animations(box_type))
        super().__init__(group, position, self.animator.get_image(), layer=1)
        self.hit = False
        self.breaking = False

    def collision(self, other) -> None:
        if other.type == "Player" and not self.hit:
            self.animator.restart_animation("Hit")
            self.hit = True

    def update(self, **kwargs) -> None:

        if self.hit and not self.animator.is_running("Hit"):
            self.hit = False
            self.delete()

        self.animator.update(
            dt=kwargs['dt'],
            hit=self.hit,
            breaking=self.breaking
        )
        self.image = self.animator.get_image()

    def draw(self, surface, offset=(0, 0)):
        surface.blit(
            self.image,
            (
                self.rectangle.x - offset[0],
                self.rectangle.y - offset[1]
            )
        )

    def _load_animations(self, box_type):
        animations = {
            "Break": {
                "delay": 3,
                "cycle_mode": "END",
                "images_path": f"data/Assets/Free/Items/Boxes/Box{box_type}/Break",
                "conditions": ["breaking"],
                "images_colorkey": [0, 0, 0],
                "images_scale": 2
            }, "Hit": {
                "delay": 3,
                "cycle_mode": "END",
                "images_path": f"data/Assets/Free/Items/Boxes/Box{box_type}/Hit (28x24)",
                "conditions": ["hit"],
                "images_colorkey": [0, 0, 0],
                "images_scale": 2
            }, "IDLE": {
                "delay": 3,
                "cycle_mode": "END",
                "images_path": f"data/Assets/Free/Items/Boxes/Box{box_type}/Idle",
                "conditions": ["breaking"],
                "images_colorkey": [0, 0, 0],
                "images_scale": 2
            }}

        return animations
