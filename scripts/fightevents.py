from fightrole import FightRole
from fightskill import FightSkill

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

class EndTurn:
    def __init__(self, actor: FightRole):
        self.actor  = actor

class BeforeTakeDamage:
    def __init__(self, actor: FightRole, caster: FightRole, skill: FightSkill, damage: int):
        self.actor = actor
        self.caster = caster
        self.skill = skill
        self.damage = damage

class AfterTakeDamage:
    def __init__(self, actor: FightRole, caster: FightRole, skill: FightSkill, damage: int):
        self.actor = actor
        self.caster = caster
        self.skill = skill
        self.damage = damage

class Died:
    def __init__(self, actor: FightRole, killer: FightRole):
        self.actor = actor
        self.killer = killer
        