import sys
import os
sys.path.append(os.getcwd())

from scripts.roletempl import RoleTemplMan
from scripts.skilltempl import SkillTemplMan
from scripts.bufftempl import BuffTemplMan
from scripts.role import Role
from scripts.player import Player
import random
import json

def save_player(player: Player):
    os.makedirs(f"user/players", exist_ok=True)
    with open(f"user/players/{player.uid}.json", "w", encoding="utf-8") as f:
        json.dump(player.to_saved(), f, indent=4)

def load_player(uid: str) -> Player:
    with open(f"user/players/{uid}.json", "r", encoding="utf-8") as f:
        return Player.from_saved(json.load(f))

if __name__ == "__main__":
    RoleTemplMan.load("data/roles.json")
    SkillTemplMan.load("data/skills.json")
    BuffTemplMan.load("data/buffs.json")

    player =  Player("Test Player")
    print(f"player: {player.uid}, name={player.name}, create_time={player.create_time}")

    role_ids = random.choices(RoleTemplMan.get_all_roles(), k=10)
    for tid in role_ids:
        role = Role(tid)
        player.add_role(role)
        print(f"获得角色：{role.template.name}")

    p = Player.from_saved(player.to_saved())
    print(p)
