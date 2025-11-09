from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fightcontext import FightContext
from role import Role
from fightskill import FightSkill

class FightRole:
    def __init__(self, role: Role, team: int, field: int, context: FightContext):
        self.uid = role.uid
        self.template = role.template
        self.stats = role.stats
        self.team = team
        self.field = field
        self.context = context
        self.health = role.max_health
        self.buffs = []
        self.skills: list[FightSkill] = []
        for skill in role.skills:
            self.skills.append(FightSkill.create(skill, self, context))

    @property
    def is_alive(self) -> bool:
        return self.health > 0
    
    def register_events(self):
        for skill in self.skills:
            skill.register_events()

    def take_damage(self, value: int):
        if value < 0:
            raise ValueError("Damage value must be non-negative.")
        self.health -= value

    def take_heal(self, value: int):
        if value < 0:
            raise ValueError("Heal value must be non-negative.")
        self.health += value
