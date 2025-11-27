from scripts.player import Player
from scripts.playersaveman import PlayerSaveMan
from scripts.role import Role, RoleTemplMan
import random
import arcade
import arcade.gui as gui

class GameView(gui.UIView):
    def __init__(self, player: Player):
        super().__init__()
        self.player = player
        self.create_ui()

    def on_command_role(self, event):
        pass

    def on_command_bag(self, event):
        pass

    def on_command_summon(self, event):
        self.summon_panel.visible = not self.summon_panel.visible

    def on_command_summon_roles(self, count: int):
        role_ids = random.choices(RoleTemplMan.get_all_roles(), k=count)
        for tid in role_ids:
            role = Role(tid)
            self.player.add_role(role)
            print(f"获得角色：{role.template.name}")
        save_man = PlayerSaveMan()
        save_man.save_player(self.player)

    def create_ui(self):
        anchor = gui.UIAnchorLayout()
        
        # player info
        self.image_player = gui.UISpace(color=arcade.color.AERO_BLUE, width=40, height=40)
        self.label_name = gui.UILabel(text=f"{self.player.name}", font_size=16)
        self.label_level = gui.UILabel(text=f"Lv.{99}", font_size=16)
        self.player_panel = gui.UIBoxLayout(vertical=False, space_between=20)
        self.player_panel.with_padding(all=10)
        self.player_panel.with_background(color=arcade.color.DARK_GRAY)
        self.player_panel.add(self.image_player)
        self.player_panel.add(self.label_name)
        self.player_panel.add(self.label_level)
        anchor.add(self.player_panel, anchor_x="left", anchor_y="top", align_x=20, align_y=-20)

        # menu
        bw = 80
        bh = 40
        button_role = gui.UIFlatButton(text="角色", width=bw, height=bh)
        button_role.on_click = self.on_command_role
        button_bag = gui.UIFlatButton(text="背包", width=bw, height=bh)
        button_bag.on_click = self.on_command_bag
        button_summon = gui.UIFlatButton(text="召唤", width=bw, height=bh)
        button_summon.on_click = self.on_command_summon
        self.menu_panel = gui.UIBoxLayout(vertical=False, space_between=10)
        self.menu_panel.with_padding(all=10)
        self.menu_panel.with_background(color=arcade.color.DARK_GRAY)
        self.menu_panel.add(button_role)
        self.menu_panel.add(button_bag)
        self.menu_panel.add(button_summon)
        anchor.add(self.menu_panel, anchor_x="right", anchor_y="top", align_x=-20, align_y=-20)

        # summon
        image1 = gui.UISpace(color=arcade.color.AFRICAN_VIOLET, width=200, height=200)
        image10 = gui.UISpace(color=arcade.color.AFRICAN_VIOLET, width=200, height=200)
        button1 = gui.UIFlatButton(text="召唤 1 次", width=200, height=60)
        button1.on_click = lambda event: self.on_command_summon_roles(1)
        button10 = gui.UIFlatButton(text="召唤 10 次", width=200, height=60)
        button10.on_click = lambda event: self.on_command_summon_roles(10)
        self.summon_panel = gui.UIGridLayout(row_count=2, column_count=2, horizontal_spacing=10, vertical_spacing=20)
        self.summon_panel.with_padding(all=20)
        self.summon_panel.with_background(color=arcade.color.AIR_FORCE_BLUE)
        self.summon_panel.add(image1, row=0, column=0)
        self.summon_panel.add(image10, row=0, column=1)
        self.summon_panel.add(button1, row=1, column=0)
        self.summon_panel.add(button10, row=1, column=1)
        self.summon_panel.visible = False
        anchor.add(self.summon_panel, anchor_x="center", anchor_y="center")

        self.add_widget(anchor)
