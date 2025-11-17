from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fightrole import FightRole
    from fightcontext import FightContext

class Buff:
    def __init__(self, duration: int = 1):
        self.duration = duration
        self.time_left = duration

    def on_add(self, actor: FightRole, context: FightContext):
        pass

    def on_remove(self, actor: FightRole, context: FightContext):
        pass

    def on_begin_turn(self, actor: FightRole, context: FightContext):
        pass

    def on_end_turn(self, actor: FightRole, context: FightContext):
        pass
    