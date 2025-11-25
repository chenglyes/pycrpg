import sys
import os
sys.path.append(os.getcwd())

from scripts.roletempl import RoleTemplMan
from scripts.skilltempl import SkillTemplMan
from scripts.bufftempl import BuffTemplMan
from scripts.role import Role
from scripts.fight import Fight
from scripts.fightwithactqueue import FightWithActQueue

def get_actor_name(info: dict):
    actor: Role = info["role"]
    team: int = info["team"]
    field: int = info["field"]
    return f"{actor.template.name}(队伍{team},位置{field})"

def print_fight(fight: Fight, actions: list[dict]):
    for action in actions:
        match action["type"]:
            case "begin_fight":
                print("战斗开始！")
            case "end_fight":
                print(f"战斗结束！队伍 {action["winner"]} 获胜！")
            case "begin_round":
                print(f"第 {action["round"]} 回目开始：")
            case "end_round":
                print(f"第 {action["round"]} 回目结束。")
            case "begin_turn":
                info = fight.get_role_info(action["actor"])
                print(f"现在是 {get_actor_name(info)} 的回合：")
            case "end_turn":
                info = fight.get_role_info(action["actor"])
                print(f"{get_actor_name(info)} 的回合结束了。")
            case "cast_skill":
                info = fight.get_role_info(action["actor"])
                actor = info["role"]
                skill = actor.get_skill(action["skill"])
                print(f"{get_actor_name(info)} 使用了技能 {skill.template.name} ！")
            case "take_damage":
                info = fight.get_role_info(action["actor"])
                actor = info["role"]
                caster = fight.get_role(action["caster"])
                value = action["value"]
                left = action["left"]
                source_type = action["source_type"]
                source_id = action["source_id"]
                if source_type == "skill":
                    skill = caster.get_skill(source_id)
                    print(f"{get_actor_name(info)} 失去了 {value} 生命！由于技能 {skill.template.name}。当前生命：{left}")
                else:
                    buff_tmpl = BuffTemplMan.get(source_id)
                    assert(buff_tmpl is not None)
                    print(f"{get_actor_name(info)} 失去了 {value} 生命！由于BUFF {buff_tmpl.name}。当前生命：{left}")
            case "died":
                info = fight.get_role_info(action["actor"])
                print(f"{get_actor_name(info)} 死了！")
            case "add_buff":
                actor_info = fight.get_role_info(action["actor"])
                actor = actor_info["role"]
                caster_info = fight.get_role_info(action["caster"])
                caster = caster_info["role"]
                buff_tmpl = BuffTemplMan.get(action["buff"])
                assert(buff_tmpl is not None)
                stack = action["stack"]
                duration = action["duration"]
                print(f"{get_actor_name(actor_info)} 获得了BUFF {buff_tmpl.name}({stack}层 {duration}回合)，施加者：{get_actor_name(caster_info)}")
            case "stack_buff":
                actor_info = fight.get_role_info(action["actor"])
                actor = actor_info["role"]
                caster_info = fight.get_role_info(action["caster"])
                caster = caster_info["role"]
                buff_tmpl = BuffTemplMan.get(action["buff"])
                assert(buff_tmpl is not None)
                stack = action["stack"]
                duration = action["duration"]
                print(f"{get_actor_name(actor_info)} 叠加了 BUFF {buff_tmpl.name}({stack}层{duration}回合)，施加者：{get_actor_name(caster_info)}")
            case "remove_buff":
                info = fight.get_role_info(action["actor"])
                buff_tmpl = BuffTemplMan.get(action["buff"])
                assert(buff_tmpl is not None)
                print(f"{get_actor_name(info)} 失去了BUFF {buff_tmpl.name}")

if __name__ == "__main__":
    RoleTemplMan.load("data/roles.json")
    SkillTemplMan.load("data/skills.json")
    BuffTemplMan.load("data/buffs.json")

    team1: list[Role] = []
    team1.append(Role("r001"))
    #team1.append(Role("r001"))
    #team1.append(Role("r001"))
    team2: list[Role] = []
    team2.append(Role("r002"))

    #fight = Fight()
    fight = FightWithActQueue()
    fight.add_team(team1)
    fight.add_team(team2)

    print(f"seed={fight.seed}")

    actions = fight.simulate()
    print_fight(fight, actions)
