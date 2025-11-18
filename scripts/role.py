# from roletempl import RoleTempl
from roletemplman import RoleTemplMan
from stats import Stats
from skill import Skill
import uuid

class Role:
    def __init__(self, tid: str, uid: str | None = None):
        template = RoleTemplMan.get(tid)
        if template is None:
            raise Exception(f"Invalid template ID '{tid}'.")
        self.template = template
        self.uid = uid if uid else str(uuid.uuid4())
        self.level: int = 1
        self.exp: int = 0
        self.skills: list[Skill] = []
        for skill_id in template.skills:
            self.skills.append(Skill(skill_id))
    
    @property
    def max_health(self) -> int:
        return self.template.base_health + (self.level - 1) * 10
    
    def get_stats(self) -> Stats:
        stats = Stats()
        # TODO sum stats
        stats.add("health", self.template.base_health)
        stats.add("attack", self.template.base_attack)
        stats.add("defense", self.template.base_defense)
        stats.add("speed", self.template.base_speed)
        return stats
    
    def get_skill(self, id: str) -> Skill:
        for skill in self.skills:
            if skill.template.id == id:
                return skill
        raise IndexError(f"Skill {id} not in this role")

    @classmethod
    def from_saved(cls, data: dict):
        role = cls(data["tid"], data["uid"])
        role.level = data["level"]
        role.exp = data["exp"]
        return role

    def to_saved(self) -> dict:
        return {
            "uid": self.uid,
            "tid": self.template.id,
            "level": self.level,
            "exp": self.exp
        }
