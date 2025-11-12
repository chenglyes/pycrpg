from eventman import EventMan
from fightcontext import FightContext
from fightrole import FightRole

class FightEffect:
    def enter_fight(self, owner: FightRole, context: FightContext):
        pass

    def exit_fight(self, owner: FightRole, context: FightContext):
        pass
    