from fightskill import FightSkill
import fightevents as fightevents

class Fireball(FightSkill):
    def register_events(self):
        self.context.event_man.register(fightevents.OnTurn, self.on_turn)

    def on_turn(self, event: fightevents.OnTurn):
        if not self.owner.is_alive:
            return
        if event.actor == self.owner:
            enemys = [r for r in self.context.all_roles if r.is_alive and r.team != self.owner.team]
            if not enemys:
                return

            target = self.context.random.choice(enemys)

            self.context.log_action("cast_skill", {
                "actor": self.owner.uid,
                "skill": self.template.id,
                "targets": [target.uid]
            })

            damage = self.owner.stats.attack

            self.context.log_action("take_damage", {
                "actor": target.uid,
                "value": damage
            })

            target.health -= damage
