from dataclasses import dataclass, field

@dataclass
class RoleTempl:
    id: str
    name: str
    base_health: int
    base_attack: int
    base_defense: int
    base_speed: int
    skills: list[str] = field(default_factory=list)
