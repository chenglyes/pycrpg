from .uipanel import UIPanel
from scripts.player import Player
from scripts.playersaveman import PlayerSaveMan
from scripts.role import Role, RoleTemplMan
import random
import arcade
import arcade.gui as gui

class RolePanel(UIPanel):
    def __init__(self, player: Player, *, x: float = 0, y: float = 0, width: float = 100, height: float = 100):
        super().__init__(x=x, y=y, width=width, height=height)
        self.player = player
        self.roles_grid = gui.UIGridLayout(row_count=4, column_count=3, horizontal_spacing=5, vertical_spacing=5)
        self.image_role = gui.UISpace(color=arcade.color.ALLOY_ORANGE, width=300, height=400)
        self.stats_panel = gui.UIBoxLayout(align="left", vertical=True, space_between=10, width=300, height=400)
        self.stats_panel.with_padding(all=30)
        self.stats_panel.with_background(color=arcade.color.DARK_BLUE_GRAY)
        hbox = gui.UIBoxLayout(vertical=False, space_between=15)
        hbox.with_padding(all=20)
        hbox.with_background(color=arcade.color.AIR_FORCE_BLUE)
        hbox.add(self.roles_grid)
        hbox.add(self.image_role)
        hbox.add(self.stats_panel)
        self.root.add(hbox, anchor_x="center", anchor_y="center")
        self.update()

    def update(self):
        self.roles_grid.clear()
        for i, role in enumerate(self.player.role_collections.roles):
            if i >= self.roles_grid.row_count * self.roles_grid.column_count:
                break
            image = gui.UISpace(color=arcade.color.ALLOY_ORANGE, width=60, height=60)
            label = gui.UILabel(text=role.template.name, font_size=10)
            vbox = gui.UIBoxLayout(vertical=True, space_between=2)
            vbox.with_padding(all=5)
            vbox.add(image)
            vbox.add(label)
            button = gui.UIFlatButton(width=100, height=100)
            button.on_click = lambda event, index=i: self.on_command_role(index)
            button.add(vbox)
            self.roles_grid.add(button, row=i // self.roles_grid.column_count, column=i % self.roles_grid.column_count)
        if self.player.role_collections.roles:
            role = self.player.role_collections.roles[0]
            self.update_role(role)
        else:
            self.update_role(None)

    def on_command_role(self, index: int):
        role = self.player.role_collections.roles[index]
        self.update_role(role)
    
    def update_role(self, role: Role | None):
        self.stats_panel.clear()
        if role:
            stats = role.get_stats()
            label_name = gui.UILabel(text=f"{role.template.name} Lv.100", font_size=20)
            label_health = gui.UILabel(text=f"生    命: {stats.get("health")}", font_size=16)
            label_attack = gui.UILabel(text=f"攻击力: {stats.get("attack")}", font_size=16)
            label_defense = gui.UILabel(text=f"防御力: {stats.get("defense")}", font_size=16)
            self.stats_panel.add(label_name)
            self.stats_panel.add(label_health)
            self.stats_panel.add(label_attack)
            self.stats_panel.add(label_defense)

class SummonPanel(UIPanel):
    def __init__(self, player: Player, *, x: float = 0, y: float = 0, width: float = 100, height: float = 100):
        super().__init__(x=x, y=y, width=width, height=height)
        self.player = player
        image1 = gui.UISpace(color=arcade.color.AFRICAN_VIOLET, width=200, height=200)
        image10 = gui.UISpace(color=arcade.color.AFRICAN_VIOLET, width=200, height=200)
        button1 = gui.UIFlatButton(text="召唤 1 次", width=200, height=60)
        button1.on_click = lambda event: self.on_command_summon_roles(1)
        button10 = gui.UIFlatButton(text="召唤 10 次", width=200, height=60)
        button10.on_click = lambda event: self.on_command_summon_roles(10)
        grid = gui.UIGridLayout(row_count=2, column_count=2, horizontal_spacing=10, vertical_spacing=20)
        grid.with_padding(all=20)
        grid.with_background(color=arcade.color.AIR_FORCE_BLUE)
        grid.add(image1, row=0, column=0)
        grid.add(image10, row=0, column=1)
        grid.add(button1, row=1, column=0)
        grid.add(button10, row=1, column=1)
        self.root.add(grid, anchor_x="center", anchor_y="center")

    def on_command_summon_roles(self, count: int):
        pass

class GameView(gui.UIView):
    def __init__(self, player: Player):
        super().__init__()
        self.player = player
        self.create_ui()

    def on_command_role(self, event):
        self.role_panel.visible = not self.role_panel.visible

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
        self.role_panel.update()

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

        # role
        self.role_panel = RolePanel(self.player, width=1000, height=600)
        self.role_panel.visible = False
        anchor.add(self.role_panel.root, anchor_x="center", anchor_y="center")

        # summon
        self.summon_panel = SummonPanel(self.player)
        self.summon_panel.on_command_summon_roles = self.on_command_summon_roles
        self.summon_panel.visible = False
        anchor.add(self.summon_panel.root, anchor_x="center", anchor_y="center")

        self.add_widget(anchor)
