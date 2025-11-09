from roletemplman import RoleTemplMan
from skilltemplman import SkillTemplMan
from role import Role
from fight import Fight

if __name__ == "__main__":
    RoleTemplMan.load("data/roles.json")
    SkillTemplMan.load("data/skills.json")

    team1: list[Role] = []
    team1.append(Role("r001"))
    team2: list[Role] = []
    team2.append(Role("r001"))

    fight = Fight()
    fight.add_team(team1)
    fight.add_team(team2)

    actions = fight.simulate()

    for action in actions:
        print(action)
