from eventman import EventMan
from role import Role
from fightrole import FightRole
from fightskill import FightSkill
from buff import Buff
import fightevents
from random import Random

class FightContext:
    def __init__(self, seed: int, init_teams: list[list[Role]]):
        self.random = Random(seed)
        self.event_man = EventMan()
        #self.actor: FightRole | None = None
        #self.actor_queue: list[FightRole] = []
        self.round: int = 0
        self.actions: list[dict] = []
        self.all_roles: list[FightRole] = []
        for i, team in enumerate(init_teams):
            for j, role in enumerate(team):
                self.all_roles.append(FightRole(role, i + 1, j + 1, self))
        self.all_roles.sort(key=lambda r: r.stats.get("speed"), reverse=True)
        for role in self.all_roles:
            role.prepare_fight()

    def dispatch_event(self, event):
        self.log_action("event", {
            "name": type(event).__name__
        })
        self.event_man.dispatch(event)

    def log_action(self, type: str, data: dict = {}):
        action = {"type": type, **data}
        self.actions.append(action)

    def check_winner(self) -> int:
        alive_teams = set()
        for role in self.all_roles:
            if role.is_alive():
                alive_teams.add(role.team)
        if len(alive_teams) == 1:
            return alive_teams.pop()
        elif len(alive_teams) == 0:
            return -1
        else:
            return 0
        
    def deal_damage(self, actor: FightRole, target: FightRole, source: FightSkill | Buff, damage: int):
        self.dispatch_event(fightevents.BeforeTakeDamage(target, actor, source, damage))
        real_damage = target.take_damage(damage)
        self.log_action("take_damage", {
            "actor": target.uid,
            "value": real_damage,
            "left": target.health
        })
        self.dispatch_event(fightevents.AfterTakeDamage(target, actor, source, real_damage))
        if not target.is_alive():
            self.log_action("died", {
                "actor": target.uid
            })
            self.dispatch_event(fightevents.Died(target, actor))
