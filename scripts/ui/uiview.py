import arcade
from arcade.gui import UIManager

class UIView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = UIManager()
        self.on_init()

    def on_init(self):
        pass
        
    def on_show_view(self) -> None:
        self.manager.enable()

    def on_hide_view(self) -> None:
        self.manager.disable()

    def on_update(self, delta_time: float):
        self.manager.on_update(delta_time)

    def on_draw(self):
        self.manager.draw()
