from __future__ import annotations
from typing import TYPE_CHECKING, Callable
from .role import Role
from .fightskill import FightSkill, FightSkillMan
from .buff import Buff
from .eventman import EventMan
if TYPE_CHECKING:
    from .fightcontext import FightContext

class FightRole:
    def __init__(self, role: Role, team: int, field: int, context: FightContext):
        self.uid = role.uid
        self.template = role.template
        self.team = team
        self.field = field
        self.context = context
        self.event_man = EventMan()
        self.base_stats = role.get_stats()
        self.stats = self.base_stats.copy()
        self.health = self.stats.get("health")
        self.states: dict[str, int] = {}
        self.buffs: list[Buff] = []
        self.skills: list[FightSkill] = []
        for skill in role.skills:
            self.skills.append(FightSkillMan.load(skill))

    def is_alive(self) -> bool:
        return self.health > 0
    
    def add_state(self, state: str):
        if state in self.states:
            self.states[state] += 1
        else:
            self.states[state] = 1

    def remove_state(self, state: str):
        if state in self.states:
            self.states[state] -= 1
            if self.states[state] == 0:
                self.states.pop(state)

    def has_state(self, state: str) -> bool:
        return state in self.states
    
    def add_buff(self, buff: Buff):
        has_buff = False
        for b in self.buffs:
            if b.try_stack(buff, self, self.context):
                has_buff = True
                self.context.log_action("stack_buff", {
                    "actor": self.uid,
                    "caster": buff.caster.uid,
                    "buff": b.template.id,
                    "stack": b.stack,
                    "duration": b.duration
                })
                break
        if not has_buff:
            self.context.log_action("add_buff", {
                "actor": self.uid,
                "caster": buff.caster.uid,
                "buff": buff.template.id,
                "stack": buff.stack,
                "duration": buff.duration
            })
            buff.on_add(self, self.context)
            self.buffs.append(buff)

    def remove_buff(self, buff: Buff):
        for i, b in enumerate(self.buffs):
            if b.template.id == buff.template.id:
                self.context.log_action("remove_buff", {
                    "actor": self.uid,
                    "buff": buff.template.id
                })
                b.on_remove(self, self.context)
                self.buffs.pop(i)
                break
            
    def get_buff(self, id: str) -> Buff | None:
        for b in self.buffs:
            if b.template.id == id:
                return b
        return None
    
    def can_act(self) -> bool:
        if not self.is_alive():
            return False
        for state in [ "dizzy", "frozen" ]:
            if self.has_state(state):
                return False
        return True
    
    def prepare_fight(self):
        for skill in self.skills:
            skill.prepare_fight(self, self.context)

    def register_event(self, event_type: type, callback: Callable[..., bool]) -> int:
        return self.event_man.register(event_type, callback)
    
    def unregister_event(self, id: int):
        self.event_man.unregister(id)

    def dispatch_event(self, event) -> bool:
        return self.event_man.dispatch(event)

    def calc_damage(self, k: float = 1.0, base_stat: str = "attack") -> int:
        damage = round(self.stats.get(base_stat) * k)
        if self.context.random.random() < (self.stats.get("critical_changce") / 100):
            damage = round(damage * (1.0 + self.stats.get("critical_damage") / 100))
        return damage

    def take_damage(self, value: int) -> int:
        if value < 0:
            raise ValueError("Damage value must be non-negative.")
        reduce = 200 / (200 + self.stats.get("defense"))
        damage = max(1, round(value * reduce))
        self.health -= damage
        return damage
    
    def select_cast_skill(self) -> FightSkill | None:
        for skill in self.skills:
            if skill.can_cast(self, self.context):
                return skill
        return None
    
    def update_cooltimes(self):
        for skill in self.skills:
            skill.update_cooltime()

    def update_buffs(self):
        for buff in self.buffs:
            buff.duration -= 1
        need_removes = [b for b in self.buffs if b.duration <= 0]
        for buff in need_removes:
            self.remove_buff(buff)

    def on_begin_turn(self):
        for buff in self.buffs:
            buff.on_begin_turn(self, self.context)

    def on_end_turn(self):
        for buff in self.buffs:
            buff.on_end_turn(self, self.context)
