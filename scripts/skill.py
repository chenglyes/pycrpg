from skilltemplman import SkillTemplMan

class Skill:
    def __init__(self, tid: str):
        template = SkillTemplMan.get(tid)
        if template is None:
            raise Exception(f"Invalid template ID '{tid}'.")

        self.template = template
        self.level: int = 1

    @classmethod
    def from_saved(cls, data: dict):
        skill = cls(data["tid"])
        skill.level = data["level"]
        return skill
    