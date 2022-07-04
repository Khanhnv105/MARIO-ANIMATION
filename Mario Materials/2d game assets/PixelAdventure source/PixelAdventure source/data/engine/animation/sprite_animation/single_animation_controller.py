from pygame import Surface
from data.engine.animation.sprite_animation.animation_timer import AnimationTimer
from data.engine.json.json_management import get_data
from data.engine.tile.tile_set_loader import load_folder


class SingleAnimationController:

    def __init__(self, animation):

        if type(animation) == str:
            data = get_data(animation)

        else:
            data = animation

        self.images = load_folder(
            path=data["images_path"],
            colorkey=data["images_colorkey"],
            scale=data["images_scale"],
            sorted_images=True
        )
        self.animator = AnimationTimer(
            images_list_length=len(self.images),
            delay=data["delay"],
            cycle_mode=data["cycle_mode"]
        )

    def is_running(self) -> bool:
        return self.animator.is_running()

    def reset(self):
        self.animator.reset()

    def update(self, dt):
        self.animator.update(dt)

    def get_image(self) -> Surface:
        return self.images[self.animator.get_image_index()]
