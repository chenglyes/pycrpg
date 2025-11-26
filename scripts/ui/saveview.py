from .uiview import UIView
from scripts.playersaveman import Player, PlayerView, PlayerSaveMan
import arcade
import arcade.gui as gui

class SaveView(UIView):
    def on_command_player(self, player: PlayerView):
        print(f"click player: {player.name}")

    def on_command_remove_player(self, player: PlayerView):
        print(f"click delete player: {player.name}")
        self.save_man.remove_player(player.uid)
        self.create_ui()

    def on_command_add(self, event):
        print("click add")
        self.save_man.add_player(Player("新的存档"))
        self.create_ui()

    def on_command_back(self, event):
        print("click back")

    def on_init(self):
        self.save_man = PlayerSaveMan()
        self.create_ui()

    def create_ui(self):
        self.manager.clear()
        anchor = self.manager.add(gui.UIAnchorLayout())
        vbox = anchor.add(
            gui.UIBoxLayout(
                vertical=True, space_between=10
            ),
            anchor_x="center_x", anchor_y="center_y"
        )
        vbox.add(gui.UILabel(
            text="选择/创建存档", font_size=60, width=300, height=80
        ))
        for player in self.save_man.player_views:
            vbox.add(self.create_player_button(player))
        add_button = vbox.add(gui.UIFlatButton(
            text="+", width=600, height=80
        ))
        add_button.on_click = self.on_command_add
        back_button = vbox.add(gui.UIFlatButton(
            text="返回", width=200, height=50
        ))
        back_button.on_click = self.on_command_back

    def create_player_button(self, player: PlayerView) -> gui.UIWidget:
        root = gui.UIBoxLayout(vertical=False, space_between=10)
        player_button = root.add(gui.UIFlatButton(
            width=540, height=80
        ))
        player_button.on_click = lambda event: self.on_command_player(player)
        hbox = player_button.add(gui.UIBoxLayout(vertical=False, space_between=10))
        hbox.add(gui.UILabel(
            text=f"{player.name}", font_size=16, width=250
        ))
        hbox.add(gui.UILabel(
            text=f"创建时间：{player.create_time}", font_size=16, text_color=arcade.color.LIGHT_GRAY
        ))
        remove_button = root.add(gui.UIFlatButton(
            text="删除", width=50, height=80, style=gui.UIFlatButton.STYLE_RED
        ))
        remove_button.on_click = lambda event: self.on_command_remove_player(player)
        return root

    def on_draw(self):
        self.clear()
        super().on_draw()
