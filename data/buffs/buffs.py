from scripts.buff import Buff, BuffTempl
from scripts.fightcontext import FightContext
from scripts.fightrole import FightRole

class DamageBeinTurn(Buff):
    def __init__(self, template: BuffTempl, caster: FightRole, stack: int, duration: int, /,
                 k: float = 1.0, base_stat: str = "attack"):
        super().__init__(template, caster, stack, duration)
        self.k = k
        self.base_stat = base_stat

    def on_begin_turn(self, actor: FightRole, context: FightContext):
        damage = self.caster.calc_damage(self.k, self.base_stat)
        context.deal_damage(self.caster, actor, self, damage)

class StateBuff(Buff):
    def __init__(self, template: BuffTempl, caster: FightRole, stack: int, duration: int, /,
                 state: str):
        super().__init__(template, caster, stack, duration)
        self.state = state
    
    def on_add(self, actor: FightRole, context: FightContext):
        actor.add_state(self.state)
    
    def on_remove(self, actor: FightRole, context: FightContext):
        actor.remove_state(self.state)

class Statbuff(Buff):
    def __init__(self, template: BuffTempl, caster: FightRole, stack: int, duration: int, /,
                 k: float = 1.0, base_stat: str = None):
        super().__init__(template, caster, stack, duration)
        self.k = k
        self.target_stat = base_stat
    
    def on_readd(self, buff:Buff, actor: FightRole, context: FightContext):
        self.stack = min(self.template.stacks,self.stack+buff.stack)
        self.time+=buff.duration
        self.on_remove(actor,context)
        self.on_add(actor,context)

    def on_add(self, actor: FightRole, context: FightContext):
        self.stat = self.stack*self.k * actor.base_stats.get(self.target_stat)
        actor.stats.add(self.target_stat,self.stat)

    def on_remove(self, actor: FightRole, context: FightContext):
        actor.stats.add(self.target_stat,-self.stat)
        