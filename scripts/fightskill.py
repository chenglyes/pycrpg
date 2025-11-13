from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fightrole import FightRole
    from fightcontext import FightContext
from skill import Skill
import importlib.util

class FightSkill:
    def __init__(self, skill: Skill):
        self.skill = skill
        self.cooltime: int = 0

    def prepare_fight(self, actor: FightRole, context: FightContext):
        pass

    def update_cooltime(self):
        if self.cooltime > 0:
            self.cooltime -= 1
    
    def can_cast(self, actor: FightRole, context: FightContext) -> bool:
        # TODO check cooltime
        return self.cooltime == 0
    
    def do_cast(self, actor: FightRole, context: FightContext):
        pass
    
    def cast(self, actor: FightRole, context: FightContext):
        self.do_cast(actor, context)
        self.cooltime = self.skill.template.cooldown


class FightSkillMan:
    @classmethod
    def load(cls, skill: Skill) -> FightSkill:
        module_name, class_name = skill.template.entry.rsplit('.', 1)
        module_path = module_name.replace(".", "/") + ".py"
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None or spec.loader is None:
            raise Exception(f"Failed to load skill module '{skill.template.entry}'")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        skill_class = getattr(module, class_name)
        if not issubclass(skill_class, FightSkill):
            raise TypeError(f"Class '{class_name}' is not a subclass of FightSkill")
        return skill_class(skill)
    