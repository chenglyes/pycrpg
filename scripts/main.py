from roletemplman import RoleTemplMan
from skilltemplman import SkillTemplMan
from bufftemplman import BuffTemplMan
from role import Role
from fight import Fight
from fightwithactqueue import FightWithActQueue

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
                actor = fight.get_role(action["actor"])
                print(f"现在是 {actor.template.name} 的回合：")
            case "end_turn":
                actor = fight.get_role(action["actor"])
                print(f"{actor.template.name} 的回合结束了。")
            case "cast_skill":
                actor = fight.get_role(action["actor"])
                skill = actor.get_skill(action["skill"])
                print(f"{actor.template.name} 使用了技能 {skill.template.name} ！")
            case "take_damage":
                actor = fight.get_role(action["actor"])
                value = action["value"]
                left = action["left"]
                print(f"{actor.template.name} 失去了 {value} 生命！当前生命：{left}")
            case "died":
                actor = fight.get_role(action["actor"])
                print(f"{actor.template.name} 死了！")
            case "add_buff":
                actor = fight.get_role(action["actor"])
                caster = fight.get_role(action["caster"])
                buff_tmpl = BuffTemplMan.get(action["buff"])
                assert(buff_tmpl is not None)
                stack = action["stack"]
                duration = action["duration"]
                print(f"{actor.template.name} 获得了BUFF {buff_tmpl.name}({duration}回合)，施加者：{caster.template.name}")
            case "remove_buff":
                actor = fight.get_role(action["actor"])
                buff_tmpl = BuffTemplMan.get(action["buff"])
                assert(buff_tmpl is not None)
                print(f"{actor.template.name} 失去了BUFF {buff_tmpl.name}")

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
