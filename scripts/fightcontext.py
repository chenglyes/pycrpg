from eventman import EventMan
from fightrole import FightRole
from random import Random

class FightContext:
    def __init__(self, seed: int):
        self.random = Random(seed)
        self.event_man = EventMan()
        self.all_roles: list[FightRole] = []
        self.actor: FightRole | None = None
        self.actor_queue: list[FightRole] = []
        self.round: int = 0
        # self.winner: int = 0
        self.actions: list[dict] = []

    def dispatch_event(self, event):
        self.event_man.dispatch(event)

    def log_action(self, type: str, data: dict):
        action = {"type": type, **data}
        self.actions.append(action)

    def check_winner(self) -> int:
        alive_teams = set()
        for role in self.all_roles:
            if role.is_alive:
                alive_teams.add(role.team)
        if len(alive_teams) == 1:
            return alive_teams.pop()
        elif len(alive_teams) == 0:
            return -1
        else:
            return 0
        