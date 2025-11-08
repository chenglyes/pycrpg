from role import Role
from fightrole import FightRole
from fightcontext import FightContext
import fightevents
import uuid

class Fight:
    def __init__(self, seed: int = int(uuid.uuid4())):
        self.seed = seed
        self.init_teams: list[list[Role]] = []

    def add_team(self, team: list[Role]):
        self.init_teams.append(team)

    def simulate(self) -> list[dict]:
        context = FightContext(self.seed)
        
        for i, team in enumerate(self.init_teams):
            for j, role in enumerate(team):
                context.all_roles.append(FightRole(role, i, j))

        context.log_action("begin_fight", {})
        context.dispatch_event(fightevents.BeginFight())
        
        while context.check_winner() == 0:
            self._round += 1
            self._on_round(context)

        winner = context.check_winner()
        context.log_action("end_fight", {"winner": winner})

        return context.actions

    def _on_round(self, context: FightContext):
        context.log_action("begin_round", {"round": context.round})
        context.dispatch_event(fightevents.BeginRound(context.round))
        
        active_roles = [r for r in context.all_roles if r.is_alive]
        active_roles.sort(key=lambda x: x.stats.speed, reverse=True)

        for role in active_roles:
            if role.is_alive:
                self._on_turn(role, context)
                if context.check_winner() != 0:
                    break

    def _on_turn(self, actor: FightRole, context: FightContext):
        context.log_action("begin_turn", {
            "actor": actor.uid,
        })
        context.dispatch_event(fightevents.BeginTurn(actor))

        # attack rand 1 enemy
        enemys = [r for r in context.all_roles if r.is_alive and r.team != actor.team]
        if not enemys:
            return
        
        target = context.random.choice(enemys)

        damage = actor.stats.attack
        context.log_action("attack", {
            "actor": actor.uid,
            "targets": [target.uid]
        })

        target.take_damage(damage)
        context.log_action("take_damage", {
            "actor": target.uid,
            "value": damage
        })
