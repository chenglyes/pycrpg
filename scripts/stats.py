class Stats:
    def __init__(self):
        self._add_stats: dict[str, int] = {}
        self._multi_stats: dict[str, float] = {}

    def clear(self):
        self._add_stats.clear()
        self._multi_stats.clear()
    
    def copy(self):
        stats = Stats()
        stats._add_stats = self._add_stats.copy()
        stats._multi_stats = self._multi_stats.copy()
        return stats

    def add(self, type: str, value: int):
        if type not in self._add_stats:
            self._add_stats[type] = 0
        self._add_stats[type] += value
        if self._add_stats[type] < 0:
            raise ValueError(f"Stat {type} cannot be negative")

    def add_multi(self, type: str, value: float):
        if type not in self._multi_stats:
            self._multi_stats[type] = 0
        self._multi_stats[type] += value
        if self._multi_stats[type] < 0:
            raise ValueError(f"Stat {type} cannot be negative")

    def get(self, type: str) -> int:
        base_value = self._add_stats.get(type, 0)
        if base_value == 0:
            return 0
        multi_value = self._multi_stats.get(type, 0)
        value = base_value * (1 + multi_value)
        return round(value)
    