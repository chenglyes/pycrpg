from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fightrole import FightRole
    from fightcontext import FightContext
from bufftemplman import BuffTempl, BuffTemplMan
import importlib.util

class Buff:
    def __init__(self, template: BuffTempl, stack: int = 1, duration: int = 1):
        self.template = template
        self.stack = stack
        self.duration = duration
        self.time = duration

    def try_stack(self, buff: Buff) -> bool:
        if self.template.id != buff.template.id:
            return False
        self.stack = min(self.stack + buff.stack, self.template.stacks)
        self.duration = max(self.duration, buff.duration)
        return True

    def on_add(self, actor: FightRole, context: FightContext):
        pass

    def on_remove(self, actor: FightRole, context: FightContext):
        pass

    def on_begin_turn(self, actor: FightRole, context: FightContext):
        pass

    def on_end_turn(self, actor: FightRole, context: FightContext):
        self.time -= 1
        if self.time <= 0:
            actor.remove_buff(self)

class BuffMan:
    @classmethod
    def create(cls, tid: str, stack: int = 1, duration: int = 1) -> Buff:
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
        return buff_class(template, stack, duration)
    