

class UI_Manager:
    def __init__(self, root):
        self.root = root

    def update(self, **kwargs):
        self.root.update(**kwargs)

    def draw(self, surface, offset):
        self.root.draw(surface, offset)

    def handle_key_pressed(self, event):
        self.root.key_pressed(event)