from dataclasses import dataclass

@dataclass
class SkillTempl:
    id: str
    name: str
    description: str
    cost: int
    cooldown: int
    entry: str
