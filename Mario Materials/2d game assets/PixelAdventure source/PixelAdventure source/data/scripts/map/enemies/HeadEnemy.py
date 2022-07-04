from data.engine.animation.sprite_animation.animations_controller import AnimationsController
from data.engine.entity.image_collideable_entity import ImageCollideableEntity
from data.engine.math.vector import Vector
from data.engine.animation.math_animation.bezier_animation import BezierAnimation
from data.engine.physics.rectangular_physical_entity import RectangularPhysicalEntity
from data.scripts.map.enemies.enemy import Enemy
from data.scripts.map.tile.tile import Tile


class HeadEnemy(ImageCollideableEntity, RectangularPhysicalEntity, Enemy):
    def __init__(self, group, position, points, type="Spike", start_index=0):
        self.animations_controller = AnimationsController(self._get_dynamic_loaded_animations(type))
        image = self.animations_controller.get_image()

        ImageCollideableEntity.__init__(self, group, position, image)

        collisions_rectangle = self.rectangle.copy()
        w_sub = int(self.rectangle.w / 6)
        h_sub = int(self.rectangle.h / 6)
        collisions_rectangle.x += w_sub
        collisions_rectangle.y += h_sub
        collisions_rectangle.w -= w_sub * 2
        collisions_rectangle.h -= h_sub * 2

        RectangularPhysicalEntity.__init__(self, collisions_rectangle)
        self.position = Vector(position[0] + image.get_width() // 2, position[1] + image.get_width() // 2)
        self.points = [Vector(x, y) for x, y in points]

        # Image animation
        if start_index < len(self.points) - 2:
            self.actual_index = start_index
            self.next_index = start_index + 1

        elif start_index < len(self.points) - 1:
            self.actual_index = start_index
            self.next_index = 0

        else:
            self.actual_index = 0
            self.next_index = 1

        self.attack_step = 0
        self.attacking = False
        self.attack_bezier_animation = BezierAnimation((.22, .51), (.05, 1.04))

        self._change_target()

    def get_position(self):
        return Vector(self.rectangle.center[0], self.rectangle.center[1])

    def fits_in_node(self, node_rect) -> bool:
        return False

    def does_intersect(self, node_rect) -> bool:
        return True

    def collides(self, other) -> bool:
        return super().collides(other)

    def _move(self, dt):
        self.update_x_pos(dt)
        self.set_center_pos(self.position.x, self.position.y)
        previous = self.rectangle.copy()
        self.rectangle = self.collisions_rectangle
        collisions = self.collisions_manager.get_filtered_static_collisions_by_subclass(self, Tile)

        for other in collisions:

            if self.velocity.x:
                # Collides Right
                if self.velocity.x > 0:
                    self.set_right_pos(other.rectangle.left)
                    self.animations_controller.start_animation("RIGHT_HIT")
                    self._shake()

                    self._change_target()
                # Collides left
                else:
                    self.set_left_pos(other.rectangle.right)
                    self.animations_controller.start_animation("LEFT_HIT")
                    self._shake()

                    self._change_target()

                self.velocity.x = 0

        self.update_y_pos(dt)
        self.set_center_pos(self.position.x, self.position.y)
        collisions = self.collisions_manager.get_filtered_static_collisions_by_subclass(self, Tile)

        for other in collisions:
            if self.velocity.y:
                # Collides bottom
                if self.velocity.y > 0:
                    self.set_bottom_pos(other.rectangle.top)
                    self.animations_controller.start_animation("BOTTOM_HIT")
                    self._shake()
                    self._change_target()

                # Collides top
                else:
                    self.set_top_pos(other.rectangle.bottom)
                    self.animations_controller.start_animation("TOP_HIT")
                    self._shake()
                    self._change_target()
                self.velocity.y = 0

        self.rectangle = previous

    def update(self, **kwargs) -> None:
        self.animations_controller.update(
            kwargs["dt"],
            right=False,
            left=False,
            top=False,
            bottom=False
        )
        self.set_visible(self.rectangle.colliderect(kwargs["display_rect"]))

        # Solamete se va a mover cuando no hayan
        # animaciones de colision corriendo
        if not self._running_collision_animation():
            magnitude = self.velocity.get_length()
            self.velocity = self.velocity.normalized() * (magnitude + 0.15 * kwargs["dt"])
            self._move(kwargs["dt"])
            self.set_center_pos(self.position.x, self.position.y)

        self.image = self.animations_controller.get_image()
        self.update_data()


    def draw(self, surface, offset=(0, 0)):

        surface.blit(
            self.image,
            (
                self.rectangle.x - offset[0],
                self.rectangle.y - offset[1]
            )
        )
    def set_center_pos(self, x, y):
        super().set_center_pos(x, y)
        self.rectangle.centerx = x
        self.rectangle.centery = y

    def _collided(self, animation_name):
        if self._running_collision_animation():
            self.animations_controller.start_animation(animation_name)

    def _change_target(self):

        self.actual_index = self.next_index
        self.next_index += 1
        if self.next_index > len(self.points) - 1:
            self.next_index = 0

        final_position = self.points[self.actual_index]
        initial_position = self.points[self.next_index]
        distance = final_position - initial_position
        self.velocity = distance.normalized()

    def _running_collision_animation(self):
        animations = "BOTTOM_HIT", "TOP_HIT", "LEFT_HIT", "RIGHT_HIT"
        return any([self.animations_controller.is_running(animation_name) for animation_name in animations])

    def _shake(self):

        if self.is_visible():
            x = -self.velocity.x / abs(self.velocity.x) if self.velocity.x else 0
            y = -self.velocity.y / abs(self.velocity.y) if self.velocity.y else 0

            self.group.game_scene.camera.push(Vector(x, y) * 3)

    def _get_dynamic_loaded_animations(self, head_type) -> dict:

        return {
            "RIGHT_HIT": {
                "delay": 5,
                "cycle_mode": "END",
                "images_path": f"data/Assets/Free/Traps/{head_type} Head/Right Hit",
                "conditions": ["right"],
                "images_colorkey": None,
                "images_scale": 2
            },
            "LEFT_HIT": {
                "delay": 5,
                "cycle_mode": "END",
                "images_path": f"data/Assets/Free/Traps/{head_type} Head/Left Hit",
                "conditions": ["left"],
                "images_colorkey": None,
                "images_scale": 2
            },
            "TOP_HIT": {
                "delay": 5,
                "cycle_mode": "END",
                "images_path": f"data/Assets/Free/Traps/{head_type} Head/Top Hit",
                "conditions": ["top"],
                "images_colorkey": None,
                "images_scale": 2
            },
            "BOTTOM_HIT": {
                "delay": 5,
                "cycle_mode": "END",
                "images_path": f"data/Assets/Free/Traps/{head_type} Head/Bottom Hit",
                "conditions": ["bottom"],
                "images_colorkey": None,
                "images_scale": 2
            },
            "IDLE": {
                "delay": 10,
                "cycle_mode": "REPEAT",
                "images_path": f"data/Assets/Free/Traps/{head_type} Head/Idle",
                "conditions": [],
                "images_colorkey": None,
                "images_scale": 2
            }
        }
