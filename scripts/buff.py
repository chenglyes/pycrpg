from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .fightrole import FightRole
    from .fightcontext import FightContext
from .bufftempl import BuffTempl, BuffTemplMan
import importlib.util

class Buff:
    def __init__(self, template: BuffTempl, caster: FightRole, stack: int, duration: int):
        self.template = template
        self.caster = caster
        self.stack = stack
        self.duration = duration

    def try_stack(self, buff: Buff, actor: FightRole, context: FightContext) -> bool:
        if self.template.id != buff.template.id:
            return False
        new_stack = self.stack + buff.stack
        if self.template.stacks != 0 and new_stack > self.template.stacks:
            new_stack = self.template.stacks
        if self.stack != new_stack:
            self.on_remove(actor, context)
            self.stack = new_stack
            self.on_add(actor, context)
        self.duration = max(self.duration, buff.duration)
        return True

    def on_add(self, actor: FightRole, context: FightContext):
        pass

    def on_remove(self, actor: FightRole, context: FightContext):
        pass

    def on_begin_turn(self, actor: FightRole, context: FightContext):
        pass

    def on_end_turn(self, actor: FightRole, context: FightContext):
        pass

class BuffMan:
    @classmethod
    def create(cls, tid: str, caster: FightRole, stack: int = 1, duration: int = 1) -> Buff:
        template = BuffTemplMan.get(tid)
        if template is None:
            raise Exception(f"Invalid buff template ID '{tid}'.")
        module_name, class_name = template.entry.rsplit('.', 1)
        module_path = module_name.replace(".", "/") + ".py"
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None or spec.loader is None:
            raise Exception(f"Failed to load buff module '{template.entry}'")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        buff_class = getattr(module, class_name)
        if not issubclass(buff_class, Buff):
            raise TypeError(f"Class '{class_name}' is not a subclass of Buff")
        return buff_class(template, caster, stack, duration, **template.args)
    