from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.fightskill import FightSkill
    from scripts.buff import BuffMan
    from scripts.fightrole import FightRole
    from scripts.fightcontext import FightContext
    #import scripts.fightevents as fightevents
else:
    from fightskill import FightSkill
    from buff import BuffMan
    from fightrole import FightRole
    from fightcontext import FightContext
    #import fightevents as fightevents

class Fireball(FightSkill):
    def can_cast(self, actor: FightRole, context: FightContext) -> bool:
        if not super().can_cast(actor, context):
            return False
        self.enemys = [r for r in context.all_roles if r.is_alive() and r.team != actor.team]
        return len(self.enemys) > 0

    def do_cast(self, actor: FightRole, context: FightContext):
        target = context.random.choice(self.enemys)
        damage = actor.calc_damage(1.0 + 0.1 * (self.skill.level - 1))
        context.deal_damage(actor, target, self, damage)

class BigFireball(FightSkill):
    def can_cast(self, actor: FightRole, context: FightContext) -> bool:
        if not super().can_cast(actor, context):
            return False
        self.enemys = [r for r in context.all_roles if r.is_alive() and r.team != actor.team]
        return len(self.enemys) > 0

    def do_cast(self, actor: FightRole, context: FightContext):
        for target in self.enemys:
            damage = actor.calc_damage(1.2 + 0.15 * (self.skill.level - 1))
            context.deal_damage(actor, target, self, damage)
            if context.random.random() < 0.20:
                buff = BuffMan.create("b0001", actor)
                target.add_buff(buff)
                