from __future__ import annotations
from typing import TYPE_CHECKING
from role import Role
from fightskill import FightSkill, FightSkillMan
from buff import Buff
if TYPE_CHECKING:
    from fightcontext import FightContext

class FightRole:
    def __init__(self, role: Role, team: int, field: int, context: FightContext):
        self.uid = role.uid
        self.template = role.template
        self.team = team
        self.field = field
        self.context = context
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
        self.context.log_action("add_buff", {
            "actor": self.uid,
            "caster": buff.caster.uid,
            "buff": buff.template.id,
            "stack": buff.stack,
            "duration": buff.duration
        })
        stacked = False
        for b in self.buffs:
            if b.try_stack(buff):
                stacked = True
                break
        if not stacked:
            self.buffs.append(buff)
        buff.on_add(self, self.context)

    def remove_buff(self, buff: Buff):
        buff.on_remove(self, self.context)
        self.context.log_action("remove_buff", {
            "actor": self.uid,
            "buff": buff.template.id
        })
        for i, b in enumerate(self.buffs):
            if b == buff:
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

    def calc_damage(self, k: float) -> int:
        damage = round(self.stats.get("attack") * k)
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
            buff.time -= 1
        need_removes = [b for b in self.buffs if b.time <= 0]
        for buff in need_removes:
            self.remove_buff(buff)

    def on_begin_turn(self):
        for buff in self.buffs:
            buff.on_begin_turn(self, self.context)

    def on_end_turn(self):
        for buff in self.buffs:
            buff.on_end_turn(self, self.context)
