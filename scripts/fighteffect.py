from fightcontext import FightContext
from fightrole import FightRole

class FightEffect:
    def on_add(self, actor: FightRole, context: FightContext):
        pass

    def on_remove(self, actor: FightRole, context: FightContext):
        pass
