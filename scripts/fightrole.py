from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fightcontext import FightContext
from role import Role
from fightskill import FightSkill, FightSkillMan

class FightRole:
    def __init__(self, role: Role, team: int, field: int):
        self.uid = role.uid
        self.template = role.template
        self.team = team
        self.field = field
        self.base_stats = role.get_stats()
        self.stats = self.base_stats.copy()
        self.health = self.stats.get("health")
        self.buffs = []
        self.skills: list[FightSkill] = []
        for skill in role.skills:
            self.skills.append(FightSkillMan.load(skill))

    def is_alive(self) -> bool:
        return self.health > 0
    
    def can_act(self) -> bool:
        # TODO check state
        return self.is_alive()
    
    def prepare_fight(self, context: FightContext):
        for skill in self.skills:
            skill.prepare_fight(self, context)

    def calc_damage(self, context: FightContext, k: float) -> int:
        # TODO sum attack
        damage = round(self.stats.get("attack") * k)
        # TODO check critical
        if context.random.random() < 0.1:
            damage = round(damage * 1.5)
        return damage

    def take_damage(self, value: int) -> int:
        if value < 0:
            raise ValueError("Damage value must be non-negative.")
        # TODO cacl defense
        reduce = 200 / (200 + self.stats.get("defense"))
        damage = max(1, round(value * reduce))
        self.health -= damage
        return damage
