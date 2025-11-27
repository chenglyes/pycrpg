from scripts.roletempl import RoleTemplMan
from scripts.skilltempl import SkillTemplMan
from scripts.bufftempl import BuffTemplMan
import arcade

if __name__ == "__main__":
    RoleTemplMan.load("data/roles.json")
    SkillTemplMan.load("data/skills.json")
    BuffTemplMan.load("data/buffs.json")

    window = arcade.Window(1000, 600, "PYCRPG", center_window=True)
    from scripts.ui.welcomeview import WelcomeView
    arcade.run(WelcomeView())
