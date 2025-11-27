from scripts.playersaveman import Player, PlayerView, PlayerSaveMan
from typing import override
import arcade
import arcade.gui as gui

class SaveView(gui.UIView):
    def __init__(self):
        super().__init__()
        self.save_man = PlayerSaveMan()
        self.create_ui()

    def on_command_player(self, player_view: PlayerView):
        player = self.save_man.load_player(player_view.uid)
        from .gameview import GameView
        self.window.show_view(GameView(player))

    def on_command_remove_player(self, player_view: PlayerView):
        self.save_man.remove_player(player_view.uid)
        self.create_ui()

    def on_command_add(self, event):
        self.save_man.add_player(Player("新的存档"))
        self.create_ui()

    def on_command_back(self, event):
        from .welcomeview import WelcomeView
        self.window.show_view(WelcomeView())
    
    def create_ui(self):
        self.ui.clear()
        anchor = self.add_widget(gui.UIAnchorLayout())
        vbox = anchor.add(
            gui.UIBoxLayout(
                vertical=True, space_between=10
            ),
            anchor_x="center_x", anchor_y="center_y"
        )
        vbox.add(gui.UILabel(
            text="选择/创建存档", font_size=60, width=300, height=80
        ))
        for player_view in self.save_man.player_views:
            vbox.add(self.create_player_button(player_view))
        add_button = vbox.add(gui.UIFlatButton(
            text="+", width=600, height=80
        ))
        add_button.on_click = self.on_command_add
        back_button = vbox.add(gui.UIFlatButton(
            text="返回", width=200, height=50
        ))
        back_button.on_click = self.on_command_back

    def create_player_button(self, player_view: PlayerView) -> gui.UIWidget:
        root = gui.UIBoxLayout(vertical=False, space_between=10)
        player_button = root.add(gui.UIFlatButton(
            width=540, height=80
        ))
        player_button.on_click = lambda event: self.on_command_player(player_view)
        hbox = player_button.add(gui.UIBoxLayout(vertical=False, space_between=10))
        hbox.add(gui.UILabel(
            text=f"{player_view.name}", font_size=16, width=250
        ))
        hbox.add(gui.UILabel(
            text=f"创建时间：{player_view.create_time}", font_size=16, text_color=arcade.color.LIGHT_GRAY
        ))
        remove_button = root.add(gui.UIFlatButton(
            text="删除", width=50, height=80, style=gui.UIFlatButton.STYLE_RED
        ))
        remove_button.on_click = lambda event: self.on_command_remove_player(player_view)
        return root
    