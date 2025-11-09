from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fightrole import FightRole
    from fightcontext import FightContext
from skill import Skill
import importlib.util

class FightSkill:
    def __init__(self, skill: Skill, owner: FightRole, context: FightContext):
        self.template = skill.template
        self.level = skill.level
        self.owner = owner
        self.context = context

    def register_events(self): pass

    @classmethod
    def create(cls, skill: Skill, owner: FightRole, context: FightContext):
        module_name, class_name = skill.template.entry.rsplit('.', 1)
        module_path = module_name.replace(".", "/") + ".py"
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None or spec.loader is None:
            raise Exception(f"Failed to load skill module '{skill.template.entry}'")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        #module = importlib.import_module(module_name)
        skill_class = getattr(module, class_name)
        return skill_class(skill, owner, context)
    