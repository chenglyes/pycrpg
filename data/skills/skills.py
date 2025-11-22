from scripts.fightskill import Skill, FightSkill
from scripts.buff import BuffMan
from scripts.fightrole import FightRole
from scripts.fightcontext import FightContext

class BaseAttack(FightSkill):
    def __init__(self, skill: Skill, /, k: float = 1.0, target_num: int = 1, base_stat: str = "attack"):
        super().__init__(skill)
        self.k = k
        self.target_num = target_num
        self.base_stat = base_stat
    
    def can_cast(self, actor: FightRole, context: FightContext) -> bool:
        if not super().can_cast(actor, context):
            return False
        self.enemys = [r for r in context.all_roles if r.is_alive() and r.team != actor.team]
        return len(self.enemys) > 0
    
    def do_cast(self, actor: FightRole, context: FightContext):
        targets = context.random.sample(self.enemys, k=min(len(self.enemys), self.target_num))
        for target in targets:
            damage = actor.calc_damage(self.k, self.base_stat)
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
                
class Snowball(FightSkill):
    def can_cast(self, actor: FightRole, context: FightContext) -> bool:
        if not super().can_cast(actor, context):
            return False
        self.enemys = [r for r in context.all_roles if r.is_alive() and r.team != actor.team]
        return len(self.enemys) > 0

    def do_cast(self, actor: FightRole, context: FightContext):
        for target in self.enemys:
            damage = actor.calc_damage(0.7 + 0.15 * (self.skill.level - 1))
            context.deal_damage(actor, target, self, damage)
            rand = context.random.random()
            if rand < 0.05:
                buff = BuffMan.create("b0003", actor)
                target.add_buff(buff)
            else:
                if rand < 0.5:
                    buff = BuffMan.create("b0002", actor,)
                    target.add_buff(buff)