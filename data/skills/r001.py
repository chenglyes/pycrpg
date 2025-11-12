from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.fightskill import FightSkill
    from scripts.fightcontext import FightContext
    from scripts.fightrole import FightRole
    import scripts.fightevents as fightevents
else:
    from fightskill import FightSkill
    from fightcontext import FightContext
    from fightrole import FightRole
    import fightevents as fightevents

class Fireball(FightSkill):
    def register_events(self):
        self.context.event_man.register(fightevents.OnTurn, lambda e: self.on_turn(e, self.owner, self.context))

    def on_turn(self, event: fightevents.OnTurn, owner: FightRole, context: FightContext):
        if event.actor != owner:
            return
        return self.cast(self.owner, context)

    def cast(self, caster: FightRole, context: FightContext):
        # check pre-condition
        if not caster.is_alive:
            return
        
        enemys = [r for r in self.context.all_roles if r.is_alive and r.team != caster.team]
        if not enemys:
            return

        target = self.context.random.choice(enemys)

        self.context.log_action("cast_skill", {
            "actor": caster.uid,
            "skill": self.template.id,
            "targets": [target.uid]
        })

        damage = caster.stats.attack

        self.context.deal_damage(caster, target, self, damage)
