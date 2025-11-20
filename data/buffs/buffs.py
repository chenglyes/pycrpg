from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.buff import Buff
    from scripts.fightcontext import FightContext
    from scripts.fightrole import FightRole
else:
    from buff import Buff
    from fightcontext import FightContext
    from fightrole import FightRole

class Burn(Buff):
    def on_begin_turn(self, actor: FightRole, context: FightContext):
        damage = self.caster.calc_damage(0.1)
        context.deal_damage(self.caster, actor, self, damage)

class Slowdown(Buff):
    def on_add(self, actor: FightRole, context: FightContext):
        speed = 0.5 * actor.base_stats.get("speed")
        actor.stats.add("speed",speed)
    def on_remove(self, actor: FightRole, context: FightContext):
        speed = actor.base_stats.get("speed")
        actor.stats.add("speed",speed)

class Frozen(Buff):
    def on_add(self, actor: FightRole, context: FightContext):
        actor.add_state("frozen")
    def on_remove(self, actor: FightRole, context: FightContext):
        actor.remove_state("frozen")