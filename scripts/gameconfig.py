class GameConfig:
    ROLE_MAX_LEVEL: int = 100

    @classmethod
    def get_role_levelup_exp(cls, current_level: int) -> int:
        tier = (current_level - 1) // 10
        base = 80 * (1.6 ** tier)
        growth = 30 * (current_level ** 1.3)
        return round(base + growth)
    
    @classmethod
    def get_role_defense_damage(cls, damage: int, defense: int) -> int:
        reduce = 200 / (200 + defense)
        return max(1, round(damage * reduce))
