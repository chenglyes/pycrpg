from dataclasses import dataclass

@dataclass
class BuffTempl:
    id: str
    name: str
    desc: str
    stacks: int
    entry: str
