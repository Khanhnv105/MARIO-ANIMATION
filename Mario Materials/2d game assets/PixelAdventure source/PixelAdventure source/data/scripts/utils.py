
def dynamic_animation_creation(
        images_path,
        delay=3,
        cycle_mode="REPEAT",
        conditions=None,
        images_color_key=None,
        images_scale=1
) -> dict:
    return {
        "delay": delay,
        "cycle_mode": cycle_mode,
        "images_path": images_path,
        "conditions" :conditions if conditions else [],
        "images_colorkey": images_color_key,
        "images_scale": images_scale
    }
