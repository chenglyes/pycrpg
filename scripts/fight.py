from fightrole import FightRole
# from fightaction import FightAction
from random import Random
import uuid

class Fight:
    def __init__(self, seed: int = int(uuid.uuid4())):
        self.seed = seed
        self.init_roles: list[FightRole] = []
        self._random = Random(seed)
        self._winner: int = 0
        self._round: int = 0
        self._state: str = ""
        self._actions: list[dict] = []
        self._all_roles: list[FightRole] = []
        self._actor_queue: list[FightRole] = []
        self._actor: FightRole | None = None

    @classmethod
    def from_saved(cls, data: dict):
        fight = cls(data["seed"])
        fight._winner = data["winner"]
        # load init roles
        # load actions
    
    @property
    def round(self) -> int:
        return self._round
    
    @property
    def actor(self) -> FightRole | None:
        return self._actor

    @property
    def actor_queue(self) -> list[FightRole]:
        return self._actor_queue

    def add_init_role(self, role: FightRole):
        self.init_roles.append(role)

    def simulate(self):
        self._reset()

        # TODO: copy every role
        self._all_roles = self.init_roles.copy()
        # self._all_roles.sort(key=lambda x: x.stats.speed, reverse=True)

        self._log_action("fight_start", {})

        self._winner = self._check_winner()
        
        while self._winner == 0:
            self._round += 1
            self._on_round()

        self._log_action("fight_end", {"winner": self._winner})
    
    def get_actions(self) -> list[dict]:
        return self._actions
    
    def _get_role(self, uid: str) -> FightRole:
        for role in self._all_roles:
            if role.uid == uid:
                return role
        raise ValueError(f"Role with uid '{uid}' not found.")
    
    def _reset(self):
        self._random.seed(self.seed)
        self._winner = 0
        self._round = 0
        self._actions.clear()
        self._all_roles.clear()
        self._actor_queue.clear()
        self._actor = None
        # self._state = ""

    def _check_winner(self) -> int:
        alive_teams = set()
        for role in self._all_roles:
            if role.is_alive:
                alive_teams.add(role.team)
        if len(alive_teams) == 1:
            return alive_teams.pop()
        elif len(alive_teams) == 0:
            return -1
        else:
            return 0
    
    def _log_action(self, type: str, data: dict):
        action = {"type": type, **data}
        self._actions.append(action)

    def _on_round(self):
        self._log_action("round_start", {"round": self._round})
        active_roles = [role for role in self._all_roles if role.is_alive]
        active_roles.sort(key=lambda x: x.stats.speed, reverse=True)

        for role in active_roles:
            if role.is_alive:
                continue

            self._on_turn(role)

            self._winner = self._check_winner()
            if self._winner != 0:
                break

    def _on_turn(self, actor: FightRole):
        self._log_action("turn_start", {
            "actor": actor.uid,
        })

        # attack rand 1 enemy
        enemys = [role for role in self._all_roles if role.is_alive and role.team != actor.team]
        if not enemys:
            return
        
        target = self._random.choice(enemys)

        damage = actor.stats.attack
        self._log_action("attack", {
            "actor": actor.uid,
            "targets": [target.uid]
        })

        target.take_damage(damage)
        self._log_action("take_damage", {
            "actor": target.uid,
            "value": damage
        })
