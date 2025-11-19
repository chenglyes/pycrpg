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
