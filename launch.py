from scripts.roletempl import RoleTemplMan
from scripts.skilltempl import SkillTemplMan
from scripts.bufftempl import BuffTemplMan
from scripts.role import Role
from scripts.playersaveman import Player, PlayerSaveMan
from scripts.ui.welcomeview import WelcomeView
import random
import arcade

if __name__ == "__main__":
    window = arcade.Window(800, 600, "PYCRPG", center_window=True)
    arcade.run(WelcomeView())

    RoleTemplMan.load("data/roles.json")
    SkillTemplMan.load("data/skills.json")
    BuffTemplMan.load("data/buffs.json")

    save_man = PlayerSaveMan()
    if not save_man.player_views:
        player = Player("Deafult Player")
        save_man.add_player(player)

    for v in save_man.player_views:
        print(v)

    player_view = save_man.player_views[0]
    player = save_man.load_player(player_view.uid)

    role_ids = random.choices(RoleTemplMan.get_all_roles(), k=10)
    for tid in role_ids:
        role = Role(tid)
        player.add_role(role)
        print(f"获得角色：{role.template.name}")

    save_man.update_player(player)
