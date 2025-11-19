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

    def get_role(self, uid: str) -> Role:
        for team in self.init_teams:
            for role in team:
                if role.uid == uid:
                    return role
        raise IndexError(f"Role '{uid}' not found")

    def simulate(self) -> list[dict]:
        context = FightContext(self.seed, self.init_teams)
        
        context.log_action("begin_fight", {})
        context.dispatch_event(fightevents.BeginFight())
        
        while context.check_winner() == 0 and context.round < 30:
            self._on_round(context)

        winner = context.check_winner()
        context.log_action("end_fight", {"winner": winner})

        return context.actions

    def _on_round(self, context: FightContext):
        context.round += 1
        context.log_action("begin_round", {"round": context.round})
        context.dispatch_event(fightevents.BeginRound(context.round))
        
        active_roles = [r for r in context.all_roles if r.is_alive()]
        active_roles.sort(key=lambda x: x.stats.get("speed"), reverse=True)

        for role in active_roles:
            if role.is_alive():
                self._on_turn(role, context)
                if context.check_winner() != 0:
                    break

        context.log_action("end_round", {"round": context.round})
        context.dispatch_event(fightevents.EndRound(context.round))

    def _on_turn(self, actor: FightRole, context: FightContext):
        actor.update_cooltimes()
        context.log_action("begin_turn", {
            "actor": actor.uid,
        })
        context.dispatch_event(fightevents.BeginTurn(actor))
        actor.on_begin_turn()
        if actor.can_act():
            skill = actor.select_cast_skill()
            if skill is not None:
                context.log_action("cast_skill", {
                    "actor": actor.uid,
                    "skill": skill.skill.template.id
                })
                skill.cast(actor, context)
        actor.on_end_turn()
        actor.update_buffs()
        context.dispatch_event(fightevents.EndTurn(actor))
        context.log_action("end_turn", {
            "actor": actor.uid,
        })
