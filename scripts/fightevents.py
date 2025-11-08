from fightrole import FightRole

class BeginFight: pass

class BeginRound:
    def __init__(self, round: int):
        self.round = round

class EndRound:
    def __init__(self, round: int):
        self.round = round

class BeginTurn:
    def __init__(self, actor: FightRole):
        self.actor  = actor
