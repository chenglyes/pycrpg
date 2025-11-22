from dataclasses import dataclass, field
import json

@dataclass
class RoleTempl:
    id: str
    name: str
    base_health: int
    base_attack: int
    base_defense: int
    base_speed: int
    skills: list[str] = field(default_factory=list)

class RoleTemplMan:
    _templates: dict[str, RoleTempl] = {}

    @classmethod
    def load(cls, file: str):
        with open(file, "r", encoding="utf-8") as f:
            root = json.load(f)
            cls._templates = {}
            for data in root:
                template = RoleTempl(**data)
                cls._templates[template.id] = template
    
    @classmethod
    def save(cls, file: str):
        with open(file, "w", encoding="utf-8") as f:
            json.dump(cls._templates.values(), f, indent=4)

    @classmethod
    def get(cls, id: str) -> RoleTempl | None:
        return cls._templates.get(id)
    
    @classmethod
    def get_all_roles(cls) -> list[str]:
        return list(cls._templates.keys())
