from typing import override
import arcade
import arcade.gui as gui

class WelcomeView(gui.UIView):
    def __init__(self):
        super().__init__()
        self.create_ui()

    def on_command_start(self, event):
        from .saveview import SaveView
        self.window.show_view(SaveView())

    def on_command_option(self, event):
        print("click option")

    def on_command_quit(self, event):
        arcade.exit()

    def create_ui(self):
        anchor = self.add_widget(gui.UIAnchorLayout())
        vbox = anchor.add(
            gui.UIBoxLayout(
                vertical=True, space_between=10
            ),
            anchor_x="center_x", anchor_y="center_y"
        )
        vbox.add(gui.UILabel(
            text="某个游戏", font_size=60, width=300, height=80
        ))
        start_button = vbox.add(gui.UIFlatButton(
            text="开始游戏", width=300, height=80, style=gui.UIFlatButton.STYLE_BLUE
        ))
        start_button.on_click = self.on_command_start
        option_button = vbox.add(gui.UIFlatButton(
            text="选项", width=300, height=80, style=gui.UIFlatButton.STYLE_BLUE
        ))
        option_button.on_click = self.on_command_option
        quit_button = vbox.add(gui.UIFlatButton(
            text="退出游戏", width=300, height=80, style=gui.UIFlatButton.STYLE_RED
        ))
        quit_button.on_click = self.on_command_quit
